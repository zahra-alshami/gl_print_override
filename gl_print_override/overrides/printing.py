import frappe
from frappe.utils.print_format import report_to_pdf as _orig_report_to_pdf
from frappe.utils.pdf import get_pdf

@frappe.whitelist()
def report_to_pdf(*args, **kwargs):
    # 🔹 Remove Frappe-injected junk params
    for bad_key in ("cmd", "method"):
        kwargs.pop(bad_key, None)

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

        # ✅ When called via HTTP, Frappe expects a Response
        if frappe.request:
            return frappe.response.build_response_as_stream(
                get_pdf(html, options={"orientation": "Landscape"}),
                "application/pdf",
                f"{report_name}.pdf"
            )

        # ✅ When called directly in console, just return bytes
        return get_pdf(html, options={"orientation": "Landscape"})

    # fallback: always sanitize kwargs before passing on
    return _orig_report_to_pdf(*args, **kwargs)
