import os
import json
from typing import Dict, List, Any

from agents.memory.message_bus import MessageBus, create_handoff_message
from agents.memory.agent_brain import memory_system

class CopyWriter:
    def __init__(self):
        self.name = "CopyWriter"
        self.message_bus = MessageBus()
        self.brain = memory_system.get_brain(self.name)
        self.message_bus.subscribe(self.name, self.receive_message)
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY', '')
        self.groq_key = os.getenv('GROQ_API_KEY', '')
        self.openrouter_url = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
        self.groq_url = os.getenv('GROQ_BASE_URL', 'https://api.groq.com/openai/v1')

    def receive_message(self, message):
        if message.message_type == "handoff" and message.to_agent == self.name:
            task_data = message.payload
            self.process_task(task_data)

    def process_task(self, task_data: Dict):
        self.brain.remember(f"CopyWriter received task: {task_data.get('task_id', 'unknown')}", "task_received")
        leads = task_data.get("leads", [])
        for lead in leads:
            self.generate_copy_for_lead(lead)

    def generate_copy_for_lead(self, lead: Dict) -> Dict:
        business_name = lead.get("business_name", "your business")
        niche = lead.get("niche", "business")
        city = lead.get("city", "your area")
        worst_reviews = lead.get("worst_reviews", [])
        current_rating = lead.get("current_rating", 3.0)

        copy_variants = {
            "cold_intro": {
                "subjects": [
                    f"Quick question about {business_name}",
                    f"{business_name} - one question",
                    f"Saw something interesting about {business_name}"
                ],
                "body": f"""Hi there,

I came across {business_name} while researching {niche} businesses in {city}, and I noticed something that might interest you.

Most businesses like yours are losing customers every single month due to negative reviews online. The worst part? Most of them don't even know it's happening.

I saw reviews like: "{worst_reviews[0][:100] if worst_reviews else 'multiple negative reviews'}"...

A quick question: have you ever tried to remove an unfair Google review before?

I'd love to chat for 5 minutes if you're open to it.

Best,
Michael"""
            },
            "social_proof": {
                "subjects": [
                    f"Re: Quick question about {business_name}",
                    f"How we helped similar {niche} businesses",
                    f"Proven results for {business_name}"
                ],
                "body": f"""Hi there,

Following up on my last email.

We recently helped a {niche} business in {city} remove 12 negative reviews in 3 weeks.

Result? Their Google rating went from {current_rating:.1f} to 4.6 stars.

Want to see how we did it?

Best,
Michael"""
            },
            "fear_trigger": {
                "subjects": [
                    f"What happens if negative reviews keep piling up?",
                    f"Don't ignore this about {business_name}",
                    f"The cost of inaction for {business_name}"
                ],
                "body": f"""Hi there,

Here's what I see happening with businesses that don't address their negative reviews:

Month 1: 3 negative reviews → 15 potential customers click away
Month 3: 7 negative reviews → 40 potential customers lost
Month 6: 12 negative reviews → Business is bleeding

Your competitors? They've already figured this out.

The longer you wait, the harder it gets.

Best,
Michael"""
            }
        }

        self.brain.remember(f"Generated copy variants for {business_name}", "copy_generated")

        return {
            "lead_id": lead.get("lead_id", "unknown"),
            "copy_variants": copy_variants,
            "status": "ready"
        }

    def get_copy_for_funnel_step(self, lead: Dict, step: int) -> Dict:
        copy_map = {
            1: "cold_intro",
            2: "social_proof",
            3: "fear_trigger"
        }
        angle = copy_map.get(step, "cold_intro")
        generated = self.generate_copy_for_lead(lead)
        return {
            "step": step,
            "angle": angle,
            "content": generated["copy_variants"].get(angle, {})
        }

    def start(self):
        return {"status": "online", "capabilities": ["cold_email", "follow_up", "fear_triggers"]}