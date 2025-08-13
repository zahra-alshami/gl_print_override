import json
import frappe
from frappe.utils.pdf import get_pdf
from frappe.utils.print_format import report_to_pdf as _orig_report_to_pdf

TARGET_REPORTS = {"General Ledger"}  # Modify if your GL report has a different name

def _parse_filters(filters):
    if not filters:
        return {}
    if isinstance(filters, dict):
        return filters
    try:
        return frappe.parse_json(filters) or {}
    except Exception:
        try:
            return json.loads(filters)
        except Exception:
            return {}

@frappe.whitelist()
def report_to_pdf(**kwargs):
    """Override for GL PDF generation."""
    form = frappe.form_dict or {}
    report_name = kwargs.get("report_name") or form.get("report_name")
    filters     = _parse_filters(kwargs.get("filters") or form.get("filters"))
    orientation = (kwargs.get("orientation") or form.get("orientation") or "Landscape")

    if report_name not in TARGET_REPORTS:
        return _orig_report_to_pdf(**kwargs)

    # Run the original GL report
    result = frappe.get_attr("frappe.desk.query_report.run")(report_name, filters=filters)
    columns = result.get("columns") or []
    data    = result.get("result") or []

    # Render with custom Jinja template
    html = frappe.render_template(
        "gl_print_override/templates/print_formats/gl_custom.html",
        {
            "columns": columns,
            "data": data,
            "filters": filters,
            "report": {"name": report_name},
        },
    )

    # Stream the PDF
    frappe.local.response.filename = f"{frappe.scrub(report_name)}.pdf"
    frappe.local.response.filecontent = get_pdf(html, {"orientation": orientation})
    frappe.local.response.type = "download"
