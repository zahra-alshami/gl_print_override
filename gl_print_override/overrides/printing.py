import frappe
from frappe.utils.pdf import get_pdf
@frappe.whitelist()
def report_to_pdf(*args, **kwargs):
    filters = kwargs.get("filters") or {}

    html = frappe.render_template(
        "gl_print_override/templates/print_formats/gl_custom.html",
        {
            "filters": filters,
            "_": frappe._
        }
    )

    pdf_bytes = get_pdf(html, options={"orientation": "Landscape"})
    return pdf_bytes
