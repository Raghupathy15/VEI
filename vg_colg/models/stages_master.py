from odoo import fields, models, api


class StagesMaster(models.Model):
    _name = 'stages.master'
    _description = 'Stages Master'

    name = fields.Char('Name')


    _sql_constraints = [
        ('unique_stages_constraints','UNIQUE(name)','Stage is already exist!')
    ]
