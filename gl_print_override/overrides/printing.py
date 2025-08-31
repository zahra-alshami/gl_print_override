import frappe
from frappe.utils.pdf import get_pdf
from frappe.utils.print_format import report_to_pdf as _orig_report_to_pdf

@frappe.whitelist()
def report_to_pdf(*args, **kwargs):
    report_name = kwargs.get("report_name")
    filters = kwargs.get("filters", {})

    if report_name == "General Ledger":
        context = {
            "filters": filters,
            "_": frappe._  # translation context
        }

        html = frappe.render_template(
            "<h1>hello world</h1>",
            context
        )

        pdf_bytes = get_pdf(html, options={"orientation": "Landscape"})

        if hasattr(frappe.local, "request") and frappe.local.request:
            frappe.local.response.filename = "general_ledger.pdf"
            frappe.local.response.filecontent = pdf_bytes
            frappe.local.response.type = "download"
            return

        return pdf_bytes

    # fallback to original logic
    return _orig_report_to_pdf(*args, **kwargs)