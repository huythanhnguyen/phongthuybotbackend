"""
Root Agent Implementation using direct GeminiAgent initialization.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Set, Type, Union

# Google ADK imports
from google.adk.agents import Agent as GeminiAgent
# from google.adk.tools.agent_tool import AgentTool # Removed as AgentRouter is removed
from google.genai.types import GenerateContentConfig

# Import Tools (excluding AgentRouter)
from python_adk.agents.root_agent.tools.intent_classifier import IntentClassifier
# from python_adk.agents.root_agent.tools.agent_router import AgentRouter # Removed
from python_adk.agents.root_agent.tools.context_tracker import ContextTracker
from python_adk.agents.root_agent.tools.conversation_manager import ConversationManager

# Import AgentType from the new module
from python_adk.agents.agent_types import AgentType

# Import Sub-Agents
from python_adk.agents.batcuclinh_so_agent import BatCucLinhSoAgent
from python_adk.agents.payment_agent import PaymentAgent
from python_adk.agents.user_agent import UserAgent

# Logger and Prompt
from python_adk.shared_libraries.logger import get_logger
from python_adk.prompt import get_agent_prompt


class AgentType(str, Enum):
    """Các loại agent trong hệ thống"""
    ROOT = "root"
    BATCUCLINH_SO = "batcuclinh_so"
    PAYMENT = "payment"
    USER = "user"

# --- Initialize Tools ---
intent_classifier_tool = IntentClassifier()
context_tracker_tool = ContextTracker()
conversation_manager_tool = ConversationManager()

# List of tools for the Root Agent
root_agent_tools = [
    intent_classifier_tool,
    context_tracker_tool,
    conversation_manager_tool
]

# --- Initialize Sub-Agents ---
# Assuming sub-agents don't need specific model overrides here
# and will use their default defined models.
bat_cuc_linh_so_agent = BatCucLinhSoAgent()
payment_agent = PaymentAgent()
user_agent = UserAgent()

# List of sub-agents for the Root Agent
root_agent_sub_agents = [
    bat_cuc_linh_so_agent,
    payment_agent,
    user_agent
]

# --- Agent Configuration ---
ROOT_AGENT_NAME = "root_agent"
MODEL_NAME = "gemini-2.0-flash"
ROOT_AGENT_INSTRUCTION = get_agent_prompt(AgentType.ROOT)
ROOT_AGENT_CONFIG = GenerateContentConfig(
    temperature=0.2,
    top_p=0.8,
)

# Get logger
logger = get_logger(f"{ROOT_AGENT_NAME}_agent", log_to_file=True)

# --- Create Root Agent Instance directly ---
logger.info(f"Khởi tạo {ROOT_AGENT_NAME} với model {MODEL_NAME}, {len(root_agent_tools)} tools, và {len(root_agent_sub_agents)} sub-agents")
root_agent = GeminiAgent(
    name=ROOT_AGENT_NAME,
    model=MODEL_NAME,
    instruction=ROOT_AGENT_INSTRUCTION,
    tools=root_agent_tools,
    sub_agents=root_agent_sub_agents,
    generate_content_config=ROOT_AGENT_CONFIG,
    # after_agent_callback is removed for simplicity, rely on ADK history
    # sub_agents can be added here if they are imported or later via root_agent.sub_agents = [...]
)
logger.info(f"{ROOT_AGENT_NAME} initialized successfully.") 