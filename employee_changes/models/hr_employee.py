from odoo import models, fields
from dateutil import relativedelta


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    sponsor_name = fields.Char(string="Sponsor")
    sponsor_type = fields.Selection([
        ('company', 'Company'),
        ('individual', 'Individual')
    ], string='Sponsor Type')
    employee_type = fields.Selection([
        ('in_source', 'In Source'),
        ('out_source', 'Out Source'),
        ('part_time', 'Part Time')
    ], string='Employee Type')
    residency_number = fields.Char(string="Residency Number")
    passport_expiry_date = fields.Date(string="Passport Expire Date")
    insurance_type = fields.Selection([
        ('saudi', 'Saudi'),
        ('other', 'Other'),
    ], string='Social Insurance Type')

    def visa_passport_expiry_reminder(self):
        today_date = fields.Date.today()
        passport_expiration_template = self.env.ref('employee_changes.email_template_passport_expire')
        visa_expiration_template = self.env.ref('employee_changes.email_template_visa_expire')
        employee_rec = self.env['hr.employee'].search([])
        for employee in employee_rec:
            if employee.passport_expiry_date and employee.passport_id:
                passport_date_difference = relativedelta.relativedelta(employee.passport_expiry_date, today_date)
                if passport_date_difference.months == 1:
                    email_values = {
                        'email_to': '%s, %s, %s' % (employee.work_email,employee.coach_id.work_email or False,employee.parent_id.work_email or False),
                    }
                    passport_expiration_template.send_mail(employee.id, force_send=True, email_values=email_values)
            if employee.visa_expire and employee.visa_no:
                visa_date_difference = relativedelta.relativedelta(employee.visa_expire, today_date)
                if visa_date_difference.months == 1:
                    email_values = {
                        'email_to': '%s, %s, %s' % (employee.work_email,employee.coach_id.work_email or False,employee.parent_id.work_email or False),
                    }
                    visa_expiration_template.send_mail(employee.id, force_send=True, email_values=email_values)