import inspect
import frappe
from frappe import whitelist
from frappe.utils import print_format

# Keep reference to original
_orig_report_to_pdf = print_format.report_to_pdf

@whitelist()   # ✅ Make it whitelisted
def report_to_pdf(*args, **kwargs):
    # Get the allowed parameters from the original function signature
    allowed_params = inspect.signature(_orig_report_to_pdf).parameters.keys()

    # Clean kwargs to only what original accepts
    clean_kwargs = {k: v for k, v in kwargs.items() if k in allowed_params}

    # 🔹 Inject custom HTML only for General Ledger
    if clean_kwargs.get("report_name") == "General Ledger":
        clean_kwargs["html"] = frappe.render_template(
            "gl_print_override/templates/print_formats/gl_custom.html",
            clean_kwargs
        )

    return _orig_report_to_pdf(*args, **clean_kwargs)
