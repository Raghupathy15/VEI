from odoo import fields, models, api


class degreeLevelMaster(models.Model):
    _name = 'degree.level.master'
    _description = 'Degree Master'

    name = fields.Char('Degree')
    grade_id = fields.Many2one('grade.master',string="Grade")
    stream_id = fields.Many2one('stream.master',string="Stream")
    description = fields.Char('Description')
    active = fields.Boolean('Active',default=True)


    _sql_constraints = [
        ('unique_degree_level','UNIQUE(name,grade_id,stream_id)','Combination of Degree, Grade and Stream must be unique!'),
    ]