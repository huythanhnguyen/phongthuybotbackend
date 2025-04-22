import os
import js2py

# Load BAT_TINH constant from JS via js2py
_base_dir = os.path.abspath(os.path.dirname(__file__))
_js_path = os.path.join(_base_dir, '..', '..', 'constants', 'batTinh.js')
_ctx = js2py.EvalJs()
# Prepare module and exports
_ctx.execute('var module = {exports:{}}; var exports = module.exports;')
# Execute JS file
with open(_js_path, 'r', encoding='utf-8') as f:
    _ctx.execute(f.read())
# Convert to Python dict
BAT_TINH = _ctx.module.exports.to_dict() 