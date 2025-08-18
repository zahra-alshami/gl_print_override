import frappe
import json
from frappe.utils.print_format import report_to_pdf as _orig_report_to_pdf

@frappe.whitelist()
def report_to_pdf(*args, **kwargs):
    """
    Custom wrapper around frappe.utils.print_format.report_to_pdf
    to inject a custom HTML template for General Ledger.
    """
    clean_kwargs = dict(kwargs)

    if clean_kwargs.get("report_name") == "General Ledger":
        # Parse filters safely
        filters = {}
        if clean_kwargs.get("filters"):
            try:
                filters = (
                    json.loads(clean_kwargs["filters"])
                    if isinstance(clean_kwargs["filters"], str)
                    else clean_kwargs["filters"]
                )
            except Exception:
                filters = {}

        # Build context for Jinja template
        context = {
            **clean_kwargs,
            "filters": filters,   # ✅ now template sees "filters"
            "_": frappe._         # ✅ translation helper
        }

        clean_kwargs["html"] = frappe.render_template(
            "gl_print_override/templates/print_formats/gl_custom.html",
            context
        )

    # Return PDF bytes (Frappe will handle Response)
    return _orig_report_to_pdf(*args, **clean_kwargs)
