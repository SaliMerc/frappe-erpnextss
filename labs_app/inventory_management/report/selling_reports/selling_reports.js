// Copyright (c) 2025, Labs and contributors
// For license information, please see license.txt

frappe.query_reports["Selling Report"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer"
        },
        {
            "fieldname": "pos_profile",
            "label": __("POS Profile"),
            "fieldtype": "Link",
            "options": "POS Profile"
        },
        {
            "fieldname": "territory",
            "label": __("Territory"),
            "fieldtype": "Link",
            "options": "Territory"
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nDraft\nReturn\nCredit Note Issued\nSubmitted\nPaid\nPartly Paid\nUnpaid\nOverdue\nCancelled\nInternal Transfer"
        },
        {
            "fieldname": "pos_only",
            "label": __("POS Only"),
            "fieldtype": "Check",
            "default": 1
        },
        {
            "fieldname": "is_return",
            "label": __("Is Return"),
            "fieldtype": "Check"
        },
        {
            "fieldname": "chart_type",
            "label": __("Chart Type"),
            "fieldtype": "Select",
            "options": "Daily Sales\nPayment Mode\nTerritory",
            "default": "Daily Sales"
        }
    ],
    
    "formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        
        // Highlight returns in red
        if (column.fieldname == "is_return" && data && data.is_return == 1) {
            value = `<span style="color: red;">${value}</span>`;
        }
        
        // Highlight status
        if (column.fieldname == "status" && data) {
            if (data.status == "Paid") {
                value = `<span style="color: green; font-weight: bold;">${value}</span>`;
            } else if (data.status == "Overdue" || data.status == "Unpaid") {
                value = `<span style="color: red; font-weight: bold;">${value}</span>`;
            } else if (data.status == "Partly Paid") {
                value = `<span style="color: orange; font-weight: bold;">${value}</span>`;
            }
        }
        
        // Highlight grand total
        if (column.fieldname == "grand_total" && data) {
            if (data.is_return == 1) {
                value = `<span style="color: red; font-weight: bold;">${value}</span>`;
            } else {
                value = `<span style="font-weight: bold;">${value}</span>`;
            }
        }
        
        return value;
    },
    
    "onload": function(report) {
        // Add custom buttons
        report.page.add_inner_button(__("Refresh"), function() {
            report.refresh();
        });
        
        report.page.add_inner_button(__("Export"), function() {
            let filters = report.get_values();
            frappe.utils.csvExport(report, filters);
        }, __("Tools"));
    }
};