from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class StudentOneTimeFees(models.Model):
	_name = 'student.onetime.fees'
	

	student_id = fields.Many2one('student.details',string="Student")
	onetimefees_id = fields.Many2one('one.time.fees',string="One Time Fees")
	course_id = fields.Many2one('courses.master', string="Course Name", required=True)
	degree_id = fields.Many2one('degree.master', string="Degree Name")
	degree_level_id = fields.Many2one('degree.level.master', string="Degree")
	college_id = fields.Many2one('res.company', 'College Name', readonly=True, index=True, default=lambda self: self.env.company)
	currency_id = fields.Many2one('res.currency', string='Currency')
	amount = fields.Monetary(string="Amount", currency_field='currency_id')
	invoice_created = fields.Boolean("Invoice Created",default=False)
