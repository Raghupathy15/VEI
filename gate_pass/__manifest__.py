# -*- coding: utf-8 -*-
{
    'name': "Gate Pass",

    'summary': """
        Gate Pass""",

    'description': """
        Gate Pass
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','mail'],

    'data': [
        'security/ir.model.access.csv',
        'security/gate_pass_security.xml',
        # 'data/gate_pass_views.xml',
        'views/gate_pass_views.xml',
        'reports/gatepass_report.xml',
        'reports/gatepass_inwardreport.xml',
    ]
}
