"""
Agent for analyzing phone numbers and CCCD numbers using Bát Cục Linh Số method
"""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from typing import Dict, Any, List, Optional

class BatCucLinhSoAgent(LlmAgent):
    def __init__(
        self,
        name: str = "bat_cuc_linh_so_agent",
        description: str = "Agent for analyzing phone numbers and CCCD numbers using Bát Cục Linh Số method",
        tools: Optional[List[FunctionTool]] = None,
    ):
        super().__init__(
            name=name,
            description=description,
            tools=tools or []
        )

    async def analyze_phone_number(self, phone_number: str, purpose: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze a phone number using Bát Cục Linh Số method
        
        Args:
            phone_number: The phone number to analyze
            purpose: Optional purpose for the analysis
            
        Returns:
            Dict containing analysis results
        """
        try:
            # Get the phone analyzer tool
            phone_analyzer = next((tool for tool in self.tools if tool.name == "phone_analyzer"), None)
            if not phone_analyzer:
                raise ValueError("Phone analyzer tool not found")

            # Execute the analysis
            result = await phone_analyzer.execute({
                "phone_number": phone_number,
                "purpose": purpose
            })

            return {
                "success": True,
                "message": "Phone number analysis completed successfully",
                "analysis": result
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error analyzing phone number: {str(e)}",
                "analysis": None
            }

    async def analyze_cccd_number(self, cccd_number: str, purpose: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze a CCCD number using Bát Cục Linh Số method
        
        Args:
            cccd_number: The CCCD number to analyze
            purpose: Optional purpose for the analysis
            
        Returns:
            Dict containing analysis results
        """
        try:
            # Get the CCCD analyzer tool
            cccd_analyzer = next((tool for tool in self.tools if tool.name == "cccd_analyzer"), None)
            if not cccd_analyzer:
                raise ValueError("CCCD analyzer tool not found")

            # Execute the analysis
            result = await cccd_analyzer.execute({
                "cccd_number": cccd_number,
                "purpose": purpose
            })

            return {
                "success": True,
                "message": "CCCD number analysis completed successfully",
                "analysis": result
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error analyzing CCCD number: {str(e)}",
                "analysis": None
            }