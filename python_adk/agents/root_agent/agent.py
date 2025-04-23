"""
Root Agent Implementation

Triển khai RootAgent - Agent chính điều phối các agent chuyên biệt.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig

from python_adk.prompt import get_agent_prompt
from python_adk.shared_libraries.logger import get_logger


class AgentType(str, Enum):
    """Các loại agent trong hệ thống"""
    ROOT = "root"
    BATCUCLINH_SO = "batcuclinh_so"
    PAYMENT = "payment"
    USER = "user"


# Import các sub-agents sau khi đã định nghĩa AgentType để tránh circular import
from python_adk.agents.batcuclinh_so_agent.agent import batcuclinh_so_agent
from python_adk.agents.payment_agent.agent import payment_agent
from python_adk.agents.user_agent.agent import user_agent


def _track_request(agent_state, user_input, agent_response):
    """Callback để theo dõi yêu cầu và phản hồi"""
    logger = get_logger("RootAgent")
    logger.info(f"Đã nhận yêu cầu: {user_input}")
    logger.info(f"Đã phản hồi: {agent_response}")
    
    # Thêm vào lịch sử hội thoại nếu cần
    if "conversation_history" not in agent_state:
        agent_state["conversation_history"] = []
    
    agent_state["conversation_history"].append({
        "role": "user",
        "content": user_input
    })
    
    agent_state["conversation_history"].append({
        "role": "assistant",
        "content": agent_response
    })
    
    return agent_state


root_agent = Agent(
    model="gemini-2.0-flash",
    name="root_agent",
    description="Agent chính điều phối các yêu cầu đến các agent chuyên biệt",
    instruction=get_agent_prompt(AgentType.ROOT),
    sub_agents=[
        batcuclinh_so_agent,
        payment_agent,
        user_agent,
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.2,
        top_p=0.8,
    ),
    after_agent_callback=_track_request,
) 