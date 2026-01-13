// Copyright (c) 2025, Your Company and contributors
// For license information, please see license.txt

frappe.query_reports["My Dividend Report"] = {
	"filters": [
		{
			"fieldname": "fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year"
		},
        {
			"fieldname": "member_name",
			"label": __("Member Name"),
			"fieldtype": "Link",
			"options": "Investment Member",
		},
		{
			"fieldname": "dividend_rate",
			"label": __("Interest on Shares (%)"),
			"fieldtype": "Float"
		},
		{
			"fieldname": "interest_rate",
			"label": __("Interest on Deposit (%)"),
			"fieldtype": "Float"
		},
        {
			"fieldname": "withholding_tax_rate",
			"label": __("Withholding Tax Rate (%)"),
			"fieldtype": "Float"
		},
		{
			"fieldname": "processing_fee",
			"label": __("Processing Fee"),
			"fieldtype": "Currency"
		}
	],
	
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		
		// Right align currency columns
		if (column.fieldtype === "Currency" || column.fieldname.includes("deposit") || 
			column.fieldname.includes("capital") || column.fieldname.includes("dividend") || 
			column.fieldname.includes("interest") || column.fieldname.includes("fee") || 
			column.fieldname.includes("tax")) {
			if (value && value !== "0.00") {
				value = '<div style="text-align: right">' + value + '</div>';
			}
		}
		
		return value;
	},
	
	"onload": function(report) {
		// Add Export to CSV button
		report.page.add_inner_button(__('Export to CSV'), function() {
			const data = report.data;
			const columns = report.columns;
			
			if (!data || data.length === 0) {
				frappe.msgprint(__('No data to export'));
				return;
			}
			
			// Create CSV content
			let csv = [];
			
			// Add title row
			csv.push(['COMPUTATION OF DIVIDEND & INTEREST FY 2024']);
			csv.push([]);
			
			// Add headers
			let headers = columns.map(col => col.label || col.fieldname);
			csv.push(headers);
			
			// Add data rows
			data.forEach((row, index) => {
				let csv_row = columns.map(col => {
					let value = row[col.fieldname];
					if (value === null || value === undefined) {
						return '';
					}
					// Handle strings with commas
					if (typeof value === 'string' && value.includes(',')) {
						return '"' + value + '"';
					}
					return value;
				});
				csv.push(csv_row);
			});
			
			// Convert to CSV string
			let csv_content = csv.map(row => row.join(',')).join('\n');
			
			// Create download
			let blob = new Blob([csv_content], { type: 'text/csv;charset=utf-8;' });
			let link = document.createElement("a");
			let url = URL.createObjectURL(blob);
			link.setAttribute("href", url);
			link.setAttribute("download", "dividend_computation_" + frappe.datetime.now_date() + ".csv");
			link.style.visibility = 'hidden';
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
			
			frappe.msgprint(__('CSV file downloaded successfully'));
		}, __('Actions'));
		
		// Add Print button
		report.page.add_inner_button(__('Print'), function() {
			window.print();
		}, __('Actions'));
	}
};