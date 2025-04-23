import os
import sys

# Ensure project root (parent directory) is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test(name, fn):
    try:
        fn()
        print(f"✅ {name} import OK")
        return True
    except Exception as e:
        print(f"❌ {name} import FAILED:", e)
        return False

print("\n=== Testing Google ADK imports ===")
# 1. Google ADK core
test("google.adk.agents.Agent", lambda: __import__("google.adk.agents", fromlist=["Agent"]))
test("google.adk.tools.agent_tool.AgentTool", lambda: __import__("google.adk.tools.agent_tool", fromlist=["AgentTool"]))

print("\n=== Testing key utility imports ===")
# 2. Base support classes
test("python_adk.agents.base_agent.agent_tool", lambda: __import__("python_adk.agents.base_agent", fromlist=["agent_tool"]))
test("python_adk.agents.base_agent.annotate_type", lambda: __import__("python_adk.agents.base_agent", fromlist=["annotate_type"]))

print("\n=== Testing BatCucLinhSoAgent ===")
# 3. Domain agent (direct import)
if test("python_adk.agents.batcuclinh_so_agent.agent", lambda: __import__("python_adk.agents.batcuclinh_so_agent.agent")):
    from python_adk.agents.batcuclinh_so_agent.agent import BatCucLinhSoAgent
    
    # Create agent instance
    agent = BatCucLinhSoAgent()
    print(f"✅ Successfully created BatCucLinhSoAgent instance with name: {agent.name}")
    
    # Test agent methods
    result = agent.invoke("Test message")
    print(f"✅ Agent invoke method works: {result}") 