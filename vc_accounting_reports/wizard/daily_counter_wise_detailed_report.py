from odoo import api, fields, models, _
from datetime import datetime, date

class DailyCounterDetailedReportXlsx(models.AbstractModel):
    _name = 'report.vc_accounting_reports.dc_detailed_report'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Daily Counter Wise Detailed Report'

    def generate_xlsx_report(self, workbook, data, objects):
        print("=================generate_xlsx_report===================",data)
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 15.0'})
        sheet = workbook.add_worksheet(_('Daily Counter Wise Detailed Report'))

        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        sheet.set_column(0, 0, 6)
        sheet.set_column(1, 1, 25)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 20)
        sheet.set_column(4, 4, 28)
        sheet.set_column(5, 5, 20)
        sheet.set_column(6, 6, 20)
        sheet.set_column(7, 7, 20)
        sheet.set_column(8, 8, 20)

        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '16px'})
        cell_format = workbook.add_format({'font_size': '12px', 'bold': True})
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy', 'font_size': '12px', 'bold': False,'align': 'left'})
        bold = workbook.add_format({'bold': False})
        bold_number = workbook.add_format({'bold': False,'align': 'right'})
        title_style = workbook.add_format({'bold': True,
                                           'bg_color': '#FFFFCC',
                                           'bottom': 1})

        sheet_title = [
            _('Sr No.'),
            _('Student Name'),
            _('Course'),
            _('Year'),
            _('Bank'),
            _('Number'),
            _('Date'),
            _('Amount'),
        ]

        # sheet.set_row(0, None, None, {'collapsed': 1})
        sheet.merge_range('B3:G4', 'Daily Counter Wise Detailed Report', head)
        sheet.write_row(6, 0, sheet_title, cell_format)

        domain = [('company_id', '=', data['company_id']), ('invoice_date', '>=', data['from_date']),
                  ('invoice_date', '<=', data['to_date'])]
        counter_name = ''
        if data['counter_ids']:
            domain.append(('counter_id', 'in', data['counter_ids']))
            counter_name_list = self.env['counter.master'].sudo().browse(data['counter_ids']).mapped('name')
            counter_name = ','.join(counter_name_list)

        moves_name = self.env['account.move'].sudo().search(domain).mapped('name')
        payments = self.env['account.payment'].sudo().search([('ref', 'in', moves_name)])

        i = 7
        count = 1
        total = 0
        if payments:
            for payment in payments:
                invoice = self.env['account.move'].sudo().search([('name','=',payment.ref)],limit=1)
                sheet.write(i, 0, count, bold)
                sheet.write(i, 1, payment.partner_id.name or ' ', bold)
                sheet.write(i, 2, invoice.degree_level_id.name or ' ', bold)
                sheet.write(i, 3, invoice.course_year or ' ', bold)
                sheet.write(i, 4, payment.payment_method_bank or ' ', bold)
                sheet.write(i, 5, payment.payment_method_number or ' ', bold)
                sheet.write(i, 6, payment.payment_method_date or ' ', date_format)
                sheet.write(i, 7, '%.2f' % payment.amount or 0, bold_number)
                i = i + 1
                count = count + 1
                total = total + payment.amount
            sheet.write(i, 6, 'Total', cell_format)
            sheet.write(i, 7, '%.2f' % total or 0, cell_format)



