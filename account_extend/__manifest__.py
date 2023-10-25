{
    'name': "Invoice Extend",
    'summary': """
        Account Extend
    """,
    'description': """
        Customisation in Invoicing Module.
    """,
    'author': "Arun",

    'category': 'e',
    'version': '15.0.1.0',
    'license': 'OPL-1',
    'depends': ['base','account','vg_colg','fees_management'],
    'data': [
        'views/account_move.xml',
        'security/ir.model.access.csv',
        'views/counter_master.xml',
        'views/no_due_generation.xml',
        'views/fees_management.xml',
        'views/chart_of_account.xml',
        'wizard/student_invoice.xml',
        'wizard/account_payment.xml',
        # 'data/account.account.template.csv',
    ],
    'installable': True,
    'auto_install': False,
}
