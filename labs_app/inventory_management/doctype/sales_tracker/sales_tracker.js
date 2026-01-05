// Copyright (c) 2025, Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Tracker Item', {
	// Trigger when a new row is added to the items table
	items_add: function(frm) {
		call_calculate(frm);
	},

	// Trigger when a relevant field in the child row changes
	// Using your fieldnames: quantity, rate, discount_percentage, amount
	quantity: function(frm) {
		call_calculate(frm);
	},
	rate: function(frm) {
		call_calculate(frm);
	},
	discount_percentage: function(frm) {
		call_calculate(frm);
	},
	amount: function(frm) {
		call_calculate(frm);
	},

	// Trigger when a row is removed
	items_remove: function(frm) {
		call_calculate(frm);
	}
});

// Helper function to collect minimal payload and call server calculation
function call_calculate(frm) {
	try {
		const items_payload = (frm.doc.items || []).map(
            r => ({
			idx: r.idx,
			name: r.name,
			quantity: r.quantity,
			rate: r.rate,
			discount_percentage: r.discount_percentage,
			amount: r.amount
		}));

		// total_amount computed client-side for quick usage (optional)
		let total_amount = 0;
		items_payload.forEach(it => {
			total_amount += (parseFloat(it.amount) || 0);
		});

		const discount_value = frm.doc.discount_amount || 0;

		frappe.call({
			method: 'labs_app.inventory_management.doctype.sales_tracker.sales_tracker.calculate_amounts',
			args: {
				items: items_payload,
				discount_amount: discount_value
			},
			callback: function(r) {
				if (r.message) {
					// apply server result: set total_amount fields
					if (r.message.total_amount !== undefined) {
						frm.set_value('total_amount', r.message.total_amount);
					}

					// update child row amounts using frappe.model.set_value to ensure UI updates
					if (r.message.items && Array.isArray(r.message.items)) {
						r.message.items.forEach(it => {
							// find matching row by name or idx
							const row = frm.doc.items.find(r => (r.name && r.name === it.idx) || r.idx === it.idx || r.name === it.name);
							if (row) {
								try {
									if (row.doctype && row.name) {
										frappe.model.set_value(row.doctype, row.name, 'amount', it.amount);
									} else {
										row.amount = it.amount;
									}
								} catch (e) {
									row.amount = it.amount;
								}
							}
						});
						frm.refresh_field('items');
					}
				}
			}
		});
	} catch (e) {
		console.error('call_calculate error', e);
	}
}

