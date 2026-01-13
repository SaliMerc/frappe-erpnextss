# Copyright (c) 2025, Labs and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    if not filters:
        filters = {}
    
    columns = get_columns()
    data = get_sales_data(filters)
    
    if not data:
        frappe.msgprint(_("No Data Found"))
        return columns, [], None, None, None
    
    # Format data
    formatted_data = []
    for d in data:
        row = {
            "name": d.name,
            "posting_date": d.posting_date,
            "posting_time": d.posting_time,
            "customer": d.customer,
            "customer_name": d.customer_name,
            "territory": d.territory,
            "pos_profile": d.pos_profile,
            "total_qty": d.total_qty,
            "total": d.total,
            "discount_amount": d.discount_amount,
            "grand_total": d.grand_total,
            "outstanding_amount": d.outstanding_amount,
            "paid_amount": d.paid_amount,
            "status": d.status,
            "is_return": d.is_return,
        }
        formatted_data.append(row)
    
    # Get chart and summary
    chart = get_chart_data(formatted_data, filters)
    report_summary = get_report_summary(formatted_data)
    
    return columns, formatted_data, None, chart, report_summary


def get_columns():
    return [
        {
            "fieldname": "name",
            "label": _("Invoice No"),
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 140,
        },
        {
            "fieldname": "posting_date",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 100,
        },
        {
            "fieldname": "posting_time",
            "label": _("Time"),
            "fieldtype": "Time",
            "width": 100,
        },
        {
            "fieldname": "customer",
            "label": _("Customer ID"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 120,
        },
        {
            "fieldname": "customer_name",
            "label": _("Customer Name"),
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "territory",
            "label": _("Territory"),
            "fieldtype": "Link",
            "options": "Territory",
            "width": 120,
        },
        {
            "fieldname": "pos_profile",
            "label": _("POS Profile"),
            "fieldtype": "Link",
            "options": "POS Profile",
            "width": 120,
        },
        {
            "fieldname": "total_qty",
            "label": _("Total Qty"),
            "fieldtype": "Float",
            "width": 100,
        },
        {
            "fieldname": "total",
            "label": _("Total"),
            "fieldtype": "Currency",
            "width": 120,
        },
        {
            "fieldname": "discount_amount",
            "label": _("Discount"),
            "fieldtype": "Currency",
            "width": 110,
        },
        {
            "fieldname": "grand_total",
            "label": _("Grand Total"),
            "fieldtype": "Currency",
            "width": 130,
        },
        {
            "fieldname": "paid_amount",
            "label": _("Paid Amount"),
            "fieldtype": "Currency",
            "width": 130,
        },
        {
            "fieldname": "outstanding_amount",
            "label": _("Outstanding"),
            "fieldtype": "Currency",
            "width": 130,
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "fieldname": "is_return",
            "label": _("Is Return"),
            "fieldtype": "Check",
            "width": 80,
        },
    ]


def get_sales_data(filters):
    conditions = get_conditions(filters)
    
    try:
        data = frappe.get_all(
            "Sales Invoice",
            fields=[
                "name",
                "posting_date",
                "posting_time",
                "customer",
                "customer_name",
                "territory",
                "pos_profile",
                "total_qty",
                "total",
                "discount_amount",
                "grand_total",
                "outstanding_amount",
                "paid_amount",
                "status",
                "is_return",
            ],
            filters=conditions,
            order_by="posting_date desc, posting_time desc",
        )
        return data
    except Exception as e:
        frappe.log_error(f"Error fetching Sales Invoice data: {str(e)}")
        return []


def get_conditions(filters):
    conditions = {"docstatus": 1}  # Only submitted invoices
    
    # Handle date range filters
    if filters.get("from_date") and filters.get("to_date"):
        conditions["posting_date"] = ["between", [filters.get("from_date"), filters.get("to_date")]]
    elif filters.get("from_date"):
        conditions["posting_date"] = [">=", filters.get("from_date")]
    elif filters.get("to_date"):
        conditions["posting_date"] = ["<=", filters.get("to_date")]
    
    # POS only filter
    if filters.get("pos_only"):
        conditions["is_pos"] = 1
    
    # Handle other filters
    if filters.get("customer"):
        conditions["customer"] = filters.get("customer")
    
    if filters.get("pos_profile"):
        conditions["pos_profile"] = filters.get("pos_profile")
    
    if filters.get("territory"):
        conditions["territory"] = filters.get("territory")
    
    if filters.get("status"):
        conditions["status"] = filters.get("status")
    
    if filters.get("is_return"):
        conditions["is_return"] = 1
    
    return conditions


def get_chart_data(data, filters):
    if not data:
        return None
    
    try:
        chart_type = filters.get("chart_type", "daily_sales")
        
        if chart_type == "daily_sales":
            return get_daily_sales_chart(data)
        elif chart_type == "payment_mode":
            return get_payment_mode_chart(data)
        elif chart_type == "territory":
            return get_territory_chart(data)
        else:
            return get_daily_sales_chart(data)
            
    except Exception as e:
        frappe.log_error(f"Error generating chart: {str(e)}")
        return None


def get_daily_sales_chart(data):
    """Group sales by date"""
    daily_sales = {}
    
    for entry in data:
        date = str(entry.get("posting_date"))
        amount = float(entry.get("grand_total") or 0)
        
        if entry.get("is_return"):
            amount = -amount
        
        if date not in daily_sales:
            daily_sales[date] = 0
        daily_sales[date] += amount
    
    # Sort by date
    sorted_dates = sorted(daily_sales.keys())
    labels = sorted_dates
    values = [daily_sales[date] for date in sorted_dates]
    
    chart = {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Daily Sales",
                    "values": values
                }
            ],
        },
        "type": "line",
        "height": 300,
        "colors": ["#29CD42"]
    }
    
    return chart


def get_payment_mode_chart(data):
    """Get payment mode distribution"""
    payment_modes = {}
    
    for entry in data:
        invoice_name = entry.get("name")
        
        # Get payment entries for this invoice
        payments = frappe.get_all(
            "Sales Invoice Payment",
            filters={"parent": invoice_name},
            fields=["mode_of_payment", "amount"]
        )
        
        for payment in payments:
            mode = payment.get("mode_of_payment") or "Cash"
            amount = float(payment.get("amount") or 0)
            
            if mode not in payment_modes:
                payment_modes[mode] = 0
            payment_modes[mode] += amount
    
    if not payment_modes:
        return None
    
    labels = list(payment_modes.keys())
    values = list(payment_modes.values())
    
    chart = {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Payment Modes",
                    "values": values
                }
            ],
        },
        "type": "pie",
        "height": 300,
        "colors": ["#29CD42", "#4C78FF", "#FFA00A", "#F56B6B"]
    }
    
    return chart


def get_territory_chart(data):
    """Group sales by territory"""
    territories = {}
    
    for entry in data:
        territory = entry.get("territory") or "Not Set"
        amount = float(entry.get("grand_total") or 0)
        
        if entry.get("is_return"):
            amount = -amount
        
        if territory not in territories:
            territories[territory] = 0
        territories[territory] += amount
    
    labels = list(territories.keys())
    values = list(territories.values())
    
    chart = {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Sales by Territory",
                    "values": values
                }
            ],
        },
        "type": "line",
        "height": 300,
        "colors": ["#4C78FF"]
    }
    
    return chart


def get_report_summary(data):
    if not data:
        return None
    
    try:
        total_sales = 0.0
        total_qty = 0.0
        total_discount = 0.0
        total_outstanding = 0.0
        total_paid = 0.0
        return_amount = 0.0
        invoice_count = 0
        return_count = 0
        
        for entry in data:
            grand_total = float(entry.get("grand_total") or 0)
            qty = float(entry.get("total_qty") or 0)
            discount = float(entry.get("discount_amount") or 0)
            outstanding = float(entry.get("outstanding_amount") or 0)
            paid = float(entry.get("paid_amount") or 0)
            
            if entry.get("is_return"):
                return_amount += grand_total
                return_count += 1
            else:
                total_sales += grand_total
                invoice_count += 1
            
            total_qty += qty
            total_discount += discount
            total_outstanding += outstanding
            total_paid += paid
        
        net_sales = total_sales - abs(return_amount)
        avg_invoice_value = net_sales / invoice_count if invoice_count > 0 else 0
        
        summary = [
            {
                "value": net_sales,
                "label": "Net Sales",
                "indicator": "blue",
                "datatype": "Currency",
            },
            {
                "value": total_sales,
                "label": "Gross Sales",
                "indicator": "green",
                "datatype": "Currency",
            },
            {
                "value": invoice_count,
                "label": "Total Invoices",
                "indicator": "blue",
                "datatype": "Int",
            },
            {
                "value": avg_invoice_value,
                "label": "Avg Invoice Value",
                "indicator": "orange",
                "datatype": "Currency",
            },
            {
                "value": total_qty,
                "label": "Total Qty Sold",
                "indicator": "green",
                "datatype": "Float",
            },
            {
                "value": total_discount,
                "label": "Total Discount",
                "indicator": "red",
                "datatype": "Currency",
            },
            {
                "value": abs(return_amount),
                "label": "Returns",
                "indicator": "red",
                "datatype": "Currency",
            },
            {
                "value": return_count,
                "label": "Return Count",
                "indicator": "red",
                "datatype": "Int",
            },
            {
                "value": total_paid,
                "label": "Total Paid",
                "indicator": "green",
                "datatype": "Currency",
            },
            {
                "value": total_outstanding,
                "label": "Total Outstanding",
                "indicator": "orange",
                "datatype": "Currency",
            },
        ]
        
        return summary
    except Exception as e:
        frappe.log_error(f"Error generating report summary: {str(e)}")
        return None