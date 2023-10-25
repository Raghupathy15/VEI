from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import ValidationError, UserError


class TransferCollegeWizard(models.TransientModel):

    _name = "transfer.college.wizard"
    _description = "Transfer College wizard"

    student_id = fields.Many2one('student.details', string='Student Name')
    current_company_id = fields.Many2one('res.company', string='Current College')
    to_company_id = fields.Many2one('res.company', string="Transfer College To", required=True)
    remarks = fields.Html(string="Remarks", required=True)

    def action_transfer_college(self):
        self.student_id.company_id = self.to_company_id.id


class TransferCourcesWizard(models.TransientModel):

    _name = "transfer.courses.wizard"
    _description = "Transfer Courses wizard"

    student_id = fields.Many2one('student.details', string='Student Name')
    courses_id = fields.Many2one('courses.master', string="Current Courses")
    degree_id = fields.Many2one('degree.master', string="Current Degree")
    to_degree_id = fields.Many2one('degree.master', string="Transfer Degree To", required=True)
    to_courses_id = fields.Many2one('courses.master', string="Transfer Courses To", required=True)
    remarks = fields.Html(string="Remarks", required=True)

    def action_transfer_courses(self):
        self.student_id.write({
            'degree_id': self.to_degree_id.id,
            'courses_id': self.to_courses_id.id
        })