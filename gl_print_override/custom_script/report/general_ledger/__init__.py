import frappe 
from gl_print_override.custom_script.report.general_ledger.general_ledger import execute as custom_general_ledger 
import erpnext.accounts.report.general_ledger.general_ledger 


# Replace the original execute function with your custom one 
erpnext.accounts.report.general_ledger.general_ledger.execute = custom_general_ledger

def custom_get_html(filters=None):
    custom_path = os.path.join(
        frappe.get_app_path("gl_print_override"),
        "templates",
        "general_ledger.html"
    )
    with open(custom_path, "r", encoding="utf-8") as f:
        template = f.read()

    jenv = frappe.get_jenv()
    return jenv.from_string(template).render({
        "filters": filters
    })

# Monkey patch
erpnext.accounts.report.general_ledger.general_ledger.get_html = custom_get_html
