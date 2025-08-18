import frappe
from frappe.utils.pdf import get_pdf
from frappe.utils.response import Response

@frappe.whitelist()
def report_to_pdf(*args, **kwargs):
    clean_kwargs = {k: v for k, v in kwargs.items() if k != "cmd"}

    # Custom override for General Ledger
    if clean_kwargs.get("report_name") == "General Ledger":
        html = frappe.render_template(
            "gl_print_override/templates/print_formats/gl_custom.html",
            clean_kwargs,
        )
        pdf_bytes = get_pdf(html)
    else:
        # Fallback – render normal HTML
        from frappe.www.printview import get_html
        html = get_html(**clean_kwargs)
        pdf_bytes = get_pdf(html)

    # ✅ return as proper HTTP Response
    return Response(
        filename=f"{clean_kwargs.get('report_name') or 'report'}.pdf",
        content_type="application/pdf",
        data=pdf_bytes
    )
