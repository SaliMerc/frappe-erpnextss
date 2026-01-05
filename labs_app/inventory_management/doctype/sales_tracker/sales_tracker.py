# Copyright (c) 2025, Labs and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.utils import flt
from frappe.model.document import Document


class SalesTracker(Document):
	pass

@frappe.whitelist()
def calculate_amounts(items):
	# Accept JSON string
	if isinstance(items, str):
		try:
			items = json.loads(items)
		except Exception:
			items = []

	result_items = []
	total = 0.0

	for item in items or []:
		try:
			qty = flt(item.get("quantity")) or 0
			rate = flt(item.get("rate")) or 0
			disc_pct = flt(item.get("discount_percentage")) or 0

			base = qty * rate
			disc_amt = (base * disc_pct) / 100
			amt = base - disc_amt

			# Round to 2 decimals for currency fields
			amt = round(amt, 2)

			result_items.append({
				"idx": item.get("idx"),
				"name": item.get("name"),
				"amount": amt
			})

			total += amt
		except Exception as e:
			frappe.log_error(f"Error calculating line for item {item}: {str(e)}", "Sales Tracker")

	total = round(total, 2)

	return {"items": result_items, "total_amount": total}

