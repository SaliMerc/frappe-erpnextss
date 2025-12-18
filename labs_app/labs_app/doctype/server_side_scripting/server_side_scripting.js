frappe.ui.form.on('Server Side Scripting', {
    refresh: frm => update_full_name_and_dob(frm),
    first_name: frm => update_full_name_and_dob(frm),
    middle_name: frm => update_full_name_and_dob(frm),
    dob: frm => update_full_name_and_dob(frm),
    validate: frm => update_full_name_and_dob(frm)
});

function update_full_name_and_dob(frm) {
    let full_name = "";
       
    if (frm.doc.first_name) {
        full_name = full_name + frm.doc.first_name.trim();
    }
    
    if (frm.doc.middle_name) {
        if (full_name) full_name = full_name + " ";  
        full_name = full_name + frm.doc.middle_name.trim();
    }
    
    frm.set_value('full_name', full_name);

    let age = null
    if (frm.doc.dob) {
        const dob = new Date(frm.doc.dob);
        const currentYear = new Date().getFullYear();
        age = currentYear - dob.getFullYear();
    }

    frm.set_value('age', age);
}