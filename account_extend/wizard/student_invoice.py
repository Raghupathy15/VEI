from odoo import fields, models, _
from odoo.exceptions import UserError
from datetime import datetime

class AccountReportGeneralLedger(models.TransientModel):
	_name = "student.fee.invoice"
	_description = "Student Fee Invoice"

	term_id = fields.Many2one('fees.for',string="Term",required=True)
	year = fields.Char(string="Batch Start Year",translate=False)

	def create_fee_invoice(self):
		student_ids = self.env['student.details'].search([('batch_start_year','=',self.year)])
		existing_student = []
		for student_obj in student_ids:
			if_exist = self.env['account.move'].search([('details_id','=',student_obj.role_no),('term_id','=',self.term_id.id),('is_true','=',True),('state','!=','cancel'),('payment_state','not in',('reversed','invoicing_legacy'))]) 
			if if_exist:
				existing_student.append(if_exist.details_id.role_no)
			else:
				fee_obj = self.env['fees.management'].search([('fees_for_id', '=', self.term_id.id),('state','=','approved')])
				partner_id = self.env['res.partner'].search([('aadhar_no','=',student_obj.aadhar_no)],limit=1)
				journal = self.env['account.journal'].search([('company_id', '=', self.env.company.id),('type', '=', 'sale')],limit=1)
				fee_lines = []
				inv_lines = []
				for i in fee_obj.fees_ids:
					fee_val = {
						'product_id': i.product_id.id,
						'payment_type': i.payment_type,
						'priority': i.priority,
						'terms': i.terms,
						'amount': i.amount,
						'unpaid': i.amount
					}
					fee_lines.append((0, 0,fee_val))

					inv_val = {
						'product_id': i.product_id.id,
						'price_unit': i.amount,
						'tax_ids': [(6, 0, i.product_id.taxes_id.ids)],
					}
					if i.product_id.id:
						inv_lines.append((0, 0,inv_val))
				inv_vals = {
					'details_id':student_obj.id,
					'partner_id':partner_id.id,
					'is_true':True,
					'journal_id': journal.id,
					'invoice_date': datetime.now().date(),
					'date': datetime.now().date(),
					'term_id':self.term_id.id,
					'move_type':'out_invoice',
					'course_year':fee_obj.course_year,
					'fee_manage_id':fee_obj.id,
					'degree_id':student_obj.degree_id.id,
					'course_id':student_obj.courses_id.id,
					'payment_state':'not_paid',
					'state':'draft',
					'fee_line_ids': fee_lines,
					'invoice_line_ids': inv_lines,
				}
				move_id = self.env['account.move'].sudo().create(inv_vals)
			if existing_student:
				raise UserError(_('Invoices for the following roll number already exist %s ') % (existing_student))




		
