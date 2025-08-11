# apps/<your_app>/<your_app>/erpnext/accounts/report/general_ledger/general_ledger.py
# This shim makes this app "own" the module path, but delegates to the original ERPNext code.
import importlib.machinery
import importlib.util
import sys
import frappe
from pathlib import Path

# locate the original ERPNext file by full path (avoids importing via package name)
orig_path = frappe.get_app_path(
    "erpnext", "accounts", "report", "general_ledger", "general_ledger.py"
)
orig_path = Path(orig_path).resolve()

# load original module under a safe alias to avoid name collision / recursion
loader = importlib.machinery.SourceFileLoader("erpnext_original_general_ledger", str(orig_path))
spec = importlib.util.spec_from_loader(loader.name, loader)
original = importlib.util.module_from_spec(spec)
loader.exec_module(original)

# expose the same entrypoints as the original module (e.g., execute)
# so when Frappe imports erpnext.accounts.report.general_ledger.general_ledger,
# it will get this module and call execute(), which delegates to original.execute
try:
    execute = original.execute
except AttributeError:
    # fallback: try to get other names if needed
    raise

# optionally re-expose other attributes you might need (get_columns, etc.)
for attr in ("get_columns", "get_data",):
    if hasattr(original, attr):
        globals()[attr] = getattr(original, attr)
