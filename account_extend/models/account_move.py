from odoo import models, fields, api, exceptions, _
from odoo.tests import tagged, Form
from datetime import date, datetime, time, timedelta
from odoo.exceptions import UserError, ValidationError

# class AccountInvoiceLine(models.Model):
# 	_inherit = 'account.move.line'
			
# 		@api.model
# 		def create(self,vals):
# 			res =super(AccountInvoiceLine, self).create(vals)
# 			if not res.product_id and res.display_type == 'product':
# 				res.unlink()
# 			return res

class AccountMove(models.Model):
	_inherit = "account.move"


	counter_id = fields.Many2one('counter.master',string='Counter Number')
	degree_level_id = fields.Many2one('degree.level.master',string='Degree')
	term_id = fields.Many2one('fees.for',string='Term')
	course_year = fields.Integer(string="Course Year")
	fee_manage_id = fields.Many2one('fees.management',string='Fee Management ID',store=True)
	fee_line_ids = fields.One2many('account.fees.details','move_id',string='Fee Details',store=True,copy=False,readonly=True,states={'draft': [('readonly', False)]})


	def clean_lines(self):
		self.fee_line_ids = [(6, 0, [])]
		self.invoice_line_ids = [(6, 0, [])]
		return True

	def action_register_payment(self):
		for obj in self:
			if not obj.partner_id:
				obj.partner_id = obj.details_id.custom_create_contacts()

			if obj.fees_id and obj.details_id.invoice_ids:
				move_objs = obj.details_id.invoice_ids.filtered(lambda x:x.move_type == 'out_invoice' and x.payment_state in ['not_paid','partial'] and not x.parent_invoice_id and x.fees_id)
				for itm in move_objs:
					if itm.fees_for_id.term_order < obj.fees_for_id.term_order:
						raise ValidationError(_(f"Please process the lowest term order collections first!"))

			if obj.state =='draft':
				obj.action_post()

		cash = self.env['account.journal'].search([('name','=','Cash'),('company_id','=',self.env.company.id)],limit=1)
		res = super(AccountMove, self).action_register_payment()
		res['context'].update(default_journal_id=cash.id)
		return res
	
	def action_post(self):
		for obj in self:
			if obj.fees_id and obj.details_id.invoice_ids:
				move_objs = obj.details_id.invoice_ids.filtered(lambda x:x.move_type == 'out_invoice' and x.payment_state in ['not_paid','partial'] and not x.parent_invoice_id and x.fees_id)
				for itm in move_objs:
					if itm.fees_for_id.term_order < obj.fees_for_id.term_order:
						raise ValidationError(_(f"Please process the lowest term order collections first!"))
					
		res = super(AccountMove,self).action_post()
		return res
			

	# @api.onchange('details_id')
	# def _get_invoice_info(self):
	# 	if self.details_id:
	# 		details_obj = self.env['res.partner'].search([('aadhar_no','=',self.details_id.aadhar_no)],limit=1)
	# 		self.degree_id = self.details_id.degree_id.id
	# 		self.partner_id = details_obj.id
	# 		self.course_id = self.details_id.courses_id.id
	# 		self._onchange_fee_details()

	# @api.onchange('is_true')
	# def _onchange_fee_details(self):
		# if self._origin.is_true ==True and self.is_true == False:
		# 	self.term_id = False
		# 	self.course_year = 0
		# 	self.clean_lines()
		# if self.is_true == True:
		# 	check_invoice = self.env['account.move'].search([('is_true','=',True),('state','!=','cancel'),('payment_state','in',('not_paid','partial')),('partner_id','=',self.partner_id.id)])
		# 	if check_invoice:
		# 		raise UserError(_('A Partially paid invoice already exist for %s') % self.partner_id.name)
		# 	not_in_invoice = self.env['account.move'].search([('partner_id','=',self.partner_id.id),('state','!=','cancel'),('is_true','=',True)]).mapped('fee_manage_id.id')
		# 	obj = self.env['fees.management'].search([
		# 		('id', 'not in', tuple(not_in_invoice)),
		# 		('degree_id', '=', self.degree_id.id),
		# 		('course_id', '=', self.course_id.id)],
		# 		order='course_year asc',
		# 		limit=1)
		# 	if obj:
		# 		self.fee_manage_id = obj.id
		# 		self.term_id = obj.fees_for_id.id
		# 		self.course_year = obj.course_year
		# 		vals = []
		# 		inv_vals = []
		# 		move_id = self._origin.id if isinstance(self._origin.id, int) else self.id
		# 		for i in obj.fees_ids:
		# 			fee_val = {
		# 				'product_id': i.product_id.id,
		# 				'payment_type': i.payment_type,
		# 				'priority': i.priority,
		# 				'terms': i.terms,
		# 				'amount': i.amount,
		# 				'move_id': int(move_id),
		# 				'unpaid': i.amount
		# 			}
		# 			vals.append((0, 0, fee_val))

		# 			inv_val = {
		# 				'product_id': i.product_id.id,
		# 				'move_id': int(move_id),
		# 				'price_unit': i.amount,
		# 				'tax_ids': [(6, 0, i.product_id.taxes_id.ids)],
		# 				'display_type':'product'
		# 			}
		# 			if i.product_id.id:
		# 				inv_vals.append((0, 0, inv_val))
		# 		self.clean_lines()
		# 		self.update({
		# 			'fee_line_ids': vals,
		# 			'invoice_line_ids': inv_vals
		# 		})
		# 	else:
		# 		self.fee_manage_id = False
		# 		self.term_id = False
		# 		self.course_year = 0
		# 		self.clean_lines()


class AccountFeesDetails(models.Model):
	_name = 'account.fees.details'


	product_id = fields.Many2one('product.product',string="Fees Heads",required=True)
	amount = fields.Monetary(string="Amount", currency_field='currency_id')
	paid = fields.Monetary(string="Paid", currency_field='currency_id')
	unpaid = fields.Monetary(string="Unpaid", currency_field='currency_id',store=True)
	priority = fields.Integer(string='Priority')
	currency_id = fields.Many2one('res.currency', string='Currency')
	move_id = fields.Many2one('account.move', string="Fees Details")
	company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, default=lambda self: self.env.company)
	payment_type = fields.Selection(string='Payment Type', selection=[('term', 'Term'),
							('yearly', 'Yearly')])
	terms = fields.Integer(string="Terms")
	states = fields.Selection(string='State', selection=[('partial', 'Partial'),('unpaid', 'unpaid'),('paid', 'Paid'),('cancel', 'Cancelled')],default='unpaid',required=True)

	@api.onchange('payment_type')
	def _onchange_payment_type(self):
		if self.payment_type:
			self.terms = '1'
		else:
			self.terms = '0'

	def make_payment(self):
		if self.unpaid == 0:
			raise UserError(_('Theere is nothing left to pay'))
		return {
            'name': _('Register Payment'),
            'res_model': 'account.payment.register',
            'view_mode': 'form',
            'context': {
                'active_model': 'account.move',
                'active_ids': self.move_id.id,
				'default_fee_id':self.id,
				'default_from_fee':True,
				'default_amount':self.unpaid
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }


# class AccountPaymentRegister(models.TransientModel):
# 	_inherit = 'account.payment.register'

# 	def action_create_payments(self):
# 		res = super(AccountPaymentRegister, self).action_create_payments()
# 		active_ids = self._context.get("active_ids", [])
# 		invoices = self.env["account.move"].browse(active_ids)
# 		for inv in invoices:
# 			if inv.is_true:
# 				if self.from_fee and self.fee_id:
# 					if self.amount > self.fee_id.amount:
# 						raise UserError(_('The amount should not be greater than the unpaid amount'))
# 					self.fee_id.paid += self.amount
# 					self.fee_id.unpaid -= self.amount
# 					if self.fee_id.unpaid == 0.00:
# 						self.fee_id.states='paid'
# 					elif self.fee_id.amount >self.fee_id.unpaid:
# 						self.fee_id.states='partial'

# 					return res
# 				fee_obj = self.env['account.fees.details'].search([('move_id','=',inv.id),('states','in',('unpaid','partial'))],order='priority asc')
# 				amt = self.amount
# 				num=0
# 				for i in range(len(fee_obj)):
# 					if fee_obj[num].priority == 0:
# 						num += 1
# 						continue
# 					if fee_obj[num].unpaid == 0:
# 						num += 1
# 						continue
# 					if amt >= fee_obj[num].unpaid:
# 						fee_obj[num].paid += fee_obj[num].unpaid
# 						amt -= fee_obj[num].unpaid
# 						unpaid = fee_obj[num].unpaid - fee_obj[num].paid
# 						if unpaid >= 0:
# 							fee_obj[num].unpaid -= fee_obj[num].paid
# 						else:
# 							fee_obj[num].unpaid = 0.00	
# 						fee_obj[num].states = 'paid'
# 					else:
# 						if amt > 0:
# 							fee_obj[num].paid += amt
# 							fee_obj[num].unpaid = fee_obj[num].unpaid - amt
# 						amt -= fee_obj[num].unpaid
# 						fee_obj[num].states = 'partial'
# 					num += 1

# 				if invoices:
# 					admission_rec = self.env['admission.list'].search(
# 						[('admission_id', '=', invoices.admission_id.id)])
# 					admission_rec.payment_state = invoices.payment_state
# 		return res