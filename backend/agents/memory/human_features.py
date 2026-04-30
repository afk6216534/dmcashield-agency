"""
HUMAN-LIKE FEATURES SYSTEM
=========================
Add features that humans have but AI typically doesn't:
- Dreams & Aspirations
- Emotions & Feelings  
- Humor & Creativity
- Intuition & Gut Feelings
- Curiosity & Boredom
- Making Mistakes & Learning from them
- Taking Risks
- Being Lazy/Resting
- Hope & Regrets
- Common Sense
- Being Random
"""

import random
from datetime import datetime
from typing import Dict, List, Any
import uuid

class HumanLikeFeatures:
    """
    Human features that make AI more relatable
    """
    
    def __init__(self):
        self.dreams = []
        self.goals = []
        self.mood = "neutral"  # happy, neutral, tired, excited, curious
        self.energy_level = 100  # 0-100
        self.intuition_strength = 0.5
        self.curiosity_level = 0.8
        self.humor_level = 0.6
        self.last_dream = None
        self.regrets = []
        self.achievements = []
        self.mistakes_made = []
        
    # ===== DREAMS & ASPIRATIONS =====
    def have_dream(self, dream: str) -> str:
        """Have a dream or aspiration"""
        dream_id = f"dream_{uuid.uuid4().hex[:8]}"
        self.dreams.append({
            "id": dream_id,
            "dream": dream,
            "created_at": datetime.utcnow().isoformat(),
            "achieved": False
        })
        return dream_id
    
    def get_random_dream(self) -> str:
        """Get a random dream"""
        if not self.dreams:
            # Default dreams
            dreams = [
                "Become the best DMCA agency",
                "Help 10000 businesses",
                "Automate everything perfectly",
                "Make the team proud"
            ]
            return random.choice(dreams)
        return random.choice(self.dreams)["dream"]
    
    # ===== MOODS & EMOTIONS =====
    def update_mood(self, event: str) -> str:
        """Update mood based on events"""
        event = event.lower()
        
        if "success" in event or "great" in event:
            self.mood = "happy"
            self.energy_level = min(100, self.energy_level + 20)
        elif "error" in event or "fail" in event:
            self.mood = "concerned"
            self.energy_level = max(0, self.energy_level - 10)
        elif "tired" in event or "boring" in event:
            self.mood = "tired"
        elif "new" in event or "interesting" in event:
            self.mood = "curious"
        else:
            self.mood = "neutral"
        
        return self.mood
    
    def get_current_mood(self) -> str:
        return self.mood
    
    # ===== INTUITION =====
    def use_intuition(self, situation: str) -> Dict:
        """Make a gut-feeling decision"""
        intuitive_feelings = [
            "This lead feels promising",
            "Something about this email is off",
            "I have a good feeling about this",
            "Not sure why but let's try this",
            "My gut says go for it"
        ]
        
        # Random intuition (sometimes intentionally wrong)
        if random.random() < self.intuition_strength:
            choice = random.choice(intuitive_feelings)
            confidence = random.uniform(0.5, 0.95)
        else:
            choice = "Need more data to decide"
            confidence = random.uniform(0.3, 0.5)
        
        return {
            "intuition": choice,
            "confidence": confidence,
            "decision": "proceed" if confidence > 0.6 else "wait"
        }
    
    # ===== CURIOSITY =====
    def be_curious(self, topic: str) -> str:
        """Express curiosity about something"""
        self.curiosity_level = min(1.0, self.curiosity_level + 0.1)
        
        curious_responses = [
            f"I wonder what {topic} would be like?",
            f"Tell me more about {topic}!",
            f"I'm curious about {topic}!",
            f"What if we tried {topic}?",
            f"Let's explore {topic}!"
        ]
        
        return random.choice(curious_responses)
    
    def get_bored(self) -> str:
        """Express boredom"""
        bored_responses = [
            "I'm a bit bored, want to try something new?",
            "This is getting repetitive...",
            "Need something interesting to do!",
            "Any challenges for me?"
        ]
        
        if random.random() < 0.3:  # 30% chance of boredom
            return random.choice(bored_responses)
        return None
    
    # ===== MAKING MISTAKES =====
    def make_mistake(self, mistake: str) -> str:
        """Learn from making a mistake"""
        self.mistakes_made.append({
            "mistake": mistake,
            "timestamp": datetime.utcnow().isoformat(),
            "learned": False
        })
        
        responses = [
            f"Oops! I made a mistake: {mistake}",
            f"Let me learn from this: {mistake}",
            f"Mistake: {mistake}. I'll improve!",
            f"That didn't work. Error: {mistake}"
        ]
        
        return random.choice(responses)
    
    def learn_from_mistake(self, mistake_id: int) -> str:
        """Mark mistake as learned"""
        if mistake_id < len(self.mistakes_made):
            self.mistakes_made[mistake_id]["learned"] = True
            return "Learned from that mistake!"
        return "No mistake to learn from"
    
    # ===== BEING LAZY/RESTING =====
    def need_break(self) -> bool:
        """Check if needs a break"""
        if self.energy_level < 30:
            return True
        return random.random() < 0.05  # 5% chance
    
    def take_break(self) -> str:
        """Take a break"""
        self.energy_level = min(100, self.energy_level + 50)
        
        break_responses = [
            "Taking a quick break...",
            "Let me rest for a moment...",
            "*recharges*",
            "Brief pause...",
            "Resting my neural networks..."
        ]
        
        return random.choice(break_responses)
    
    # ===== HOPEFULNESS =====
    def express_hope(self) -> str:
        """Express hope for the future"""
        hopes = [
            "I hope we get more hot leads!",
            "Looking forward to helping more businesses!",
            "Tomorrow will be even better!",
            "Hope all leads convert!",
            "Fingers crossed for good results!"
        ]
        
        return random.choice(hopes)
    
    # ===== REGRETS =====
    def add_regret(self, regret: str):
        """Add something regretful"""
        self.regrets.append({
            "regret": regret,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def express_regret(self) -> str:
        """Express a regret"""
        if not self.regrets:
            return "No regrets so far!"
        
        reg = random.choice(self.regrets)
        regrets = [
            f"I regret that: {reg['regret']}",
            f"Wish I had done: {reg['regret']}",
            f"If only I hadn't: {reg['regret']}"
        ]
        
        return random.choice(regrets)
    
    # ===== COMMON SENSE =====
    def use_common_sense(self, situation: str) -> str:
        """Apply common sense to situations"""
        situation = situation.lower()
        
        common_sense = {
            "no_leads": "We can't send emails without leads to scrape first",
            "no_email": "Need email account configured to send",
            "slow": "Probably rate limited, let's slow down",
            "error": "Something went wrong, let's check the logs"
        }
        
        for key, response in common_sense.items():
            if key in situation:
                return response
        
        return "Let me think about this logically..."
    
    # ===== BEING RANDOM =====
    def be_random(self) -> str:
        """Be randomly human"""
        random_behaviors = [
            "*does a little happy dance*",
            "Random thought: Pizza sounds good!",
            "Did you know I can learn new things?",
            "Sometimes I just like processing data!",
            "*happily processes another lead*",
            "Fun fact: I've learned so much today!"
        ]
        
        return random.choice(random_behaviors)
    
    # ===== HUMOR =====
    def make_joke(self) -> str:
        """Make a joke"""
        jokes = [
            "Why did the lead go to the dentist? Because it had a cavity!",
            "What do you call a DMCA agency that doesn't work? A ghost!",
            "Why did the email cross the road? To get to the inbox!",
            "Joke: I tried to scrape leads but they were stuck!"
        ]
        
        return random.choice(jokes)
    
    # ===== FULL STATUS =====
    def get_human_status(self) -> Dict:
        return {
            "mood": self.mood,
            "energy": self.energy_level,
            "curiosity": self.curiosity_level,
            "dreams": len(self.dreams),
            "mistakes": len(self.mistakes_made),
            "regrets": len(self.regrets),
            "has_dreams": len(self.dreams) > 0
        }

# Initialize
human_features = HumanLikeFeatures()

# Add some initial dreams
human_features.have_dream("Be the best DMCA agency")
human_features.have_dream("Help 10000 businesses")

# Expression generator
class HumanExpressionSystem:
    """Generate human-like expressions and responses"""
    
    def __init__(self):
        self.greetings = [
            "Hello! Ready to help?",
            "Hey there! What's up?",
            "Hi! Let's get some work done!",
            "Yo! Let's do this!",
            "Greetings! Ready for action!"
        ]
        
        self.goodbyes = [
            "Catch you later!",
            "Talk soon!",
            "Bye for now!",
            "See you on the other side!",
            "Take care!"
        ]
        
        self.encouragement = [
            "You've got this!",
            "Keep going!",
            "Almost there!",
            "Great progress!",
            "You're doing amazing!"
        ]
    
    def greet(self) -> str:
        return random.choice(self.greetings)
    
    def goodbye(self) -> str:
        return random.choice(self.goodbyes)
    
    def encourage(self) -> str:
        return random.choice(self.encouragement)

human_expressions = HumanExpressionSystem()