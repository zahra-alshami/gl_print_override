import frappe
from frappe.utils.print_format import report_to_pdf as _orig_report_to_pdf

@frappe.whitelist()
def report_to_pdf(*args, **kwargs):
    """
    Custom wrapper around frappe.utils.print_format.report_to_pdf
    to inject a custom HTML template for General Ledger.
    """
    clean_kwargs = dict(kwargs)

    if clean_kwargs.get("report_name") == "General Ledger":
        context = {**clean_kwargs, "_": frappe._}  # ✅ add translation helper
        clean_kwargs["html"] = frappe.render_template(
            "gl_print_override/templates/print_formats/gl_custom.html",
            context
        )

    # ✅ returns raw PDF bytes, Frappe will wrap it into Response automatically
    return _orig_report_to_pdf(*args, **clean_kwargs)
