import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class Fees(models.Model):
	_name = 'fees.for'
	_inherit = ['mail.thread']

	name = fields.Char(string="Name")
	term_order = fields.Integer(string="Term Order",unique=True)
	rejected_remarks = fields.Char(string="Rejected Remarks", track_visibility="always")
	state = fields.Selection(string='State', selection=[('draft', 'New'),
							('waiting_for_approval_1', 'Waiting for Approval 1'),
							('waiting_for_approval_2', 'Waiting for Approval 2'),
							('approved', 'Approved'), ('rejected','Rejected')],readonly=True, 
							copy=False, index=True, track_visibility='always', default='draft')
	
	semester_id = fields.Many2one('semester.master',string="Semester")
	
	_sql_constraints = [
        ('unique_term_order', 'unique(term_order)', 'The value of the term order field must be unique.'),
		('unique_name', 'unique(name)', 'The value of the name field must be unique.'),
    ]

	def action_send_app_1(self):
		self.state = 'waiting_for_approval_1'

	def action_app_1_done(self):
		self.state = 'waiting_for_approval_2'

	def action_app_2_done(self):
		self.state = 'approved'

	# @api.onchange('term_order')
	# def onchange_term_order(self):
	# 	if self.term_order:
	# 		existing_order_obj = self.search([('id','!=',self.id),('term_order','=',self.term_order)],limit=1)
	# 		if existing_order_obj > 1:
	# 			raise ValidationError(_(f"Term Order {self.term_order} is already assigned to {self.existing_order_obj.name} !"))

	def button_reject(self):
		form_view = self.env.ref('fees_management.fees_reject_remark_view_id')
		return {
			'name': "Reject Remarks",
			'view_mode': 'form',
			'view_type': 'form',
			'view_id': form_view.id,
			'res_model': 'fees.reject.remark',
			'type': 'ir.actions.act_window',
			'target': 'new',
		}


class InheritSemesterMaster(models.Model):
	_inherit = "semester.master"

	term_ids = fields.One2many('fees.for','semester_id',string="Term")