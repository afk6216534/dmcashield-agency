import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import asyncio

try:
    from langchain_openai import ChatOpenAI
    from langchain.prompts import PromptTemplate
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

class AIResponseGenerator:
    def __init__(self, config_file: str = "data/ai_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.llm = None
        self._init_llm()
    
    def _load_config(self) -> Dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "openai_api_key": "",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 500
        }
    
    def _save_config(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _init_llm(self):
        if not LANGCHAIN_AVAILABLE:
            return
        
        api_key = self.config.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                self.llm = ChatOpenAI(
                    model=self.config.get("model", "gpt-4"),
                    temperature=self.config.get("temperature", 0.7),
                    max_tokens=self.config.get("max_tokens", 500),
                    openai_api_key=api_key
                )
            except Exception as e:
                print(f"LLM init error: {e}")
    
    def configure(self, api_key: str = None, model: str = "gpt-4", temperature: float = 0.7):
        if api_key:
            self.config["openai_api_key"] = api_key
        self.config["model"] = model
        self.config["temperature"] = temperature
        self._save_config()
        self._init_llm()
    
    async def generate_response(self, context: Dict, lead: Dict) -> str:
        if not self.llm:
            return self._template_response(lead)
        
        prompt = self._build_prompt(context, lead)
        
        try:
            response = await self.llm.agenerate([prompt])
            return response.generations[0][0].text
        except Exception as e:
            print(f"AI response error: {e}")
            return self._template_response(lead)
    
    def _build_prompt(self, context: Dict, lead: Dict) -> str:
        business = lead.get("business_name", "")
        niche = lead.get("niche", "")
        city = lead.get("city", "")
        state = lead.get("state", "")
        
        prompt = f"""You are a professional DMCA specialist reaching out to help {business} in {city}, {niche}.

The business has negative reviews online that are hurting their reputation. You specialize in legal DMCA removal.

Write a personalized, professional email that:
1. Is warm and friendly, not pushy
2. Shows you understand their specific situation
3. Offers free consultation
4. Has clear call-to-action
5. Is under 150 words

Write the email now:"""
        return prompt
    
    def _template_response(self, lead: Dict) -> str:
        templates = [
            f"""Hi {lead.get('owner_name', 'there')},

I came across your business ({lead.get('business_name')}) and noticed you have some negative reviews online that are likely hurting your reputation.

We specialize in legal DMCA removal - helping businesses like yours remove fake, false, or illegal content from the web.

Would you be open to a free consultation? I'd love to show you what's possible.

Best regards""",
            
            f"""Hey {lead.get('owner_name', 'there')},

Quick question - have you ever thought about removing those negative reviews about {lead.get('business_name')}?

We help businesses in {lead.get('city')} clean up their online reputation through legal DMCA processes.

No pressure at all - just thought I'd reach out.

Cheers"""
        ]
        
        import random
        return random.choice(templates)
    
    async def generate_subject_line(self, lead: Dict) -> str:
        subjects = [
            f"Can I help remove those negative reviews?",
            f"Quick question about your reviews",
            f"Following up on {lead.get('business_name')}",
            f"Thought you'd want to see this",
            f"One quick question for you"
        ]
        
        import random
        return random.choice(subjects)
    
    def is_configured(self) -> bool:
        return self.llm is not None

ai_generator = AIResponseGenerator()

class SmartReplyHandler:
    def __init__(self):
        self.reply_templates = {
            "interested": [
                "Thank you for your interest! I'd love to schedule a quick call. What time works best for you?",
                "That's great to hear! Let me get you the information you need. What's your schedule like this week?",
                "Perfect! Let's talk. I'll send over some details and we can take it from there."
            ],
            "not_interested": [
                "No problem at all! If you ever need help in the future, don't hesitate to reach out. Best of luck!",
                "Totally understand. Thanks for your time! Take care.",
                "No worries! Just wanted to make sure you knew we were here if you ever need us."
            ],
            "question": [
                "Great question! Here's what you need to know...",
                "I'd be happy to answer that. Let me explain...",
                "Excellent question. Here's the breakdown..."
            ],
            "leave_me_alone": [
                "I apologize if this came across the wrong way. I'll stop reaching out. Best of luck!",
                "Understood. Sorry to bother you. Have a great day!"
            ]
        }
    
    def classify_reply(self, reply_text: str) -> str:
        text = reply_text.lower()
        
        if any(w in text for w in ['yes', 'interested', 'tell me more', 'how', 'schedule', 'call']):
            return "interested"
        elif any(w in text for w in ['no', 'not interested', 'stop', 'leave']):
            return "not_interested"
        elif any(w in text for w in ['?', 'what', 'how', 'tell me', 'explain']):
            return "question"
        elif any(w in text for w in ['leave me alone', 'stop texting', 'dont']):
            return "leave_me_alone"
        
        return "neutral"
    
    def generate_response(self, classification: str, lead: Dict) -> str:
        import random
        
        if classification == "neutral":
            templates = self.reply_templates["interested"]
        else:
            templates = self.reply_templates.get(classification, self.reply_templates["interested"])
        
        response = random.choice(templates)
        return response.format(name=lead.get("owner_name", "there"))

smart_reply = SmartReplyHandler()

class SentimentAnalyzer:
    def __init__(self):
        self.positive_words = ['thank', 'great', 'love', 'interested', 'yes', 'please', 'help', 'schedule', 'call', 'info']
        self.negative_words = ['no', 'not', 'stop', 'leave', 'dont', 'never', 'spam', 'hate', 'remove', 'unsubscribe']
        self.neutral_words = ['ok', 'thanks', 'maybe', 'later', 'think', 'consider']
    
    def analyze(self, text: str) -> Dict:
        text = text.lower()
        words = text.split()
        
        pos_count = sum(1 for w in words if w in self.positive_words)
        neg_count = sum(1 for w in words if w in self.negative_words)
        
        total = pos_count + neg_count
        if total == 0:
            score = 0.5
            sentiment = "neutral"
        else:
            score = pos_count / total
            if score > 0.6:
                sentiment = "positive"
            elif score < 0.4:
                sentiment = "negative"
            else:
                sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "score": score,
            "positive_matches": pos_count,
            "negative_matches": neg_count
        }
    
    def is_hot(self, text: str) -> bool:
        analysis = self.analyze(text)
        return analysis["sentiment"] == "positive" and analysis["score"] > 0.7

sentiment_analyzer = SentimentAnalyzer()