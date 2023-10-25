{
    'name': "Employee Extend",
    'summary': """
        Employee Extend
    """,
    'description': """
        Customisation in Employee Module.
    """,
    'author': "Arun",

    'category': 'e',
    'version': '15.0.1.0',
    'license': 'OPL-1',
    'depends': ['base','hr','hr_attendance','hostel_management','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_extend.xml',
        'views/certificate_view.xml',
        'views/hr_employee_line.xml',
        'views/hr_employee_extend.xml',
        'views/hr_employee_type.xml',
        'views/hostel_inherit.xml',
        'views/campus_master.xml'
    ],
    'installable': True,
    'auto_install': False,
}
