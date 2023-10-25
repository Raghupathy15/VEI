# -*- coding: utf-8 -*-

{
    'name': 'Odoo16 Company master',
    'version': '16.0.1.1.0',
    'summary': """
        College master
    """,
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/company_view.xml',
        'views/trust_master_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}