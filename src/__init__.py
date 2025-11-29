"""
Kasparro Agentic FB Analyst - Main Package

A multi-agent system for Facebook Ads performance analysis.
"""

__version__ = '1.0.0'
__author__ = 'Harikrishna Choppa'
__email__ = 'harikrishna.choppa@example.com'

from .agents import *
from .orchestrator import Orchestrator
from .utils import *

__all__ = [
    'PlannerAgent',
    'DataAgent',
    'InsightAgent',
    'EvaluatorAgent',
    'CreativeAgent',
    'Orchestrator'
]
