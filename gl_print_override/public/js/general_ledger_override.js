frappe.ui.form.on("GL Entry", {
    refresh(frm) {
        console.log("✅ GL Print Override JS loaded");
        // Example: override print button
        frm.page.set_primary_action("Custom Print", () => {
            frappe.call({
                method: "frappe.utils.print_format.report_to_pdf",
                args: {
                    html: "<h1>Custom PDF Content</h1>",
                    orientation: "Landscape"
                },
                callback: function(r) {
                    frappe.utils.downloadify(r.message, "custom_gl.pdf", "application/pdf");
                }
            });
        });
    }
});
