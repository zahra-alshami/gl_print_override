import json
import frappe
from frappe.utils.pdf import get_pdf
from frappe.utils.print_format import report_to_pdf as _orig_report_to_pdf

TARGET_REPORTS = {"General Ledger"}  # Name as it appears in the report list

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
def report_to_pdf(*args, **kwargs):
    """Override GL PDF generation."""
    # Merge both styles of passing params (frappe.form_dict + kwargs)
    params = frappe._dict(frappe.form_dict or {})
    params.update(kwargs or {})

    report_name = params.get("report_name")
    filters = _parse_filters(params.get("filters"))
    orientation = params.get("orientation") or "Landscape"

    if report_name not in TARGET_REPORTS:
        # Not GL → pass all original params along
        return _orig_report_to_pdf(*args, **params)

    # Run the original GL query
    result = frappe.get_attr("frappe.desk.query_report.run")(report_name, filters=filters)
    columns = result.get("columns") or []
    data    = result.get("result") or []

    # Render with custom template
    html = frappe.render_template(
        "gl_print_override/templates/print_formats/gl_custom.html",
        {
            "columns": columns,
            "data": data,
            "filters": filters,
            "report": {"name": report_name},
        },
    )

    # Return PDF to browser
    frappe.local.response.filename = f"{frappe.scrub(report_name)}.pdf"
    frappe.local.response.filecontent = get_pdf(html, {"orientation": orientation})
    frappe.local.response.type = "download"
