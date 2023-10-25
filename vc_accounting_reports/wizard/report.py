from odoo import models, fields, api, exceptions, _

# Report 1
class DailyCounterWiseReport(models.TransientModel):
	_name = 'daily.counter.wise.report'
	_description = 'Daily Counter Wise Report'
	
	counter_ids = fields.Many2many('counter.master',string="Counter Number")
	from_date = fields.Date(string="From Date")
	to_date = fields.Date(string="To Date")
	company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, default=lambda self: self.env.company)

	def action_print_pdf(self):
		data = {
			'from_date' : self.from_date,
			'to_date' : self.to_date,
			'counter_ids' : self.counter_ids.ids,
			'company_id' : self.company_id.id,
			'id' : self.id,
		}
		report_action = self.env.ref('vc_accounting_reports.action_daily_counter_wise_report_report_pdf').report_action(
			self, data=data)
		report_action['close_on_report_download'] = True
		return report_action

	def action_print_excel(self):
		print("=============action_print_excel=========")
		data = {
			'from_date': self.from_date,
			'to_date': self.to_date,
			'counter_ids': self.counter_ids.ids,
			'company_id': self.company_id.id,
			'id': self.id,
		}
		return self.env.ref('vc_accounting_reports.report_daily_counter_xlsx').report_action(self, data=data)


# Report 2
class DailyCounterWiseDetailedReport(models.TransientModel):
	_name = 'daily.counter.wise.detailed.report'
	_description = 'Daily Counter Wise Detailed Report'

	counter_ids = fields.Many2many('counter.master', string="Counter Number")
	from_date = fields.Date(string="From Date")
	to_date = fields.Date(string="To Date")
	company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
								 default=lambda self: self.env.company)

	def action_print_pdf(self):
		data = {
			'from_date': self.from_date,
			'to_date': self.to_date,
			'counter_ids': self.counter_ids.ids,
			'company_id': self.company_id.id,
			'id': self.id,
		}
		report_action = self.env.ref('vc_accounting_reports.action_daily_counter_wise_detailed_report_report_pdf').report_action(
			self, data=data)
		report_action['close_on_report_download'] = True
		return report_action

	def action_print_excel(self):
		print("=============action_print_excel=========")
		data = {
			'from_date': self.from_date,
			'to_date': self.to_date,
			'counter_ids': self.counter_ids.ids,
			'company_id': self.company_id.id,
			'id': self.id,
		}
		return self.env.ref('vc_accounting_reports.report_daily_counter_detailed_xlsx').report_action(self, data=data)
