from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from datetime import date, datetime

class InheritAccountMoveLine(models.Model):
	_inherit = "account.move.line"

	def datetime_now(self):
		vals = {'company_name':self.env.company.name,
	  			'datetime':datetime.now().replace(microsecond=0)}
		return vals

	def _get_term(self):
		obj = self.env['account.move.line'].search([('id','in',self.env.context.get('active_ids', []))])
		final = ""
		term = []
		for i in obj:
			if i.fees_for_id.name not in term:
				term.append(i.fees_for_id.name)
		if len(term)>1:
			separator = ","  # The separator you want to use
			final = separator.join(term)
		else:
			final = term[0]
			return final
			
		
	def _get_invoices_lines(self):
		obj = self.env['account.move.line'].search([('id','in',self.env.context.get('active_ids', []))])
		final_obj = []
		for i in obj:
			val = {'id':i.move_id.details_id.role_no,
					'name':i.move_id.name,
					'grade':i.course_id.degree_id.name,
					'description':i.product_id.name,
					'amount':i.price_total,
					'paid':i.paid_amount,
					'consession':'-',
					'balance':i.price_total-i.paid_amount,
					'number':i.move_id.name,
					'date':i.move_id.invoice_date}
			final_obj.append(val)
		sorted_final_obj = sorted(final_obj, key=lambda x: x['id'])
		return sorted_final_obj

	def print_pdf(self):
		data = {
			'company_id': self.company_id.id,
			'line_ids': self.env.context.get('active_ids', []),
		}
		report_action = self.env.ref('vc_accounting_reports.action_consolidated_report_pdf').report_action(
			self, data=data)
		report_action['close_on_report_download'] = True
		return report_action