from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import format_time

class HrEmployeeEducation(models.Model):
    _name = "employee.education.line"

    name = fields.Char(string='Institution')
    certification = fields.Char(string='Certification')
    percentage = fields.Char(string='Percentage/CGPA')
    emp_id = fields.Many2one('hr.employee',string='Employee Id')
    education_doc = fields.Binary(string="Attachments")
    note = fields.Text('Internal Notes')

class HrEmpWrokExperience(models.Model):
    _name = "employee.work.line"

    name = fields.Char(string='Company Name')
    note = fields.Text('Description')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    job_role = fields.Char(string='Role')
    city = fields.Char(string='City')
    emp_id = fields.Many2one('hr.employee',string='Employee Id')
    work_doc = fields.Binary(string="Attachments")

class HrEmpExtraActivity(models.Model):
    _name = "employee.activity.line"

    name = fields.Selection(selection=[
		('events', 'Events'),
        ('paper', 'Paper Presentations'),
        ('symposiums', 'Symposiums Attended'),
        ('publications', 'Publications'),
        ('awards', 'Awards'),
        ('membership', 'Membership'),
        ('certifications', 'Certifications and Courses'),
        ('funding', 'Funding to College'),
        ('consulting', 'Consulting activities'),
        ('seminar', 'Seminar'),
        ('wrokshops', 'Wrokshops'),
        ('conference', 'Conference'),
        ('other', 'Other')], string='Name',tracking=True,copy=False)
    act_date = fields.Date(string='Date')
    note = fields.Text('Description')
    venue = fields.Date(string='Venue')
    topic = fields.Date(string='Topic')
    emp_id = fields.Many2one('hr.employee',string='Employee Id')
    work_doc = fields.Binary(string="Attachments")

class HrEmpidproof(models.Model):
    _name = "id.proof.line" 

    name = fields.Selection(selection=[
		('aadhar', 'Aadhar Card'),
        ('pan ', 'PAN Card'),
        ('birth ', 'Birth Certificate'),
        ('voter ', 'Voter ID'),
        ('passport ', 'Passport'),
        ('driver ', 'Drivers License '),
        ('other', 'Other')], string='Name',tracking=True,copy=False)
    number = fields.Char(string='ID Number')
    emp_id = fields.Many2one('hr.employee',string='Employee Id')
    withdrawn_id = fields.Many2one('certificate.withdrawn')
    id_doc = fields.Binary(string="Attachments")

class HrEmployeeReferral(models.Model):
    _name = "empl.referral" 

    type = fields.Selection(selection=[
		('student', 'Student'),
        ('employee ', 'Employee')], string='Type',tracking=True,copy=False)
    name = fields.Char(string='ID Number',required=True)
    emp_id = fields.Many2one('hr.employee',string='Employee Id')
    join_date = fields.Date('Date of joining')
    note = fields.Text('Internal Notes')

class HrEmployeeReferral(models.Model):
    _name = "employee.dedcution" 

    # type = fields.Selection(selection=[
	# 	('deduction', 'Deduction'),
    #     ('allowance ', 'Allowance')], string='Type',tracking=True,copy=False)
    rule_id = fields.Many2one('hr.salary.rule',string='Salary Rule',required=True)
    emp_id = fields.Many2one('hr.employee',string='Employee Id')
    fixed_amount = fields.Float('Amount')


    



















