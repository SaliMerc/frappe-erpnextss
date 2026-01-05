frappe.pages['first-page'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'my first page',
		single_column: true
	});

page.set_title('This is the new title')
page.set_indicator("Done", "green")

let $btn = page.set_primary_action('New', () =>frappe.msgprint("clicked"))

let $btnone = page.set_secondary_action('Refresh', () =>frappe.msgprint("refreshed"))

page.add_menu_item('Send  Mail', () =>frappe.msgprint('Clicked send mail'))
page.add_menu_item('end', () =>frappe.msgprint('Clicked send mail'))
page.add_menu_item('il', () =>frappe.msgprint('Clicked send mail'))
page.add_menu_item('Mail', () =>frappe.msgprint('Clicked send mail'))

page.add_action_item('Delete', () =>frappe.msgprint('Clicked delete'))

let field = page.add_field({
	label: 'Status',
	fieldtype:'Select',
	fieldname:'status',
	options: [
		"open",
		"closed",
		"cancelled"
	],
	change(){
		frappe.msgprint(field.get_value())
	}
})

$(frappe.render_template("mypage", {"data": "Yooh"})).appendTo(page.body);
}

