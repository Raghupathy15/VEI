from odoo import models,fields,api,_


class CourseAndCollege(models.Model):
    _name = "courses.college.master"
    _desc = "Used to map the course and college"
    _rec_name = "company_id"


    courses_ids = fields.Many2many('degree.master',required=True)
    company_id = fields.Many2one('res.company',required=True)
    active = fields.Boolean('Active',default=True)


    # _sql_constraints = [
    #     ('unique_company_id','UNIQUE(company_id)','College must be unique!')
    # ]
    