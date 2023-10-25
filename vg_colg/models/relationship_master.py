from odoo import fields, models, api


class RelationshipMaster(models.Model):
    _name = 'relationship.master'
    _description = 'Relationship Master'

    admission_id = fields.Many2one('admission.confirmation',string="Admission")
    admission_list_id = fields.Many2one('admission.list',string="Admission")
    student_id = fields.Many2one('student.details',string="Student Details")
    guardian_id = fields.Many2one('guardian.master',string="Parent/Guardian")
    status = fields.Char('Status')
    company = fields.Char('Company/school')
    mobile = fields.Char('Mobile No')
    whatsapp = fields.Char('Whatsapp No')
    occupation = fields.Char('Occupation')
    birth_place = fields.Char('Birth Place')
    aadhar_no = fields.Char('Aadhar No')
    phote = fields.Binary(string='Phote')
    visitor_allowed = fields.Boolean(string="Visitor Allowed")
    phote_name = fields.Char(string='Phote')
    attachment_id = fields.Many2one('ir.attachment',string="Photo")


class HealthInformationMaster(models.Model):
    _name = 'health.information.master'
    _description = 'Health Information Master'

    admission_id = fields.Many2one('admission.confirmation',string="Admission")
    admission_list_id = fields.Many2one('admission.list',string="Admission")
    student_id = fields.Many2one('student.details',string="Student Details")
    health_id = fields.Many2one('health.information',string="Name")
    description = fields.Char(string='Description')

class HealthInformation(models.Model):
    _name = 'health.information'
    _description = 'Health Information'

    name = fields.Char('Name')

class GuardianMaster(models.Model):
    _name = 'guardian.master'
    _description = 'Guardian Master'

    name = fields.Char('Name')


class DocumentName(models.Model):
    _inherit = 'document.name'

    degree_level_id = fields.Many2many('degree.level.master', string="Degree")
    courses_ids = fields.Many2many('courses.master', string="Courses")



