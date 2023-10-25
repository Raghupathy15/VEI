from odoo import models,fields,api,_


class SemesterMaster(models.Model):
    _name = "semester.master"


    name = fields.Char(string="Name")
    active = fields.Boolean(string="Active",default=True)


    _sql_constraints = [
        ('unique_semester_constraints','UNIQUE(name)','Semester is already exist!')
    ]