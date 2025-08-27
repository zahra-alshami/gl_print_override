frappe.query_reports["General Ledger"] = {
    onload: function(report) {
        console.log("✅ GL Print Override loaded");

        report.page.add_inner_button("Custom PDF", function() {
            frappe.call({
                method: "frappe.desk.query_report.download",
                args: {
                    report_name: "General Ledger",
                    file_format_type: "PDF",
                    filters: report.get_values(),
                    // 👇 force your custom print format
                    print_format: "Custom GL Print"
                },
                callback: function(r) {
                    if (!r.exc) {
                        // auto-download is handled by frappe, but just in case
                        frappe.msgprint("Downloaded with Custom Print Format!");
                    }
                }
            });
        });
    }
};
