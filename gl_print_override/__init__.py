# import frappe
from gl_print_overrid.overrides.printing import report_to_pdf
frappe.utils.print_format.report_to_pdf = report_to_pdf
