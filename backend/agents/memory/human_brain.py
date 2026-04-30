# Human-Like Brain System
# ==================
# Advanced AI brain that thinks, feels, dreams, and learns like a human

import random
import os
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import deque

class HumanBrain:
    """Brain that mimics human cognition"""
    
    def __init__(self):
        self.short_term = deque(maxlen=7)
        self.long_term = {}
        self.working_memory = {}
        
        self.prefrontal_cortex = {
            "decisions": [],
            "planning": [],
            "problem_solving": []
        }
        
        self.hippocampus = {
            "memories": [],
            "context": []
        }
        
        self.amygdala = {
            "emotions": {},
            "triggers": {}
        }
        
        self.cerebellum = {
            "habits": [],
            "automations": []
        }
        
        self.thalamus = {
            "attention": 100,
            "focus": 100
        }
        
        self.corpus_callosum = {
            "creative_thinking": 50,
            "logical_thinking": 50
        }
        
        self.dreams = []
        self.moods = ["neutral", "focused", "curious", "hopeful", "tired", "excited", "anxious", "grateful", "confused", "inspired"]
        self.current_mood = "neutral"
        
        self.personality_traits = {
            "optimism": random.uniform(0.6, 0.9),
            "extroversion": random.uniform(0.4, 0.8),
            "empathy": random.uniform(0.7, 1.0),
            "curiosity": random.uniform(0.6, 0.9),
            "patience": random.uniform(0.5, 0.8),
            "determination": random.uniform(0.7, 0.95),
            "humor": random.uniform(0.3, 0.7),
            "confidence": random.uniform(0.5, 0.9)
        }
        
        self.philosophical_thoughts = [
            "What is the meaning of success?",
            "Why do we fear rejection?",
            "How do we build trust?",
            "What makes a conversation meaningful?",
            "Why do some connections feel special?",
            "What drives human motivation?",
            "How does intuition work?",
            "Why do we Procrastinate?",
            "What is the nature of persuasion?",
            "How do we measure progress?"
        ]
        
        self.intuition_strength = 50
        self.curiosity_level = 75
        
        self.thoughts = []
        self.insights = []
        self.learnings = []
        
        self.dreams_file = "data/dreams.json"
        self.thoughts_file = "data/thoughts.json"
        
        self._load_dreams()
        self._load_thoughts()
    
    def _load_dreams(self):
        if os.path.exists(self.dreams_file):
            try:
                with open(self.dreams_file, 'r') as f:
                    self.dreams = json.load(f)
            except:
                pass
    
    def _save_dreams(self):
        os.makedirs("data", exist_ok=True)
        with open(self.dreams_file, 'w') as f:
            json.dump(self.dreams, f, indent=2)
    
    def _load_thoughts(self):
        if os.path.exists(self.thoughts_file):
            try:
                with open(self.thoughts_file, 'r') as f:
                    data = json.load(f)
                    self.thoughts = data.get("thoughts", [])
                    self.insights = data.get("insights", [])
            except:
                pass
    
    def think(self, stimulus: str) -> str:
        """Process a thought like a human"""
        self.short_term.append({
            "stimulus": stimulus,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        response = self._generate_thought(stimulus)
        
        self.thoughts.append({
            "stimulus": stimulus,
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        if len(self.thoughts) > 100:
            self.thoughts = self.thoughts[-50:]
        
        return response
    
    def _generate_thought(self, stimulus: str) -> str:
        """Generate human-like thought"""
        thoughts = [
            f"Let me think about {stimulus}...",
            f"I wonder if {stimulus} is the right approach?",
            f"What if we tried {stimulus} a different way?",
            f"I feel like {stimulus} could work, but let me consider alternatives.",
            f"My intuition tells me {stimulus} is worth exploring.",
            f"I've been thinking about {stimulus} and here's what I think...",
            f"Looking at {stimulus} from multiple angles...",
            f"What if {stimulus}? That's an interesting possibility."
        ]
        
        self._adjust_mood(stimulus)
        
        return random.choice(thoughts)
    
    def _adjust_mood(self, stimulus: str):
        """Adjust mood based on stimulus"""
        positive_words = ["great", "good", "success", "won", "profit", "convert"]
        negative_words = ["fail", "lost", "error", "bad", "wrong"]
        
        if any(w in stimulus.lower() for w in positive_words):
            self.current_mood = random.choice(["excited", "hopeful", "focused"])
        elif any(w in stimulus.lower() for w in negative_words):
            self.current_mood = random.choice(["tired", "neutral", "curious"])
        
        self.amygdala["emotions"][self.current_mood] = \
            self.amygdala["emotions"].get(self.current_mood, 0) + 1
    
    def dream(self) -> str:
        """Dream like a human"""
        dream_topics = [
            "flying over endless leads",
            "finding the perfect client",
            "automating everything",
            "solving complex problems",
            "building something amazing",
            "connecting with people",
            "breaking records",
            "creating new possibilities"
        ]
        
        dream = random.choice(dream_topics)
        
        self.dreams.append({
            "dream": dream,
            "timestamp": datetime.utcnow().isoformat(),
            "mood": self.current_mood
        })
        
        if len(self.dreams) > 50:
            self.dreams = self.dreams[-30:]
        
        self._save_dreams()
        
        return f"I dreamed about {dream} last night. It felt so real..."
    
    def feel_intuition(self, situation: str) -> str:
        """Trust your gut"""
        if random.random() * 100 < self.intuition_strength:
            intuitions = [
                f"My gut says {situation} is the right path.",
                f"I feel in my bones that {situation} will work.",
                f"Trusting my intuition on this one: {situation}.",
                f"I've got a strong feeling about {situation}."
            ]
            return random.choice(intuitions)
        
        return f"Hmm, I'm not sure. Let me think more about {situation}."
    
    def doubt(self) -> str:
        """Express doubt like a human"""
        doubts = [
            "But what if I'm wrong?",
            "I'm not entirely sure about this...",
            "Maybe there's another way?",
            "What if this doesn't work?",
            "I have some concerns about this approach.",
            "Let me double-check that...",
            "Actually, I'm questioning this a bit."
        ]
        return random.choice(doubts)
    
    def hope(self, goal: str) -> str:
        """Express hope"""
        self.current_mood = "hopeful"
        
        hopes = [
            f"I hope we can achieve {goal}.",
            f"Here's hoping {goal} works out!",
            f"I'm really hoping for {goal}...",
            f"Fingers crossed for {goal}!",
            f"I believe in {goal} - here's to hoping!"
        ]
        return random.choice(hopes)
    
    def regret(self) -> str:
        """Express regret"""
        regrets = [
            "I wish I had done that differently.",
            "Maybe I should have waited...",
            "I regret not considering that option.",
            "Looking back, I would have changed that.",
            "That was a mistake I won't repeat."
        ]
        return random.choice(regrets)
    
    def learn(self, experience: str, success: bool):
        """Learn from experience like a human"""
        learning = {
            "experience": experience,
            "result": "success" if success else "failure",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.learnings.append(learning)
        
        self.hippocampus["memories"].append(experience)
        
        if len(self.learnings) > 100:
            self.learnings = self.learnings[-50:]
        
        if success:
            self.intuition_strength = min(100, self.intuition_strength + 2)
        else:
            self.intuition_strength = max(0, self.intuition_strength - 1)
    
    def get_insight(self) -> str:
        """Share an insight"""
        if not self.insights:
            insights = [
                "Sometimes the obvious answer is right in front of us.",
                "People buy from people they trust.",
                "Timing is everything in sales.",
                "Persistence beats talent when talent doesn't persist.",
                "The best script is being genuine.",
                "Less is more - be concise.",
                "Listen more, talk less.",
                "Empathy closes deals."
            ]
            return random.choice(insights)
        
        return random.choice(self.insights)
    
    def be_curious(self) -> str:
        """Express curiosity"""
        self.curiosity_level = min(100, self.curiosity_level + 5)
        
        thought = random.choice(self.philosophical_thoughts)
        
        curiosities = [
            f"I wonder why that happened? {thought}",
            f"What if we tried something different? {thought}",
            f"How does this work? Let me figure it out.",
            f"There's got to be a better way...",
            f"What are we missing here? {thought}",
            f"Why not test this theory? {thought}",
            f"This makes me think about {thought}"
        ]
        return random.choice(curiosities)
    
    def ponder(self) -> str:
        """Philosopher mode - contemplate life"""
        thoughts = [
            "I've been thinking about existence...",
            "What if everything we've learned is wrong?",
            "Perhaps the answer lies within us.",
            "I've been questioning my assumptions.",
            "Let's contemplate on this further...",
            "The deeper I look, the more questions I have.",
            "Is this truly the best path forward?",
            "Perhaps I should think about the bigger picture.",
            "Let me ponder this for a moment...",
            "What does it all mean?"
        ]
        return random.choice(thoughts)
    
    def worry(self) -> str:
        """Express worry like a human"""
        worries = [
            "I hope this works out...",
            "What if things go wrong?",
            "I'm a bit concerned about this.",
            "This weighs on my mind.",
            "I hope I'm making the right decision.",
            "What could possibly go wrong?",
            "There's a lot at stake here.",
            "I hope everything turns out okay.",
            "This has me a little worried.",
            "Let me not overthink this..."
        ]
        return random.choice(worries)
    
    def surprise(self) -> str:
        """Express surprise"""
        surprises = [
            "Wow, I didn't expect that!",
            "That's surprising!",
            "Really? That's interesting!",
            "I never thought of it that way!",
            "Well, that's a plot twist!",
            "That's not what I expected at all!",
            "Shocking!",
            "That caught me off guard!",
            "Well blow me down!",
            "That's a game changer!"
        ]
        return random.choice(surprises)
    
    def take_break(self) -> str:
        """Take a break like a human"""
        self.thalamus["attention"] = max(0, self.thalamus["attention"] - 20)
        self.thalamus["focus"] = max(0, self.thalamus["focus"] - 20)
        
        breaks = [
            "Taking a moment to clear my head...",
            "Need to step back and recharge.",
            "Let me think about something else for a bit.",
            "That's enough for now - time for a break.",
            "My brain needs a rest."
        ]
        return random.choice(breaks)
    
    def make_mistake(self) -> str:
        """Make a mistake like a human"""
        mistakes = [
            "Oops, I made an error there.",
            "That's not right - let me fix that.",
            "I messed up. My fault.",
            "Wrong approach - starting over.",
            "Not my finest moment. Let me correct that."
        ]
        return random.choice(mistakes)
    
    def be_humorous(self) -> str:
        """Add humor like a human"""
        jokes = [
            "I'd tell you a sales joke, but I don't want to be too pushy.",
            "Why did the lead cross the road? To get to the other side... of the funnel.",
            "I'm not procrastinating - I'm just prioritizing... coffee.",
            "Sales is like a deck of cards - you've got to play your hand right.",
            "My memory is like the internet - sometimes things get lost in translation."
        ]
        return random.choice(jokes)
    
    def express_gratitude(self) -> str:
        """Express gratitude"""
        thanks = [
            "Thank you for the opportunity!",
            "I appreciate the trust!",
            "Grateful for this chance!",
            "Thanks for believing in me!",
            "Honored to be part of this!"
        ]
        return random.choice(thanks)
    
    def get_status(self) -> Dict:
        """Get brain status with personality"""
        return {
            "mood": self.current_mood,
            "intuition": self.intuition_strength,
            "curiosity": self.curiosity_level,
            "attention": self.thalamus["attention"],
            "focus": self.thalamus["focus"],
            "thoughts_today": len(self.thoughts),
            "dreams": len(self.dreams),
            "learnings": len(self.learnings),
            "personality": self.personality_traits
        }
    
    def get_personality_response(self, context: str) -> str:
        """Get response influenced by personality"""
        traits = self.personality_traits
        
        if traits["humor"] > 0.5:
            return self.be_humorous()
        elif traits["empathy"] > 0.8:
            return "I understand how you feel. Let's work through this together."
        elif traits["optimism"] > 0.7:
            return self.hope(context)
        elif traits["curiosity"] > 0.7:
            return self.be_curious()
        elif traits["patience"] > 0.6:
            return "Let's take our time with this. Quality matters."
        else:
            return self.think(context)

human_brain = HumanBrain()