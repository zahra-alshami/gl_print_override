import frappe
from frappe import _

def render_general_ledger_print_format(doc, print_format, **kwargs):
    # You can access report data here if needed, or get filters via kwargs

    # Load your custom template file
    template_path = frappe.get_app_path('gl_print_override', 'gl_print_override', 'templates', 'print_formats', 'general_ledger_print.html')
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Render the template with Jinja using frappe.render_template
    # Pass the 'doc' or 'kwargs' with the report data as context
    context = {
        "doc": doc,
        "filters": kwargs.get('filters', {}),
        # Add any other context variables you need here
    }
    html = frappe.render_template(template, context)

    return html
