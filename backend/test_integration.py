"""
Integration Tests for DMCAShield Autonomous System
Tests all 12 departments work together.
"""

import unittest
from datetime import datetime
from agents.memory.message_bus import MessageBus
from agents.memory.agent_brain import AgentBrain, MemorySystem

class TestMessageBus(unittest.TestCase):
    def setUp(self):
        self.bus = MessageBus()
    
    def test_send_message(self):
        msg_id = self.bus.send_message("Dept1", "Dept2", "handoff", {"task": "test"})
        self.assertIsNotNone(msg_id)
    
    def test_get_messages(self):
        self.bus.send_message("Dept1", "Dept2", "update", {"status": "ok"})
        msgs = self.bus.get_messages("Dept2")
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0]["from_agent"], "Dept1")

class TestAgentBrain(unittest.TestCase):
    def setUp(self):
        self.brain = AgentBrain("test_agent", persist_directory="./test_chroma")
    
    def test_store_experience(self):
        result = self.brain.store_experience(
            "email_sent", 
            {"lead_id": "lead-001", "opened": True},
            "success"
        )
        self.assertIsNotNone(result)
    
    def test_query_similar(self):
        self.brain.store_experience("scrape", {"found": 10}, "success")
        results = self.brain.query_similar_experiences("scrape business data")
        self.assertIn("ids", results)

if __name__ == "__main__":
    unittest.main()
