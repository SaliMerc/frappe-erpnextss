# Copyright (c) 2025, Labs and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	if not filters:
		filters = {}
	columns = get_columns()
	data = []
	cs_data= get_cs_data(filters)
	if not cs_data:
		frappe.msgprint("No Data Found")
		return columns, data
	for d in cs_data:
		row = frappe._dict(
			{
				"first_name": d.first_name,
				"dob": d.dob,
				"age": d.age,
			}
		)
		data.append(row)
	chart=get_chart_data(data)
	report_summary=get_report_summary(data)
	#The None in the return is very importatnt as it is for report summary
	return columns, data, None, chart, report_summary

def get_columns():
	return [
		{
			"fieldname": "first_name",
			"label": "First Name",
			"fieldtype": "Data",
			"width": 500,
		},
		{
			"fieldname": "dob",
			"label": "Date of Birth",
			"fieldtype": "Date",
			"width": 300,
		},
		{
			"fieldname": "age",
			"label": "Age",
			"fieldtype": "Int",
			"width": 300,

		},
	]

def get_cs_data(filters):
	conditions=get_conditions(filters)	
	data=frappe.get_all(
		doctype="Server Side Scripting",
		fields=["first_name", "dob", "age"],
		filters=conditions,
		order_by="first_name desc",
	)
	return data

def get_conditions(filters):
	conditions = {}
	for key, value in filters.items():
		if filters.get(key):
			conditions[key] = value
	return conditions

def get_chart_data(data):
    if not data:
        return None
    labels = ['Age <=20', 'Age 21-30', 'Age 31-40']  
    age_data = {
        'Age <=20': 0,
        'Age 21-30': 0,
        'Age 31-40': 0
    }
    
    for entry in data:
        if entry.age <= 20:
            age_data['Age <=20'] += 1
        elif entry.age <= 30:
            age_data['Age 21-30'] += 1
        else:
            age_data['Age 31-40'] += 1

    datasets = [
        {
            "name": "Age Status",
            "values": [
                age_data['Age <=20'],
                age_data['Age 21-30'],
                age_data['Age 31-40']
            ]
        }
    ]
    
    chart = {
        "data": {
            "labels": labels,
            "datasets": datasets,
        },
        "type": "bar",  
        "height": 500,
        "colors": ["#FF6384", "#36A2EB", "#FFCE56"]  
    }
    return chart

def get_report_summary(data):
	if not data:
		return None
	age_below_20, age_above_20, age_above_30=0,0,0
	for entry in data:
		if entry.age <=20:
			age_below_20 +=1
		elif entry.age <=30:
			age_above_20 +=1
		else:
			age_above_30 +=1
	
	return [
		{
			"value": age_below_20,
			"label": "Age below 20",
			"indicator": "green",
			"datatype": "Int",
		},
		{
			"value": age_above_20,
			"label": "Age above 20",
			"indicator": "red",
			"datatype": "Int",
		},
		{
			"value": age_above_30,
			"label": "Age above 30",
			"indicator": "orange",
			"datatype": "Int",
		},
	]
