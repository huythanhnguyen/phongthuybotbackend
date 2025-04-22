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
            
    except Exception as e:
        print("Error testing tool creation:", e)
    
if __name__ == "__main__":
    debug_function_tool() 