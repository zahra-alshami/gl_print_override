import frappe
from frappe.utils.print_format import report_to_pdf as original_report_to_pdf

@frappe.whitelist()
def report_to_pdf():
    frappe.logger().info("overriding general ledger")
# def custom_report_to_pdf(html, orientation="Landscape"):
    # 👇 detect if it's the General Ledger report
    # if "General Ledger" in html:
    #     # You can even inject a custom print format or manipulate HTML here
    #     frappe.logger().info("🔄 Overriding General Ledger PDF generation")
    #     # example: replace a title
    #     html = html.replace("General Ledger", "Custom GL Report")

#     return original_report_to_pdf(html, orientation)

# def apply_patch(*args, **kwargs):
#     frappe.logger().info("llllllllll")
#     frappe.utils.print_format.report_to_pdf = custom_report_to_pdf
