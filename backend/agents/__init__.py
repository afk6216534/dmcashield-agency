"""
DMCAShield Agency - All 12 Departments Integrated
This file wires together all agents into the autonomous system.
"""

from agents.departments.scraping.data_hunter_1 import DataHunter1
from agents.departments.scraping.data_hunter_2 import DataHunter2
from agents.departments.scraping.data_hunter_3 import DataHunter3
from agents.departments.scraping.verifier_agent import VerifierAgent

from agents.departments.validation.validator_agent import ValidatorAgent
from agents.departments.validation.competitor_spy_agent import CompetitorSpyAgent
from agents.departments.validation.audience_analyst_agent import AudienceAnalystAgent

from agents.departments.marketing.intelligence.intel_head import IntelHeadAgent as IntelHead
from agents.departments.marketing.funnel.funnel_head import FunnelHeadAgent as FunnelHead
from agents.departments.marketing.copy_head.copy_writer import CopyWriter
from agents.departments.marketing.copy_head.qa_head import QAHead
from agents.departments.marketing.competitor_head import CompetitorHead

from agents.departments.email_sending.send_head import SendHead

from agents.departments.tracking.open_tracker import OpenTracker
from agents.departments.tracking.click_tracker import ClickTracker
from agents.departments.tracking.insight_bot import InsightBot
from agents.departments.tracking.report_gen import ReportGen

from agents.departments.sales.reply_reader import ReplyReader
from agents.departments.sales.human_voice import HumanVoice

from agents.departments.sheets.sheet_bot import SheetBot

from agents.departments.accounts.warmup_bot import WarmupBot

from agents.departments.tasks.task_head import TaskTracker

from agents.departments.ml.pattern_finder import PatternFinder
from agents.departments.ml.model_trainer import ModelTrainer

from agents.departments.jarvis.jarvis_core import JARVISCore

from agents.departments.memory.soul import Soul, get_soul

__all__ = [
    'DataHunter1', 'DataHunter2', 'DataHunter3', 'VerifierAgent',
    'ValidatorAgent', 'CompetitorSpyAgent', 'AudienceAnalystAgent',
    'IntelHead', 'FunnelHead', 'CopyWriter', 'QAHead', 'CompetitorHead',
    'SendHead',
    'OpenTracker', 'ClickTracker', 'InsightBot', 'ReportGen',
    'ReplyReader', 'HumanVoice',
    'SheetBot',
    'WarmupBot',
    'TaskTracker',
    'PatternFinder', 'ModelTrainer',
    'JARVISCore',
    'Soul', 'get_soul'
]
