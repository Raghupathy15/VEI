{
    'name': "HR Extend",
    'summary': """
        HR Extend
    """,
    'description': """
        Customisation in HR Module.
    """,
    'author': "Arun",

    'category': 'e',
    'version': '15.0.1.0',
    'license': 'OPL-1',
    'depends': ['base','account','hr','hr_contract','hr_attendance','hr_holidays','hr_payroll_community','ohrms_loan'],
    'data': [
        'views/hr_loan_seq.xml',
        'security/ir.model.access.csv',
        'views/hr_attendance.xml',
        'views/hr_leave.xml',
        'views/hr_loan.xml',
        'views/hr_loan_type.xml',
        'data/hr_salary_structure.xml',
        'data/hr_time_off.xml', 

    ],
    'installable': True,
    'auto_install': False,
}
