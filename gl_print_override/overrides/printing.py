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

    # Extract "business" args (not needed by _orig_report_to_pdf)
    report_name = clean_kwargs.pop("report_name", None)
    filters = clean_kwargs.pop("filters", None)
    doctype = clean_kwargs.pop("doctype", None)
    name = clean_kwargs.pop("name", None)

    if report_name == "General Ledger":
        # Parse filters safely
        if filters:
            try:
                filters = json.loads(filters) if isinstance(filters, str) else filters
            except Exception:
                filters = {}
        else:
            filters = {}

        # Build context for Jinja
        context = {
            "doctype": doctype,
            "name": name,
            "filters": filters,
            "_": frappe._,
        }

        # Render HTML using your custom template
        clean_kwargs["html"] = frappe.render_template(
            "gl_print_override/templates/print_formats/gl_custom.html",
            context
        )

    # Now only pass safe kwargs to original PDF renderer
    return _orig_report_to_pdf(*args, **clean_kwargs)
