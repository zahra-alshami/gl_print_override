# gl_print_override/overrides/printing.py
import inspect
import frappe
from frappe.utils import print_format

# Keep reference to the original function
_orig_report_to_pdf = print_format.report_to_pdf

@frappe.whitelist()   
def report_to_pdf(*args, **kwargs):
    # Get the allowed parameters from the original function signature
    allowed_params = inspect.signature(_orig_report_to_pdf).parameters.keys()

    # Remove anything not in the original function signature
    clean_kwargs = {k: v for k, v in kwargs.items() if k in allowed_params}

    # 🔹 If you want to force your custom template:
    if clean_kwargs.get("report_name") == "General Ledger":
        clean_kwargs["html"] = frappe.render_template(
            "gl_print_override/templates/print_formats/gl_custom.html",
            clean_kwargs
        )

    return _orig_report_to_pdf(*args, **clean_kwargs)