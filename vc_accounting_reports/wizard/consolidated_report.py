from odoo import models, fields, api, exceptions, _

class ConsolidatedPaymentReport(models.TransientModel):
	_name = 'consolidated.payment.report'
	_description = 'Consolidated Payment Report'

	from_date = fields.Date(string="From Date")
	to_date = fields.Date(string="To Date")
	company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
								 default=lambda self: self.env.company)

	def action_print_pdf(self):
		data = {
			'company_id': self.company_id.id,
			'id': self.id,
		}
		report_action = self.env.ref('vc_accounting_reports.action_consolidated_report_pdf').report_action(
			self, data=data)
		report_action['close_on_report_download'] = True
		return report_action


	# def get_payment_lines(self,from_date,to_date,company_id):
    #     inv_line = self.env['account.move.line'].search([('start_date','=','from_date'),('end_date','=','to_date'),('company_id','=',company_id)])
    #     for i in inv_line