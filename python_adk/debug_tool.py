"""
Debug file to inspect FunctionTool class
"""

from google.adk.tools import FunctionTool
import inspect

def debug_function_tool():
    print("Debugging FunctionTool class:")
    print("==========================")
    
    # Print the class and module info
    print("FunctionTool class:", FunctionTool)
    print("FunctionTool module:", FunctionTool.__module__)
    
    # Print the signature
    print("FunctionTool signature:", inspect.signature(FunctionTool.__init__))
    
    # Print the source code if available
    try:
        print("FunctionTool source:")
        print(inspect.getsource(FunctionTool.__init__))
    except Exception as e:
        print("Could not get source:", e)
    
    # Print the docstring
    print("FunctionTool docstring:")
    print(FunctionTool.__doc__)
    
    # Try to create a simple tool
    try:
        def dummy_function(x: int) -> int:
            """Test function that doubles a number."""
            return x * 2
        
        # Try different ways to create the tool
        print("Testing different creation methods:")
        
        try:
            print("Method 1: FunctionTool(function=fn, description=desc)")
            tool1 = FunctionTool(function=dummy_function, description="Test function")
            print("Success! Created tool:", tool1)
        except Exception as e:
            print("Failed:", e)
            
        try:
            print("Method 2: FunctionTool(dummy_function, 'Test function')")
            tool2 = FunctionTool(dummy_function, "Test function")
            print("Success! Created tool:", tool2)
        except Exception as e:
            print("Failed:", e)
            
        try:
            print("Method 3: FunctionTool.create(dummy_function, 'Test function')")
            tool3 = FunctionTool.create(dummy_function, "Test function")
            print("Success! Created tool:", tool3)
        except Exception as e:
            print("Failed:", e)
        
        # Try to create a tool with just the function
        try:
            print("Method 4: FunctionTool(dummy_function)")
            tool4 = FunctionTool(dummy_function)
            print("Success! Created tool:", tool4)
            print("Tool4 name:", tool4.name)
            print("Tool4 description:", tool4.description)
            
            # Try to execute the tool
            try:
                print("Executing tool4 with x=5:")
                result = tool4.func(5)
                print("Result:", result)
            except Exception as e:
                print("Failed to execute:", e)
                
        except Exception as e:
            print("Failed:", e)
            
    except Exception as e:
        print("Error testing tool creation:", e)

    # Try to import and test phone_analyzer_tool
    try:
        from python_adk.agents.batcuclinh_so_agent.tools.phone_analyzer import phone_analyzer_tool, phone_analyzer
        print("\nTesting phone_analyzer_tool:")
        print("phone_analyzer_tool:", phone_analyzer_tool)
        print("phone_analyzer_tool.name:", getattr(phone_analyzer_tool, 'name', 'N/A'))
        print("phone_analyzer_tool.description:", getattr(phone_analyzer_tool, 'description', 'N/A'))
        print("phone_analyzer_tool.func:", getattr(phone_analyzer_tool, 'func', 'N/A'))
        
        try:
            print("\nTesting phone_analyzer function directly:")
            result = phone_analyzer("0123456789")
            print("Success! Result:", result.keys())
        except Exception as e:
            print("Failed to execute phone_analyzer:", e)
            
    except Exception as e:
        print("Error testing phone_analyzer_tool:", e)
    
if __name__ == "__main__":
    debug_function_tool() 