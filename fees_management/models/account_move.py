from odoo import models,fields,api,_
from odoo.exceptions import ValidationError, UserError
from odoo.tools.misc import get_lang
import pytz
from datetime import datetime
from num2words import num2words
from odoo.tools import (
	date_utils,
	email_re,
	email_split,
	float_compare,
	float_is_zero,
	float_repr,
	format_amount,
	format_date,
	formatLang,
	frozendict,
	get_lang,
	is_html_empty,
	sql
)

class InheritAccountMove(models.Model):
	_inherit = "account.move"


	degree_level_id = fields.Many2one('degree.level.master',string="Degree")
	semester_id = fields.Many2one('semester.master',string="Semaster")
	batch_id = fields.Many2one('batch.courses.master',string='Batch', track_visibility='always')
	fee_payment_type = fields.Selection([('term','Term'),('yearly','Yearly')])
	fees_for_id = fields.Many2one('fees.for',string="Fees for")
	term = fields.Integer('Term')
	details_id = fields.Many2one('student.details',string='Roll Number')
	is_true = fields.Boolean(string="Fee Payment")
	fees_id = fields.Many2one('fees.management',string="Fees")
	fees_line_id = fields.Many2one('fees.details',string="Fees Details")
	parent_invoice_id = fields.Many2one("account.move",string="Parent Invoice",index=True,track_visibility="always")
	line_invoices_ids = fields.One2many("account.move","parent_invoice_id",string="Line Invoices",index=True,track_visibility="always")
	line_invoice_count = fields.Integer(string="Child Collection Count",compute="get_child_invoice_count")
	map_concession_ids = fields.One2many('map.move.concession','invoice_id',string="Concession",copy=False)
	course_id = fields.Many2one('courses.master', string="Course",store=True)
	one_time_fee_id = fields.Many2one('one.time.fees',string='One time fees')
	last_payment = fields.Boolean(string='Last Payment',default=False,readonly=False)



	@api.model
	def create(self,vals):
		res = super(InheritAccountMove,self).create(vals)
		if 'map_concession_ids' in vals.keys():
			res.custom_onchange_map_concession_ids()
		return res
	
	def write(self,vals):
		res = super(InheritAccountMove,self).write(vals)
		if 'map_concession_ids' in vals.keys():
			self.custom_onchange_map_concession_ids()
		return res

	# @api.onchange('map_concession_ids')
	def custom_onchange_map_concession_ids(self):
		concession_amount = 0
		concession_line = self.invoice_line_ids.filtered(lambda x: x.product_id.default_code == 'CONCESSION')
		for concession in self.map_concession_ids:
			concession_amount += concession.allocated_amount
			if concession.allocated_amount:
				if concession_line:
					concession_line.write({'price_unit': concession.allocated_amount})  # Use write() to update the existing line
				else:
					concession_product_obj = self.env.ref('fees_management.concession_service_product')
					existing_lines = [(6, 0, self.invoice_line_ids.ids)]
					new_lines = [(0, 0, {'move_id':self.id,'quantity':-1,'product_id': concession_product_obj.id, 'price_unit': concession.allocated_amount,'fees_for_id':self.fees_for_id.id,'tax_ids':False,'is_concession':True,'display_type':'product'})]
					lines_to_create = existing_lines + new_lines
					self.invoice_line_ids= lines_to_create
		if not self.map_concession_ids:
			self.invoice_line_ids = [(2,concession_line.id)]
	
	# Compute method get child invoice count
	def get_child_invoice_count(self):
		for move in self:
			move.line_invoice_count = len(move.line_invoices_ids)

	def action_return_child_invoices(self):
		return {
				'name': 'Line Collections View',
				'type': 'ir.actions.act_window',
				'res_model': 'account.move',
				# 'res_id': new_move_obj.id,
				# 'view_id': invoice_form_view.id,
				'view_mode': 'tree,form',
				'domain':[('id','in',self.line_invoices_ids.ids)],
				'target': 'current',
				# 'flags': {'form': {'action_buttons': True}},
			}
	
	def get_words_from_number(self,number):
		return num2words(number, lang='en').capitalize() + ' Rupees Only'

	def custom_priority_sort(self, move_lines):
		"""
		Custom sorting function to sort account move line objects based on 'priority'.
		Records with priority 0 will appear at the end.
		"""
		def sort_key(move_line):
			# Custom key function to sort records based on 'priority'.
			# Return a tuple with two elements: (0 if priority is 0, priority).
			return (1 if move_line.priority == 0 else 0, move_line.priority)

		# Sort the move_lines list using the custom key function
		sorted_move_lines = sorted(move_lines, key=sort_key)

		return sorted_move_lines
		

	# Helper method to prepare the list of move lines to do the reconciliation
	def prepare_move_lines_by_term_and_priority_wise(self,payments):
		sorted_move_objs = self.env['account.move']
		if self.details_id.invoice_ids:
			sorted_move_objs = sorted(self.details_id.invoice_ids.filtered(lambda y:y.payment_state != 'paid' and y.move_type=='out_invoice' and not y.parent_invoice_id and y.fees_id),key=lambda x:(x.fees_for_id.term_order or 0))

		payment_names = payments.mapped('name')

		if self.one_time_fee_id:
			sorted_move_objs = [self]

		posted_moves = []

		for move in sorted_move_objs:
			for idx,payment in enumerate(payment_names):
				payments.filtered(lambda itm:itm.name == payment).get_payment_balance()
				if payments.filtered(lambda itm:itm.name == payment).amount_balance > 0:
					if idx == 0:
						if move.state == 'draft':
							move.action_post()
							posted_moves.append(move.id)
					move._compute_payments_widget_to_reconcile_info()
					if move.invoice_outstanding_credits_debits_widget and move.invoice_outstanding_credits_debits_widget.get('content'):
						content = [itm.get('id') for itm in move.invoice_outstanding_credits_debits_widget.get('content') if itm.get('journal_name') == payment ]
						if content:
							move.js_assign_outstanding_line(content[0])
							if move.id in posted_moves:
								posted_moves.remove(move.id)

		for move in sorted_move_objs:
			if move.id in posted_moves:
				move.button_draft()
				move.posted_before = False
				move.name = '/'
				move.sequence_prefix = ''

	# While Posting an invoice update current login user as a sales person
	def action_post(self):
		for move in self:
			if move.move_type in ['out_invoice','out_refund']:
				move.invoice_user_id = self.env.user.id
		res = super(InheritAccountMove,self).action_post()
		return res
	
	# Action Bulk Reset to Draft
	def bulk_reset_to_draft(self):
		for move in self:
			move.button_draft()
	
				
class InheritAccountMoveLine(models.Model):
	_inherit = "account.move.line"


	payment_state = fields.Selection([('paid','Paid'),('partially_paid','Partial'),('not_paid','Not Paid')],compute="get_invoice_line_payment_state",string="Payment Status",store=True)
	fees_for_id = fields.Many2one('fees.for', string="Fees for", track_visibility='always')
	semester_id = fields.Many2one('semester.master',related="move_id.semester_id",store=True,string="Semester")
	batch_id = fields.Many2one('batch.courses.master',related="move_id.batch_id",store=True,string="Batch")
	course_year = fields.Integer(string="Course Year")
	start_date = fields.Date(string="Start Date")
	end_date = fields.Date(string="End Date")
	due_date = fields.Date(string="Due Date")
	student_id = fields.Many2one('student.details',string="Student")
	course_id = fields.Many2one('courses.master',string="Course")
	priority = fields.Integer(default=0, string="Priority")
	is_hostel = fields.Boolean(related="product_id.hostel_ok",string="Is hostel?")
	paid_amount = fields.Float(string="Paid Amount",compute="get_invoice_line_paid_amount",store=True)
	payment_ref_ids = fields.Many2many('account.payment',string="Reconciled Payments",compute="get_invoice_line_paid_amount",store=True)
	is_concession = fields.Boolean(string="Is Concession?")


	@api.model
	def create(self,vals):
		if vals.get('display_type') == 'payment_term':
			print('Term lines')
		res = super(InheritAccountMoveLine,self).create(vals)
		return res


	def action_custom_create_invoice(self):
		if self.move_id.one_time_fee_id:
			raise UserError(_('This action is not possible because this invoice is a One Time Fees'))
		if len(self.move_id.invoice_line_ids) > 1 and self.move_id.payment_state == 'not_paid' and self.move_id.state in ['draft','posted'] and self.move_id.payment_state == 'not_paid' and self.move_id.move_type == 'out_invoice':
			parent_move = self.move_id
			new_move_obj = self.move_id.copy()
			new_move_obj.button_draft()
			new_move_obj.invoice_line_ids = [(6,0,[])]
			self.move_id = new_move_obj.id
			new_move_obj.parent_invoice_id = parent_move.id
			parent_move.message_post(body=_(f"Line wise payment initiated for {self.name}, New Collection ref {new_move_obj.name}"))
			return {
				'name': 'Collection View',
				'type': 'ir.actions.act_window',
				'res_model': 'account.move',
				'res_id': new_move_obj.id,
				# 'view_id': invoice_form_view.id,
				'view_mode': 'form',
				'target': 'current',
			}
			# return new_move_obj.action_register_payment()
		else:
			if len(self.move_id.invoice_line_ids) == 1:
				return self.move_id.action_register_payment()
			if self.move_id.payment_state == 'not_paid':
				raise ValidationError(_("Cannot do line wise payment For which payment is initiated!"))
			if self.move_id.move_type != 'out_invoice':
				raise ValidationError(_("Cannot do line wise payment For other than Collections!"))
			if self.move_id.state != 'not_paid':
				raise ValidationError(_("Line wise payment will work when the payment state is not paid in the invoice level!"))

	# Convert Payment dates as str 
	def get_dates_as_str(self):
		string_dates = ', '.join(payment.date.strftime('%d-%b-%Y') for payment in self.payment_ref_ids) or ''
		return string_dates
	

	def get_payment_names(self):
		names = ', '.join(self.payment_ref_ids.mapped('name'))
		return names
	
	# We use this method in future 
	def get_reconciled_data(self):
		reconciled_vals = []
		reconciled_partials = self.move_id._get_all_reconciled_invoice_partials()
		for reconciled_partial in reconciled_partials:
			counterpart_line = reconciled_partial['aml']
			if counterpart_line.move_id.ref:
				reconciliation_ref = '%s (%s)' % (counterpart_line.move_id.name, counterpart_line.move_id.ref)
			else:
				reconciliation_ref = counterpart_line.move_id.name
			if counterpart_line.amount_currency and counterpart_line.currency_id != counterpart_line.company_id.currency_id:
				foreign_currency = counterpart_line.currency_id
			else:
				foreign_currency = False

			reconciled_vals.append({
				'name': counterpart_line.name,
				'journal_name': counterpart_line.journal_id.name,
				'amount': reconciled_partial['amount'],
				'currency_id': self.move_id.company_id.currency_id.id if reconciled_partial['is_exchange'] else reconciled_partial['currency'].id,
				'date': counterpart_line.date,
				'partial_id': reconciled_partial['partial_id'],
				'account_payment_id': counterpart_line.payment_id.id,
				'payment_method_name': counterpart_line.payment_id.payment_method_line_id.name,
				'move_id': counterpart_line.move_id.id,
				'ref': reconciliation_ref,
				# these are necessary for the views to change depending on the values
				'is_exchange': reconciled_partial['is_exchange'],
				'amount_company_currency': formatLang(self.env, abs(counterpart_line.balance), currency_obj=counterpart_line.company_id.currency_id),
				'amount_foreign_currency': foreign_currency and formatLang(self.env, abs(counterpart_line.amount_currency), currency_obj=foreign_currency)
			})
		
		return reconciled_vals


	# Compute method to get the payment status of invoice line
	@api.depends('move_id.amount_residual')
	def get_invoice_line_paid_amount(self):
		for line in self:
			content = line.move_id.invoice_payments_widget.get('content') if line.move_id.invoice_payments_widget else []
			# content = line.get_reconciled_data()
			payment_vals = {}
			for payment in reversed(content):
				if payment.get('account_payment_id'):
					key = str(payment.get('account_payment_id')).strip()
					if key in payment_vals.keys():
						payment_vals[key]['amount'] = payment_vals.get(key)['amount'] + payment.get('amount')
					else:
						payment_vals[key] = {'id':payment.get('account_payment_id'),'amount':payment.get('amount'),'':payment.get('date')}
			
			processed_line = line.move_id.custom_priority_sort(line.move_id.invoice_line_ids)
	
			if line.display_type == 'product':
				paid_amount = line.move_id.amount_total - line.move_id.amount_residual
				if line.move_id.payment_state == 'paid':
					line.paid_amount = line.price_total
				elif line.move_id.payment_state == 'partial':
					
					for sub_line in processed_line:
						if paid_amount > 0:
							paid_amount -= sub_line.price_total
							if line.id == sub_line.id:
								if paid_amount >= 0:
									line.paid_amount = line.price_total
								else:
									line.paid_amount = round(line.price_total + paid_amount,2)
						else:
							if line.id == sub_line.id:
								line.paid_amount = 0.0
				elif line.move_id.payment_state == 'not_paid':
					line.paid_amount = 0.0
			else:
				line.paid_amount = 0.0

			if payment_vals:
				line.get_compute_map_payment_line(payment_vals,[{'id':line_1,'amount':line_1.price_subtotal}for line_1 in processed_line])
			else:
				line.payment_ref_ids = False


	# Compute invoice line payment state
	@api.depends('move_id.amount_residual')
	def get_invoice_line_payment_state(self):
		for line in self:
			paid_amount = line.move_id.amount_total - line.move_id.amount_residual
			line.payment_state = 'not_paid'
			processed_line = line.move_id.custom_priority_sort(line.move_id.invoice_line_ids)
			
			if line.move_id.payment_state == 'paid':
				line.payment_state = 'paid'
				# line.paid_amount = line.price_total
			elif line.move_id.payment_state == 'partial':
				for sub_line in processed_line:
					if paid_amount > 0:
						paid_amount -= sub_line.price_total
						if line.id == sub_line.id:
							if paid_amount >= 0:
								line.payment_state = 'paid'
								# line.paid_amount = line.price_total
							else:
								line.payment_state = 'partially_paid'
								# line.paid_amount = round(line.price_total + paid_amount,2)
					else:
						if line.id == sub_line.id:
							line.payment_state = 'not_paid'
							# line.paid_amount = 0.0
			elif line.move_id.payment_state == 'not_paid':
				line.payment_state = 'not_paid'
				# line.paid_amount = 0.0

	def get_compute_map_payment_line(self,var_1,var_2):
		result = []
		# Iterate through invoice lines and distribute payments
		for line in var_2:
			line_amount = line['amount']
			payment_ids = []

			payments_to_remove = []  # Keep track of payments to remove from var_1
			for payment_key, payment_info in var_1.items():
				payment_amount = payment_info['amount']
				payment_id = payment_info['id']

				if payment_amount >= line_amount:
					payment_ids.append(payment_id)
					payment_info['amount'] -= line_amount
					line_amount = 0
					break
				else:
					payment_ids.append(payment_id)
					line_amount -= payment_amount
					payments_to_remove.append(payment_key)

			for payment_key in payments_to_remove:
				del var_1[payment_key]

			result.append((line, payment_ids))
			list_of_payment_ids = [(6, 0, payment_ids)]
			line.get('id').payment_ref_ids = list_of_payment_ids

	
class InheritPaymentRegister(models.TransientModel):
	_inherit = 'account.payment.register'


	# mode_of_payment = fields.Many2one('mode.of.payment',string="Mode of Payment")
	# dd_bank = fields.Char(string="DD Bank")
	# dd_no = fields.Char(string="DD No")
	# dd_date = fields.Date(string="DD Date")

	is_custom_method = fields.Boolean(string="Is Custom Payment Method")
	payment_method_bank = fields.Char(string="Payment Method Bank",copy=False)
	payment_method_number = fields.Char(string="Payment Method No",copy=False)
	payment_method_date = fields.Date(string="Payment Method Date",copy=False)


	@api.onchange('payment_method_line_id')
	def onchange_payment_method_line_id(self):
		if self.payment_method_line_id:
			if self.payment_method_line_id.name in ['Cheque','DD']:
				self.is_custom_method = True
			else:
				self.is_custom_method = False


	def _prepare_payment_vals(self, invoices):
		res = super(InheritPaymentRegister, self)._prepare_payment_vals(invoices)
	
		# Updating values in case of Multi payments
		res.update({
			# 'mode_of_payment': self.mode_of_payment,
			'payment_method_bank': self.payment_method_bank,
			'payment_method_number': self.payment_method_number,
			'payment_method_date': self.payment_method_date,
		})
		return res


	# Overriding Payment create action for student fee invoices
	def action_create_payments(self):
		move_objs = self.env['account.move']
		partner_ids = False
		line_invoice = False
		parent_invoice = False

		if self.env.context.get('active_model') == 'account.move':
			move_objs = move_objs.browse(self.env.context.get('active_ids'))
		
		if len(move_objs) == 1:
			if move_objs.one_time_fee_id:
				if move_objs.last_payment:
					obj =self.env['account.move'].search([('semester_id','=',move_objs.semester_id.id),('fees_for_id','=',move_objs.fees_for_id.id),('partner_id','=',move_objs.partner_id.id),('payment_state','!=','paid'),('last_payment','=',False)])
					if obj:
						raise ValidationError(_("Please completed the rest of the payment before paying this."))
				if move_objs.amount_total != self.amount:
					raise ValidationError(_("Since its an One time fees. Please pay the actual amount."))
		else:
			for i in move_objs:
				if i.one_time_fee_id:
					raise ValidationError(_(f"{i.name} an One time fees. One time fees should be paid individually"))

		
		if move_objs:
			partner_ids = move_objs.mapped('partner_id')
			move_types = move_objs.mapped('move_type')
			move_is_true = move_objs.mapped('is_true')
			line_invoice = move_objs.filtered(lambda x:x.parent_invoice_id.id)
			parent_invoice = move_objs.filtered(lambda x:x.line_invoices_ids)
		
		if parent_invoice and line_invoice:
			raise ValidationError(_("Don't process Parent inovices and Line invoices together!"))

		if move_types and move_types[0] == 'out_invoice' and partner_ids and len(partner_ids.ids) > 1:
			raise ValidationError(f"Please register a Payment for one person at a time. Cannont do for different users!")
		
		if move_is_true and len(set(move_is_true))>1:
			raise ValidationError(f"Please don't process the invoice which is related to student fees together with normal invoices!")
		
		if len(move_objs) == 1 and not parent_invoice and line_invoice:
			if move_objs.amount_total != self.amount:
				raise ValidationError(_("Please register a Actual Amount, Hence its a Line wise collection!"))
		
		if move_types and move_types[0] == 'out_invoice' and move_is_true[0] == True and not line_invoice:
			if move_types and move_types[0] == 'out_invoice':

				payments = self._create_payments()
				
				for payment in payments:
					payment.action_draft()
					payment.action_post()
					payment.ref = ''

				for move in move_objs:
					move.prepare_move_lines_by_term_and_priority_wise(payments)
				report_action = self.env.ref('fees_management.action_report_fee_payment_receipt').report_action(payments)
				report_action['close_on_report_download'] = True
				return report_action
		else:
			res = super(InheritPaymentRegister,self).action_create_payments()
			return res
		
	def _create_payments(self):
		res = super(InheritPaymentRegister,self)._create_payments()
		for payment in res:
			# payment.mode_of_payment = self.mode_of_payment.id
			payment.payment_method_bank = self.payment_method_bank
			payment.payment_method_number = self.payment_method_number
			payment.payment_method_date = self.payment_method_date
		return res

class AccountPayment(models.Model):
	_inherit = "account.payment"

	def get_total_invoice(self):
		return len(self.reconciled_invoice_ids.ids)

	def get_total_residual(self):
		res = 0.00
		total = 0.00
		for i in self.reconciled_invoice_ids.ids:
			obj = self.env['account.move'].browse(i)
			res += obj.amount_residual
			total += obj.amount_total
		if res == 0.00:
			return (total,False)
		return (total,res)
		
	def _get_reconciled_invoices_part(self):
		paid = self.amount
		if not self.reconciled_invoice_ids:
			student_id = self.env['student.details'].search([('aadhar_no','=',self.partner_id.aadhar_no)],limit=1)
			utc_now = datetime.now(pytz.utc)
			ist = pytz.timezone('Asia/Kolkata')
			ist_now = utc_now.astimezone(ist)
			formatted_time = ist_now.strftime('%Y-%m-%d %I:%M:%S %p')
			acc=""
			if student_id.accomodation_check_box == 'hosteler':
				acc = "Hosteler"
			else:
				acc = "Dayscholar"	
			inv_detail = {'name':'',
				'cashier':self.env.user.name,
				'datetime':formatted_time,
				'batch':student_id.batch_id.name,
				'role_no':student_id.role_no,
				'course':student_id.courses_id.degree_id.name,
				'barcode':student_id.barcode_no,
				'quota':student_id.quota_id.name,
				'accomodation':acc}
			
			return (False,inv_detail,False)


		line_list = []
		print("len(self.reconciled_invoice_ids.ids) =",len(self.reconciled_invoice_ids.ids))
		if len(self.reconciled_invoice_ids.ids)>1:
			
			for i in self.reconciled_invoice_ids.ids:

				move_obj = self.env['account.move'].browse(i)

				utc_now = datetime.now(pytz.utc)
				ist = pytz.timezone('Asia/Kolkata')
				ist_now = utc_now.astimezone(ist)
				formatted_time = ist_now.strftime('%Y-%m-%d %I:%M:%S %p')	
				acc=""
				if move_obj.details_id.accomodation_check_box == 'hosteler':
					acc = "Hosteler"
				else:
					acc = "Dayscholar"				
				inv_detail = {'name':move_obj.name,
					'cashier':self.env.user.name,
					'datetime':formatted_time,
					'batch':move_obj.batch_id.name,
					'role_no':move_obj.details_id.role_no,
					'course':move_obj.details_id.courses_id.degree_id.name,
					'barcode':move_obj.details_id.barcode_no,
					'quota':move_obj.details_id.quota_id.name,
					'accomodation':acc}
			

				content = move_obj.invoice_payments_widget.get('content') if move_obj.invoice_payments_widget else False
				sorted_payment_data = sorted(content, key=lambda x: x['ref'])
				total_paid_sum = 0.0
				for i in sorted_payment_data:
					if i.get('account_payment_id') == self.id:
						break
					else:
						total_paid_sum += i.get('amount')
				sorted_lines_by_priority = move_obj.custom_priority_sort(move_obj.invoice_line_ids)
				for line in sorted_lines_by_priority:
					if line.payment_state != 'not_paid':
						if total_paid_sum > 0:
							if  total_paid_sum >= line.paid_amount:
								total_paid_sum -= line.paid_amount
								continue
							else:
								if paid >= line.paid_amount:
									paid -= line.paid_amount-total_paid_sum
									line_list.append({'name':line.product_id.name,'price_total':line.paid_amount-total_paid_sum,'term':str(line.fees_for_id.name),'inv_name':line.move_id.name})
									total_paid_sum=0
									# paid=  -(line.paid_amount-total_paid_sum)
									continue
								else:
									line_list.append({'name':line.product_id.name,'price_total':paid,'term':str(line.fees_for_id.name),'inv_name':line.move_id.name})
									paid -= paid
									break
						if paid > 0:
							if line.paid_amount > paid:
								line_list.append({'name':line.product_id.name,'price_total':paid,'term':str(line.fees_for_id.name)})
								paid -= paid
							else:
								line_list.append({'name':line.product_id.name,'price_total':line.paid_amount,'term':str(line.fees_for_id.name)})
								paid -= line.paid_amount
					else:
						continue
				# line_list.reverse()

			if paid >0:
				return (line_list,inv_detail,paid)
			
			return (line_list,inv_detail,False)
		
		total_paid_sum = 0.0
		obj=self.reconciled_invoice_ids

		content = obj.invoice_payments_widget.get('content') if obj.invoice_payments_widget else False
		sorted_payment_data = sorted(content, key=lambda x: x['ref'])
		total_paid_sum = 0.0
		for i in sorted_payment_data:
			if i.get('account_payment_id') == self.id:
				break
			else:
				total_paid_sum += i.get('amount')
		utc_now = datetime.now(pytz.utc)
		ist = pytz.timezone('Asia/Kolkata')
		ist_now = utc_now.astimezone(ist)
		formatted_time = ist_now.strftime('%Y-%m-%d %I:%M:%S %p')
		acc=""
		if obj.details_id.accomodation_check_box == 'hosteler':
			acc = "Hosteler"
		else:
			acc = "Dayscholar"	
		inv_detail = {'name':obj.name,
			'cashier':self.env.user.name,
			'datetime':formatted_time,
			'batch':obj.batch_id.name,
			'role_no':obj.details_id.role_no,
			'course':obj.details_id.courses_id.degree_id.name,
			'barcode':obj.details_id.barcode_no,
			'quota':obj.details_id.quota_id.name,
			'accomodation':acc}
		

		paid = self.amount
		inv_lines = obj.custom_priority_sort(obj.invoice_line_ids)
		list_line = []
		for i in inv_lines:
			list_line.append({'id':i.id,'name':i.product_id.name,'price_total':i.paid_amount,'term':str(i.fees_for_id.name),'inv_name':i.move_id.name})
			
		if total_paid_sum >0:
			new_list_line = []  
			for line in list_line:
				temp = line.get('price_total') - total_paid_sum
				if temp > 0:
					line['price_total'] = temp
					total_paid_sum = 0
				elif temp < 0:
					total_paid_sum -= line.get('price_total')
				else:
					total_paid_sum = 0
				if temp > 0:
					new_list_line.append(line)
			list_line = new_list_line

		result_vals = []

		for res in list_line:
			temp = res.get('price_total') - paid
			if temp<0:
				result_vals.append(res)
				paid -= res.get('price_total')
				continue
			elif temp>0:
				res['price_total']=paid
				result_vals.append(res)
				paid = 0
				break
			else:
				result_vals.append(res)
				paid = 0
				break

		# for line in inv_lines:	
		# 	if total_paid_sum > 0:
		# 		print("total_paid_sum 1 =",total_paid_sum)
		# 		print("line.paid_amount 1 =",line.paid_amount)
		# 		if  total_paid_sum >= line.paid_amount:
		# 			total_paid_sum -= line.paid_amount
		# 			continue
		# 		else:
		# 			if paid >= line.paid_amount:
		# 				print("total_paid_sum 2 =",line.paid_amount-total_paid_sum)
		# 				# paid += total_paid_sum
		# 				paid -= line.paid_amount-total_paid_sum
		# 				line_list.append({'name':line.product_id.name,'price_total':line.paid_amount-total_paid_sum,'term':str(line.fees_for_id.name),'inv_name':line.move_id.name})
		# 				total_paid_sum=0
		# 				# paid=  -(line.paid_amount-total_paid_sum)
		# 				continue
		# 			else:
		# 				print("total_paid_sum 3 =",paid)
		# 				line_list.append({'name':line.product_id.name,'price_total':paid,'term':str(line.fees_for_id.name),'inv_name':line.move_id.name})
		# 				paid -= paid
		# 				break
		# 	if paid > 0:
		# 		if line.paid_amount > paid:
		# 			line_list.append({'name':line.product_id.name,'price_total':paid,'term':str(line.fees_for_id.name)})
		# 			paid -= paid
		# 		else:
		# 			line_list.append({'name':line.product_id.name,'price_total':line.paid_amount,'term':str(line.fees_for_id.name)})
		# 			paid -= line.paid_amount
		if paid >0:
			return (result_vals,inv_detail,paid)
		return (result_vals,inv_detail,False)
