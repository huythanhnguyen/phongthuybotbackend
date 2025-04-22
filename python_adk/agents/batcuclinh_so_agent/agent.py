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

    async def process_message(self, message: str) -> str:
        """
        Process a message and return a response
        
        Args:
            message: The message to process
            
        Returns:
            Response string
        """
        try:
            # Check if message contains phone number
            if any(char.isdigit() for char in message) and len(message) >= 10:
                # Try to extract phone number
                phone_number = ''.join(filter(str.isdigit, message))
                if len(phone_number) >= 10:
                    result = self.analyze_phone_number(phone_number)
                    return result.get("message", "Không thể phân tích số điện thoại")

            # Check if message contains CCCD number
            if any(char.isdigit() for char in message) and len(message) >= 12:
                # Try to extract CCCD number
                cccd_number = ''.join(filter(str.isdigit, message))
                if len(cccd_number) >= 12:
                    result = self.analyze_cccd_number(cccd_number)
                    return result.get("message", "Không thể phân tích số CCCD")

            # Default response if no analysis is possible
            return "Xin lỗi, tôi không thể phân tích thông tin bạn cung cấp. Vui lòng cung cấp số điện thoại hoặc số CCCD để phân tích."

        except Exception as e:
            return f"Đã xảy ra lỗi khi xử lý tin nhắn: {str(e)}"

    def analyze_phone_number(self, phone_number: str, purpose: Optional[str] = None) -> Dict[str, Any]:
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

            # Execute the analysis using func() directly - không cần await vì đây không phải là async function
            params = {
                "phone_number": phone_number
            }
            if purpose:
                params["purpose"] = purpose
                
            result = phone_analyzer.func(**params)

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

    def analyze_cccd_number(self, cccd_number: str, purpose: Optional[str] = None) -> Dict[str, Any]:
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

            # Execute the analysis using func() directly - không cần await vì đây không phải là async function
            params = {
                "cccd_number": cccd_number
            }
            if purpose:
                params["purpose"] = purpose
                
            result = cccd_analyzer.func(**params)

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