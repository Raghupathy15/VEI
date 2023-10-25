# -*- coding: utf-8 -*-
{
    'name': "Custom Report",
    'summary': "Custom Report",
    'description': "Custom Report",
    'category': 'Account',
    'version': '16.0.1',
    'depends': ['base','account','account_extend', 'vg_colg', 'report_xlsx','web'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/report.xml',
        'wizard/report_templete.xml',
        'views/account_payment_view.xml',
        'wizard/consolidated_report.xml',
        'report/consolidated_pdf_report.xml'
    ],
}
