# Copyright (c) 2025, Labs and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class ServerSideScripting(Document):
	pass
	# Server side calls in frappe
	
	# Writing sql queries in frappe
	# def validate(self):
	# 	self.sql()
	
	# def sql(self):
	# 	try:
	# 		results = frappe.db.sql("""
	# 							SELECT
	# 								first_name, 
	# 								middle_name, 
	# 								age
	# 							FROM 
	# 								`tabServer Side Scripting`
	# 							WHERE 
	# 								age < %s
	# 							LIMIT 10
	# 						""", 25, as_dict=1)  
	# 		for row in results:
	# 			frappe.msgprint(f"First Name: {row.first_name}, Middle Name: {row.middle_name}, Age: {row.age}")
	# 	except Exception as e:
	# 		error_msg = str(e)
	# 		frappe.log_error(error_msg, "SQL Query Error")
	# 		frappe.msgprint(f"Error executing SQL query: {error_msg}")
		
	# def get_document_list(self):
	# 	"""Fetch and display a short list of Server Side Scripting records.
	# 	Wrapped in try/except and safe for repeated saves by checking flags.
	# 	"""
	# 	frappe.msgprint("Fetching documents where age > 25")
	# 	try:
	# 		docs = frappe.db.get_list( 
	# 				"Server Side Scripting",
	# 				fields=["name", "first_name", "middle_name", "age"],
	# 				filters={"age": (">", 25)},
	# 				page_length=5,
	# 		)
	# 		for d in docs:
	# 			frappe.msgprint(f"Name: {d.name}, First Name: {d.first_name}, Middle Name: {d.middle_name}, Age: {d.age}")
	# 	except Exception as e:
	# 		error = str(e)
	# 		frappe.log_error(error, "get_document_list")
	# 		frappe.msgprint(f"Error fetching documents: {error}")

	# def validate(self):
	# 	"""Run lightweight actions on save while avoiding recursion.
	# 	Make sure this remains minimal to avoid side effects during save.
	# 	"""
	# 	# If a flag was set on this document (e.g. by create_new_doc), skip.
	# 	if self.flags.get("skip_get_document_list"):
	# 		return
	# 	try:
	# 		# Run the document-list action once per save cycle.
	# 		self.get_document_list()
	# 		# Mark to avoid re-running in the same save chain.
	# 		self.flags.skip_get_document_list = True
	# 	except Exception as e:
	# 		error = str(e)
	# 		frappe.log_error(error, "validate")
	# 		frappe.msgprint(f"Validation error: {error}")
	# def create_new_doc(self):
		# """Create a new Server Side Scripting document with the provided details and save to database
		# Always prevent teh issues of recursion by using flags
		# """
		# try:
		# 	doc = frappe.new_doc('Server Side Scripting')
		# 	doc.first_name = "mercy"
		# 	doc.middle_name = "salie"
		# 	doc.email = "merc@gmail.com"
		# 	doc.mobile_number = "1234567890"
		# 	doc.dob = "1990-01-01"
		# 	doc.flags.skip_validate = True  
			
		# 	doc.insert(ignore_mandatory=True, ignore_permissions=True)
		# 	frappe.msgprint(f"Document created successfully: {doc.name}")
		# 	return doc
			
		# except Exception as e:
		# 	error_msg = str(e)
		# 	frappe.msgprint(f"Failed to create new document: {error_msg}")
		# 	return None
	# """For deletion of a record"""
	# def delete_document(self, doc_name):
	# 	try:
	# 		doc = frappe.get_doc('Server Side Scripting', 'SSR-0040')
	# 		doc.delete()
	# 		frappe.msgprint(f"Document {doc_name} deleted successfully.")
	# 	except Exception as e:
	# 		error_msg = str(e)
	# 		frappe.msgprint(f"Failed to delete document {doc_name}: {error_msg}")
	
	# def validate(self):
	# 	"""Validate method - runs when document is being saved"""
	# 	if not self.flags.get('skip_validate'):
	# 		self.create_new_doc()
	
	# def new_document(self):
	# 	try:
	# 		doc = frappe.new_doc('Client Side Scripting')
	# 		doc.first_name = 'Mer'
	# 		doc.middle_name = 'Katy' 
	# 		doc.age = 30            

	# 		doc.insert(ignore_mandatory=True, ignore_permissions=True)

	# 		print(f"SUCCESS: New doc created - {doc.name}")
	# 		frappe.msgprint(f"Well, this works! New document: <a href='/app/client-side-scripting/{doc.name}'>{doc.name}</a>")

		# except Exception as e:
		# 	error_msg = str(e)
		# 	print("ERROR creating document:", error_msg)
		# 	frappe.msgprint(f"Failed to create new document: {error_msg}")
	""""
	# works before sending the data to the databas
	def validate(self):
		frappe.msgprint("Hello")
	
	# Works before saving the document
	def before_save(self):
		frappe.msgprint("Yooj")
	
	# Works before inserting the data into database
	def before_insert(self):
		frappe.msgprint("hsjd")
	
	# Works after inserting the data into database ?(throw an error)
	def after_insert(self):
		frappe.msgprint("hsjd")

	# Works when we update a field in the form
	def on_update(self):
		frappe.msgprint("hsjd")
	
	# Works when we submit the form
	def on_submit(self):
		frappe.msgprint("hsjd")
	
	# Works before we submit the form
	def before_submit(self):
		frappe.msgprint("hsjd")

	def on_cancel(self):
		frappe.msgprint("hsjd")
	
	def on_trash(self):
		frappe.msgprint("hsjd")

	def after_delete(self):
		frappe.msgprint("hsjd")"""

	# def validate(self):
	# 	frappe.msgprint(_("Hello, my full name is '{0}'").format(
	# 		self.first_name +" "+ self.middle_name
	# 	))
	
	# Working with child table
	# def validate(self):
	# 	for row in self.get("family_member"):
	# 		frappe.msgprint(_
	# 			   (
	# 				   "The family members number {0} have the name '{1}' and relation of '{2}'"
	# 			   ).format(row.idx, row.name1, row.relation))

	# gettign data from another doctype
	"""
	def validate(self):
		self.get_document()
	def get_document(self):
		# The name variable should be that of the related field
		doc = frappe.get_doc('Client Side Scripting', self.client_code)

		frappe.msgprint(f"The first name is {doc.first_name} and the age is {doc.age}")

		# Getting items from the child table: family_member is the field name for the child table in the lcient side doctype.  
		for row in doc.get('family_member'):
			frappe.msgprint(_("{0} The maily member name is {1} and their age is {2} and their relation is {3}").format(row.idx, row.name1, row.age, row.relation))"""
	
	# doc.insert()
