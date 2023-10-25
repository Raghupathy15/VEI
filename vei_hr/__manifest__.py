# -*- coding: utf-8 -*-
{
    'name': "VEI HR Extend",
    'summary': "VEI HR Extend",
    'description': "VEI HR Extend",
    'category': 'custom',
    'version': "16.0.0.1",
    'depends': ['hr','vg_colg'],
    'data': [
        'data/ir_cron_data.xml',
        'data/mail_template_data.xml',
        'views/department_view.xml',
    ],
    'installable': True,
    'application': False,
}
