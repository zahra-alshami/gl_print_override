import frappe
from frappe.utils.pdf import get_pdf
from frappe.utils.print_format import report_to_pdf as _orig_report_to_pdf

@frappe.whitelist()
def report_to_pdf(*args, **kwargs):
    clean_kwargs = {k: v for k, v in kwargs.items() if k != "cmd"}

    # Custom override for GL
    if clean_kwargs.get("report_name") == "General Ledger":
        html = frappe.render_template(
            "gl_print_override/templates/print_formats/gl_custom.html",
            clean_kwargs,
        )
        return get_pdf(html)   # ✅ always bytes

    # For all other reports
    if "html" not in clean_kwargs:
        from frappe.www.printview import get_html
        html = get_html(**clean_kwargs)
    else:
        html = clean_kwargs["html"]

    return get_pdf(html)   # ✅ always bytes
