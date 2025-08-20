import frappe
from frappe.utils.print_format import report_to_pdf as _orig_report_to_pdf
from frappe.utils.pdf import get_pdf

def report_to_pdf(*args, **kwargs):
    report_name = kwargs.get("report_name")
    filters = kwargs.get("filters") or {}

    if report_name == "General Ledger":
        context = {
            "filters": filters,
            "_": frappe._,
        }
        html = frappe.render_template(
            "gl_print_override/templates/print_formats/gl_custom.html",
            context
        )
        # ✅ UI expects Response (not raw bytes)
        return frappe.response.build_response_as_stream(
            get_pdf(html, options={"orientation": "Landscape"}),
            "application/pdf",
            f"{report_name}.pdf"
        )

    # fallback for all other reports
    return _orig_report_to_pdf(*args, **kwargs)
