from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta

class HrLoan(models.Model):
	_inherit = 'hr.loan'

	def compute_installment(self):
		"""This automatically create the installment the employee need to pay to
		company based on payment start date and the no of installments.
			"""
		for loan in self:
			loan.loan_lines.unlink()
			date_start = datetime.strptime(str(loan.payment_date), '%Y-%m-%d')
			amount = loan.amt_with_interest / loan.installment
			for i in range(1, loan.installment + 1):
				self.env['hr.loan.line'].create({
					'date': date_start,
					'amount': amount,
					'employee_id': loan.employee_id.id,
					'loan_id': loan.id})
				date_start = date_start + relativedelta(months=1)
			loan._compute_loan_amount()
		return True

	def _compute_loan_amount(self):
		total_paid = 0.0
		for loan in self:
			for line in loan.loan_lines:
				if line.paid:
					total_paid += line.amount
			# balance_amount = loan.loan_amount - total_paid
			# loan.total_amount = loan.loan_amount
			balance_amount = loan.amt_with_interest - total_paid
			loan.total_amount = loan.amt_with_interest
			loan.balance_amount = balance_amount
			loan.total_paid_amount = total_paid

	loan_type = fields.Many2one('hr.loan.type',string="Loan Type")
	interest_rate = fields.Float(string="Interest Percentage",digits=(16, 4), default=0.0)
	amt_with_interest = fields.Float(string="Loan Amount (W/ Interest)",compute='_include_interest_rate',readonly=True,store=True)


	@api.depends('loan_type','loan_amount')
	def _include_interest_rate(self):
		for rec in self:
			rec.amt_with_interest = 0.0
			if rec.loan_amount > 0.0 and rec.loan_type and rec.loan_type.interest_rate > 0.0:
				amt  = rec.loan_amount + ((rec.loan_amount/100.00)*rec.loan_type.interest_rate)
				rec.amt_with_interest = float(amt)

class HrLoanDatechange(models.Model):
	_name = 'hr.loan.datechange'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	active = fields.Boolean(default=True, readonly=True)
	name = fields.Char(string='Name')
	employee_id = fields.Many2one('hr.employee',string='Employee ID')
	state = fields.Selection([
		('draft', 'To Submit'),
		('confirm', 'To Approve'),
		('validate', 'Approved'),
		('refuse', 'Refused'),
		('cancel', 'Cancelled')
		], string='Status', default='draft', store=True, tracking=True, copy=False, readonly=False)
	request_date_from = fields.Date('Request Date',tracking=True)
	request_date_to = fields.Date('Change Date Date',tracking=True)
	report_note = fields.Text('Reason', copy=False)
	loan_id = fields.Many2one('hr.loan',string="Loan ID")
	attachment_ids = fields.One2many('ir.attachment', 'res_id', string="Attachments")

	@api.model
	def create(self, values):
		values['name'] = self.env['ir.sequence'].get('hr.loan.datechange.seq') or ' '
		res = super(HrLoanDatechange, self).create(values)
		return res

	def action_draft(self):
		return self.write({'state': 'draft'})

	def action_refuse(self):
		return self.write({'state': 'refuse'})

	def action_submit(self):
		line_obj = self.env['hr.loan.line'].search([('date','=',self.request_date_from),('loan_id','=',self.loan_id.id)])
		if not line_obj:
			raise ValidationError(_("Please Select a date that exist in the installement"))
		else:
			self.write({'state': 'confirm'})

	def action_cancel(self):
		self.write({'state': 'cancel'})

	def action_approve(self):
		for data in self:
			line_obj = self.env['hr.loan.line'].search([('date','=',data.request_date_from),('loan_id','=',data.loan_id.id)])
			req = self.env['hr.loan.line'].search([('date','=',data.request_date_to),('loan_id','=',data.loan_id.id)])
			if req:
				req.amount += line_obj.amount
				line_obj.unlink()
			else:
				line_obj.date = data.request_date_to 
			data.write({'state': 'validate'})

class HrLoan(models.Model):
	_inherit = 'hr.loan'

	datechange_count = fields.Integer(compute='_compute_datechange_count', string='DateChange Count')

	def _compute_datechange_count(self):
		for obj in self:
			datechange_data = self.env['hr.loan.datechange'].sudo().search([('loan_id', '=', self.id),])
			obj.datechange_count = len(datechange_data)

	def request_datechange(self):
		return {
			'name': _('Raise Date Change Request'),
			'type': 'ir.actions.act_window',
			'res_model': 'hr.loan.datechange',
			'views': [[self.env.ref('hr_extend.hr_loan_datechange_form_view').id, 'form']],
			'domain': [('employee_id', 'in', self.ids)],
			'context': {
				'default_employee_id': self.employee_id.id,
				'default_loan_id': self.id,
			},
		}