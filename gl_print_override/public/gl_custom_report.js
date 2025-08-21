frappe.query_reports["General Ledger"] = {
    "filters": [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.defaults.get_user_default("year_start"),
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.defaults.get_user_default("year_end"),
            reqd: 1
        },
        {
            fieldname: "party_name",
            label: __("Party"),
            fieldtype: "Link",
            options: "Party"
        }
    ],

    "formatter": function(value, row, column, data, default_formatter) {
        if (column.fieldname === "debit" && value > 0) {
            value = `<span style="color:green;font-weight:bold">${value}</span>`;
        }
        if (column.fieldname === "credit" && value > 0) {
            value = `<span style="color:red;font-weight:bold">${value}</span>`;
        }
        return default_formatter(value, row, column, data);
    }
};
