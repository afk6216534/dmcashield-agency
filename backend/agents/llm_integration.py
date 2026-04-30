"""
Advanced LLM Integration Module
=============================
Handles dynamic model selection, fallback chains, and cost optimization
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import random

class LLMProvider:
    """Represents a single LLM provider with its configuration"""
    def __init__(self, name: str, model_id: str, cost_per_1k: float, quality_score: int, available: bool = True):
        self.name = name
        self.model_id = model_id
        self.cost_per_1k = cost_per_1k  # USD per 1K tokens
        self.quality_score = quality_score  # 1-10
        self.available = available
        self.total_tokens_used = 0
        self.total_cost = 0.0
        self.success_count = 0
        self.failure_count = 0
        self.avg_response_time = 0.0

    def record_usage(self, tokens: int, cost: float, response_time: float, success: bool):
        """Record usage statistics"""
        self.total_tokens_used += tokens
        self.total_cost += cost
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1

        # Update average response time
        if self.avg_response_time == 0:
            self.avg_response_time = response_time
        else:
            self.avg_response_time = (self.avg_response_time * 0.9) + (response_time * 0.1)

    def get_stats(self) -> Dict:
        return {
            "name": self.name,
            "model_id": self.model_id,
            "cost_per_1k": self.cost_per_1k,
            "quality_score": self.quality_score,
            "available": self.available,
            "total_tokens": self.total_tokens_used,
            "total_cost": self.total_cost,
            "success_rate": self.success_count / max(1, (self.success_count + self.failure_count)),
            "avg_response_time": self.avg_response_time
        }

class LLMRouter:
    """Routes requests to appropriate LLM based on task requirements"""

    def __init__(self):
        self.providers = {
            "claude_opus_4_7": LLMProvider("Claude Opus 4.7", "claude-opus-4-7", 0.015, 10),
            "claude_opus_4_6": LLMProvider("Claude Opus 4.6", "claude-opus-4-6", 0.012, 9),
            "claude_sonnet_4_6": LLMProvider("Claude Sonnet 4.6", "claude-sonnet-4-6", 0.008, 8),
            "gpt_5": LLMProvider("GPT-5", "gpt-5", 0.020, 10),
            "mistral_7b": LLMProvider("Mistral 7B", "mistralai/mistral-7b-instruct:free", 0.0, 6),
            "llama_3_1": LLMProvider("Llama 3.1", "meta-llama/llama-3.1-8b-instruct:free", 0.0, 7),
            "qwen_2_5": LLMProvider("Qwen 2.5", "qwen/qwen-2.5-7b-instruct:free", 0.0, 6),
            "mixtral": LLMProvider("Mixtral 8x7B", "mistralai/mixtral-8x7b-instruct:free", 0.0, 7)
        }

        self.fallback_chains = {
            "critical": ["claude_opus_4_7", "claude_opus_4_6", "gpt_5"],
            "high_quality": ["claude_sonnet_4_6", "claude_opus_4_6", "llama_3_1"],
            "cost_optimized": ["mistral_7b", "llama_3_1", "qwen_2_5"],
            "balanced": ["claude_sonnet_4_6", "llama_3_1", "mistral_7b"],
            "coding": ["claude_opus_4_7", "gpt_5", "claude_opus_4_6"],
            "creative": ["claude_opus_4_7", "gpt_5", "claude_sonnet_4_6"]
        }

        self.usage_history = []
        self.cost_budget_daily = 10.0  # USD
        self.cost_used_today = 0.0
        self.last_reset_day = datetime.now().day

    def select_model(self, task_type: str = "balanced",
                     min_quality: int = 5,
                     max_cost_per_1k: float = None) -> Optional[LLMProvider]:
        """Select best model based on requirements"""
        chain = self.fallback_chains.get(task_type, self.fallback_chains["balanced"])

        for provider_name in chain:
            provider = self.providers.get(provider_name)
            if not provider or not provider.available:
                continue
            if provider.quality_score < min_quality:
                continue
            if max_cost_per_1k and provider.cost_per_1k > max_cost_per_1k:
                continue
            if self.cost_used_today + (provider.cost_per_1k * 10) > self.cost_budget_daily:
                continue
            return provider

        # If no model found in chain, try any available
        for provider in sorted(self.providers.values(),
                               key=lambda p: (-p.quality_score, p.cost_per_1k)):
            if provider.available and provider.quality_score >= min_quality:
                return provider

        return None

    def execute_with_fallback(self, prompt: str, task_type: str = "balanced",
                               context: Dict = None, max_retries: int = 3) -> Dict:
        """Execute prompt with automatic fallback"""
        chain = self.fallback_chains.get(task_type, self.fallback_chains["balanced"])

        for attempt, provider_name in enumerate(chain[:max_retries]):
            provider = self.providers.get(provider_name)
            if not provider or not provider.available:
                continue

            start_time = time.time()
            try:
                # Simulate API call (in real implementation, call actual API)
                response = self._simulate_api_call(provider, prompt, context)
                response_time = time.time() - start_time

                # Calculate cost (simplified)
                tokens_used = len(prompt.split()) + len(response.get("text", "").split())
                cost = (tokens_used / 1000) * provider.cost_per_1k

                # Update statistics
                provider.record_usage(tokens_used, cost, response_time, True)
                self.cost_used_today += cost

                # Save to usage history
                self._save_usage_record(provider_name, prompt, response, cost, response_time, True)

                return {
                    "success": True,
                    "provider": provider_name,
                    "model": provider.model_id,
                    "response": response.get("text", ""),
                    "tokens_used": tokens_used,
                    "cost": cost,
                    "response_time": response_time,
                    "attempt": attempt + 1
                }

            except Exception as e:
                response_time = time.time() - start_time
                provider.record_usage(0, 0, response_time, False)
                self._save_usage_record(provider_name, prompt, {"error": str(e)}, 0, response_time, False)

                if attempt == len(chain[:max_retries]) - 1:
                    return {
                        "success": False,
                        "error": f"All providers failed. Last error: {str(e)}",
                        "attempts": attempt + 1
                    }

        return {"success": False, "error": "No available providers"}

    def _simulate_api_call(self, provider: LLMProvider, prompt: str, context: Dict = None) -> Dict:
        """Simulate API call (replace with actual API calls)"""
        # Simulate processing time
        time.sleep(random.uniform(0.5, 2.0))

        # Generate simulated response based on provider
        simulated_response = f"[Response from {provider.model_id}]\n\n"

        if "email" in prompt.lower():
            simulated_response += "Subject: Important Update\n\nDear valued customer...\n[Simulated email content]"
        elif "code" in prompt.lower():
            simulated_response += "```python\ndef solution():\n    # Implemented solution\n    return True\n```"
        else:
            simulated_response += f"Processed prompt: {prompt[:100]}...\n[Simulated intelligent response]"

        return {"text": simulated_response}

    def _save_usage_record(self, provider_name: str, prompt: str, response: Dict,
                           cost: float, response_time: float, success: bool):
        """Save usage record to memory"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "provider": provider_name,
            "prompt_length": len(prompt),
            "response": response,
            "cost": cost,
            "response_time": response_time,
            "success": success
        }
        self.usage_history.append(record)

        # Keep only last 1000 records
        if len(self.usage_history) > 1000:
            self.usage_history = self.usage_history[-1000:]

        # Save to persistent memory if available
        try:
            from agents.memory.persistent_memory import persistent_memory
            persistent_memory.save_conversation(
                role="llm_usage",
                content=json.dumps(record),
                metadata={"provider": provider_name, "cost": cost},
                encrypted=False
            )
        except ImportError:
            pass

    def get_provider_stats(self) -> List[Dict]:
        """Get statistics for all providers"""
        return [p.get_stats() for p in self.providers.values()]

    def get_cost_summary(self) -> Dict:
        """Get cost summary for current day"""
        today = datetime.now().day
        if today != self.last_reset_day:
            self.cost_used_today = 0.0
            self.last_reset_day = today

        return {
            "daily_budget": self.cost_budget_daily,
            "used_today": self.cost_used_today,
            "remaining": self.cost_budget_daily - self.cost_used_today,
            "currency": "USD",
            "total_tokens": sum(p.total_tokens_used for p in self.providers.values()),
            "total_cost_all_time": sum(p.total_cost for p in self.providers.values())
        }

    def update_provider_availability(self, provider_name: str, available: bool):
        """Update provider availability"""
        if provider_name in self.providers:
            self.providers[provider_name].available = available

    def add_custom_provider(self, name: str, model_id: str, cost_per_1k: float, quality: int):
        """Add a custom LLM provider"""
        self.providers[name] = LLMProvider(name, model_id, cost_per_1k, quality)
        # Add to fallback chains
        for chain in self.fallback_chains.values():
            if name not in chain:
                chain.append(name)

# Global router instance
llm_router = LLMRouter()