#!/usr/bin/env python
"""
Convert JavaScript constant files to Python files for the Phong Thủy Số project
This script will read JavaScript constant files and convert them to Python constants
"""

import os
import re
import json

def js_to_py_value(value):
    """Convert JavaScript value literals to Python value literals"""
    if value == 'true':
        return 'True'
    elif value == 'false':
        return 'False'
    elif value == 'null':
        return 'None'
    return value

def js_object_to_py_dict(js_content):
    """
    Convert a JavaScript object to a Python dictionary string
    This is a simple conversion and may not handle all edge cases
    """
    # Remove comments
    js_content = re.sub(r'//.*', '', js_content)
    
    # Replace JS template literals with regular strings
    js_content = re.sub(r'`(.*?)`', r'"""\\1"""', js_content, flags=re.DOTALL)
    
    # Replace JavaScript object property syntax with Python dict syntax
    js_content = re.sub(r'(\w+)\s*:', r'"\1":', js_content)
    
    # Replace true/false/null with Python equivalents
    js_content = re.sub(r'\btrue\b', 'True', js_content)
    js_content = re.sub(r'\bfalse\b', 'False', js_content)
    js_content = re.sub(r'\bnull\b', 'None', js_content)
    
    return js_content

def convert_bat_tinh_js_to_py():
    """Convert batTinh.js to bat_tinh.py"""
    try:
        # Read the JavaScript file
        js_path = 'constants/batTinh.js'
        with open(js_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Extract the BAT_TINH object content
        match = re.search(r'const BAT_TINH = ({.*?});', js_content, re.DOTALL)
        if not match:
            print("Could not find BAT_TINH object in JS file")
            return
        
        bat_tinh_js = match.group(1)
        
        # Convert to Python
        bat_tinh_py = js_object_to_py_dict(bat_tinh_js)
        
        # Create Python file content
        py_content = f'''"""
Các hằng số Bát Tinh chuyển đổi từ batTinh.js sang Python
"""

# Định nghĩa trực tiếp BAT_TINH trong Python thay vì sử dụng js2py
BAT_TINH = {bat_tinh_py}
'''
        
        # Write to Python file
        py_path = 'python_adk/constants/bat_tinh.py'
        os.makedirs(os.path.dirname(py_path), exist_ok=True)
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(py_content)
        
        print(f"Successfully converted {js_path} to {py_path}")
    
    except Exception as e:
        print(f"Error converting batTinh.js: {e}")

def convert_digit_meanings_js_to_py():
    """Convert digitMeanings.js to digit_meanings.py"""
    try:
        # Read the JavaScript file
        js_path = 'constants/digitMeanings.js'
        with open(js_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Extract the digitMeanings object content
        match = re.search(r'const digitMeanings\s*=\s*({.*?});', js_content, re.DOTALL)
        if not match:
            print("Could not find digitMeanings object in JS file")
            return
        
        digit_meanings_js = match.group(1)
        
        # Convert to Python
        digit_meanings_py = js_object_to_py_dict(digit_meanings_js)
        
        # Create Python file content
        py_content = f'''"""
Các hằng số ý nghĩa các chữ số chuyển đổi từ digitMeanings.js sang Python
"""

# Định nghĩa trực tiếp DIGIT_MEANINGS trong Python thay vì sử dụng js2py
DIGIT_MEANINGS = {digit_meanings_py}
'''
        
        # Write to Python file
        py_path = 'python_adk/constants/digit_meanings.py'
        os.makedirs(os.path.dirname(py_path), exist_ok=True)
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(py_content)
        
        print(f"Successfully converted {js_path} to {py_path}")
    
    except Exception as e:
        print(f"Error converting digitMeanings.js: {e}")

def convert_response_factors_js_to_py():
    """Convert responseFactors.js to response_factors.py"""
    try:
        # Read the JavaScript file
        js_path = 'constants/responseFactors.js'
        with open(js_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Extract the responseFactors object content
        match = re.search(r'const responseFactors = ({.*?});', js_content, re.DOTALL)
        if not match:
            print("Could not find responseFactors object in JS file")
            return
        
        response_factors_js = match.group(1)
        
        # Convert to Python
        response_factors_py = js_object_to_py_dict(response_factors_js)
        
        # Create Python file content
        py_content = f'''"""
Các hệ số trọng số phân tích chuyển đổi từ responseFactors.js sang Python
"""

# Định nghĩa trực tiếp RESPONSE_FACTORS trong Python thay vì sử dụng js2py
RESPONSE_FACTORS = {response_factors_py}
'''
        
        # Write to Python file
        py_path = 'python_adk/constants/response_factors.py'
        os.makedirs(os.path.dirname(py_path), exist_ok=True)
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(py_content)
        
        print(f"Successfully converted {js_path} to {py_path}")
    
    except Exception as e:
        print(f"Error converting responseFactors.js: {e}")

def create_combinations_py():
    """Create combinations.py that loads from combinations.js using js2py"""
    try:
        py_content = '''import os
import js2py

# Load COMBINATION_INTERPRETATIONS constant from JS via js2py
_base_dir = os.path.abspath(os.path.dirname(__file__))
_js_path = os.path.join(_base_dir, '..', '..', 'constants', 'combinations.js')
_ctx = js2py.EvalJs()
# Prepare module and exports
_ctx.execute('var module = {exports:{}}; var exports = module.exports;')
# Execute JS file
with open(_js_path, 'r', encoding='utf-8') as f:
    _ctx.execute(f.read())
# Convert to Python dict
COMBINATIONS = _ctx.module.exports.to_dict()
'''
        
        # Write to Python file
        py_path = 'python_adk/constants/combinations.py'
        os.makedirs(os.path.dirname(py_path), exist_ok=True)
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(py_content)
        
        print(f"Successfully created {py_path}")
    
    except Exception as e:
        print(f"Error creating combinations.py: {e}")

if __name__ == "__main__":
    print("Starting conversion of JavaScript constants to Python...")
    convert_bat_tinh_js_to_py()
    convert_digit_meanings_js_to_py()
    convert_response_factors_js_to_py()
    create_combinations_py()
    print("Conversion complete.") 