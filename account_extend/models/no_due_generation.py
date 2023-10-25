from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta


class NoDueGeneration(models.Model):
	_name = "no.due.gen"
	
	name = fields.Char('Name')
	student_detail_id = fields.Many2one('student.details',string='Student Details')
	course_id = fields.Many2one('courses.master',string='Course')
	degree_id = fields.Many2one('degree.master',string='Degree')
	course_year = fields.Integer(string="Course Year")
	company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, default=lambda self: self.env.company)
	

