# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	"""Main execution function for the report"""
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	"""Define all report columns"""
	return [
		{
			"fieldname": "member_number",
			"label": _("No"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "member_name",
			"label": _("Name"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "current_deposit",
			"label": _("Current Deposit"),
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "share_capital",
			"label": _("Shares Capital"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "qualifying_current_deposits",
			"label": _("Qualifying Current Deposits"),
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"fieldname": "qualifying_shares_retained",
			"label": _("Qualifying Shares Retained"),
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"fieldname": "explanation",
			"label": _("Explanation"),
			"fieldtype": "Data",
			"width": 300
		},
		{
			"fieldname": "gross_dividends",
			"label": _("Gross Dividends. 7% of share capital"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "gross_interest_on_deposit",
			"label": _("Gross Interest on Deposit. 6%"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "processing_fee",
			"label": _("Processing Fee"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "withholding_tax",
			"label": _("Withholding tax 5%"),
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "net_dividends",
			"label": _("Net Dividends"),
			"fieldtype": "Currency",
			"width": 130
		}
	]


def get_data(filters=None):
	"""Fetch and calculate dividend data"""
	
	if not filters:
		filters = frappe._dict()
	
	# Get filter values with defaults
	dividend_rate = flt(filters.get("dividend_rate")) 
	interest_rate = flt(filters.get("interest_rate")) 
	processing_fee = flt(filters.get("processing_fee"))
	withholding_tax_rate = flt(filters.get("withholding_tax_rate"))
	
	# Build WHERE conditions
	conditions = ["1=1"]
	
	# if filters.get("member_name"):
	# 	conditions.append(f"member_name = %(member_name)s")
	
	
	where_clause = " AND ".join(conditions)
	
	# Fetch member data from Dividend Calculator Detail
	query = f"""
		SELECT 
			member_number,
			member_name,
			COALESCE(current_deposit, 0) as current_deposit,
			COALESCE(share_capital, 0) as share_capital,
			COALESCE(qualifying_current_deposits, 0) as qualifying_current_deposits,
			COALESCE(qualifying_shares_retained, 0) as qualifying_shares_retained,
			qualifying_deposit_explanation,
			qualifying_share_explanation
		FROM 
			`tabDividend Calculator Detail`
		WHERE
			{where_clause}
		ORDER BY 
			member_number
	"""
	
	members = frappe.db.sql(query, filters, as_dict=1)
	
	# Calculate dividends for each member
	data = []
	for member in members:
		# Get values
		share_capital = flt(member.share_capital)
		qualifying_deposits = flt(member.qualifying_current_deposits)
		
		# Calculate gross dividends (based on share capital)
		gross_dividends = share_capital * dividend_rate
		
		# Calculate gross interest (based on qualifying deposits)
		gross_interest = qualifying_deposits * interest_rate
		
		# Calculate total gross income
		total_gross = gross_dividends + gross_interest
		
		# Calculate withholding tax (5% of total gross)
		withholding_tax = total_gross * withholding_tax_rate
		
		# Calculate net dividends
		net_dividends = total_gross - withholding_tax - processing_fee
		
		# Prepare combined explanation
		explanation = get_combined_explanation(
			member.current_deposit, 
			member.qualifying_current_deposits,
			member.share_capital,
			member.qualifying_shares_retained,
			member.get("qualifying_deposit_explanation"),
			member.get("qualifying_share_explanation")
		)
		
		# Append row
		data.append({
			"member_number": member.member_number,
			"member_name": member.member_name,
			"current_deposit": flt(member.current_deposit, 2),
			"share_capital": flt(share_capital, 2),
			"qualifying_current_deposits": flt(qualifying_deposits, 2),
			"qualifying_shares_retained": flt(member.qualifying_shares_retained, 2),
			"explanation": explanation,
			"gross_dividends": flt(gross_dividends, 2),
			"gross_interest_on_deposit": flt(gross_interest, 2),
			"processing_fee": flt(processing_fee, 2),
			"withholding_tax": flt(withholding_tax, 2),
			"net_dividends": flt(net_dividends, 2)
		})
	
	return data


def get_combined_explanation(current_deposit, qualifying_deposit, share_capital, qualifying_shares, 
							  deposit_explanation_text=None, share_explanation_text=None):
	"""Generate combined explanation for both qualifying deposits and shares"""
	
	# If custom explanations exist in the doctype, use them
	if deposit_explanation_text and share_explanation_text:
		return f"{deposit_explanation_text}; {share_explanation_text}"
	
	# Otherwise, generate automatic explanation
	explanations = []
	
	# Deposit explanation
	current = flt(current_deposit)
	qualifying_dep = flt(qualifying_deposit)
	
	if current == qualifying_dep and current > 0:
		explanations.append("Full deposit qualifies")
	elif qualifying_dep == 0 and current > 0:
		explanations.append("No qualifying deposits")
	elif qualifying_dep > 0:
		explanations.append(f"Deposit: {qualifying_dep:,.2f} of {current:,.2f} qualifies")
	
	# Share explanation
	capital = flt(share_capital)
	qualifying_shr = flt(qualifying_shares)
	
	if capital == qualifying_shr and capital > 0:
		explanations.append("All shares qualify")
	elif qualifying_shr == 0 and capital > 0:
		explanations.append("No qualifying shares")
	elif qualifying_shr > 0:
		explanations.append(f"Shares: {qualifying_shr:,.2f} of {capital:,.2f} qualify")
	
	return "; ".join(explanations) if explanations else "No qualifying amounts"