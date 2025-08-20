import frappe
from frappe.utils.print_format import report_to_pdf as _orig_report_to_pdf

def report_to_pdf(*args, **kwargs):
    """Override for GL report PDF export"""

    report_name = kwargs.get("report_name")
    filters = kwargs.get("filters") or {}

    if report_name == "General Ledger":
        # ✅ build custom HTML
        context = {
            "filters": filters,
            "_": frappe._  # for translations
        }
        html = frappe.render_template(
            "gl_print_override/templates/print_formats/gl_custom.html",
            context
        )
        orientation = kwargs.get("orientation", "Landscape")
        return _orig_report_to_pdf(html, orientation=orientation)

    # fallback to normal path
    return _orig_report_to_pdf(kwargs.get("html"), orientation=kwargs.get("orientation", "Landscape"))
