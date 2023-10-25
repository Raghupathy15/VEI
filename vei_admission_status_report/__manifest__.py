# -*- coding: utf-8 -*-
{
    'name': "Admission status Report",
    'summary': "Admission status Report",
    'description': "Admission status Report",
    'category': 'custom',
    'version': "16.0.0.1",
    'depends': ['vg_colg'],
    'data': [
        'security/ir.model.access.csv',
        'views/admission_status_report.xml',
    ],
    'installable': True,
    'application': False,
}
