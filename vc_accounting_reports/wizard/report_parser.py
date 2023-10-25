import datetime
from odoo import api, models, _


# Report - 1
class ReportRenderDailyCounterWiseReport(models.AbstractModel):
    _name = 'report.vc_accounting_reports.dc_wise_report_templete'
    _description = 'Daily Counter Wise Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env['daily.counter.wise.report'].browse(data['id'])
        domain = [('company_id', '=', data['company_id']),('invoice_date', '>=', data['from_date']),
                                                                ('invoice_date', '<=', data['to_date'])]
        counter_name = ''
        if data['counter_ids']:
            domain.append(('counter_id', 'in', data['counter_ids']))
            counter_name_list = self.env['counter.master'].sudo().browse(data['counter_ids']).mapped('name')
            counter_name = ','.join(counter_name_list)

        moves = self.env['account.move'].sudo().search(domain)

        return {
            'doc_ids': docids,
            'doc_model': model,
            'docs': docs,
            'moves': moves,
            'counter_name': counter_name,
        }


# Report - 2
class ReportRenderDailyCounterWiseDetailedReport(models.AbstractModel):
    _name = 'report.vc_accounting_reports.dc_detailed_report_temp'
    _description = 'Daily Counter Wise Detailed Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env['daily.counter.wise.detailed.report'].browse(data['id'])
        domain = [('company_id', '=', data['company_id']),('invoice_date', '>=', data['from_date']),
                                                                ('invoice_date', '<=', data['to_date'])]
        counter_name = ''
        if data['counter_ids']:
            domain.append(('counter_id', 'in', data['counter_ids']))
            counter_name_list = self.env['counter.master'].sudo().browse(data['counter_ids']).mapped('name')
            counter_name = ','.join(counter_name_list)

        moves_name = self.env['account.move'].sudo().search(domain).mapped('name')
        payments = self.env['account.payment'].sudo().search([('ref','in',moves_name)])

        return {
            'doc_ids': docids,
            'doc_model': model,
            'docs': docs,
            'payments': payments,
            'counter_name': counter_name,
        }

