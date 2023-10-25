# -*- coding: utf-8 -*-
{
    'name': "Customer QR",
    'summary': "Customer QR",
    'description': "Customer QR",
    'author': "Ciberon",
    'version': '15.0.0.1',
    'depends': ['base'],
    'data': [
        'report/paperformat.xml',
        'report/report.xml',
        'report/template.xml',
        'views/views.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'customer_qr/static/src/scss/custom.scss',
        ],
    },
    'installable': True,
    'application': False,
}


