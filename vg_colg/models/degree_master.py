from odoo import fields, models, api


class degreeMaster(models.Model):
    _name = 'degree.master'
    _description = 'Degree Master'

    name = fields.Char('Course Name')
    stream_id = fields.Many2one('stream.master',string="Stream")
    grade_id = fields.Many2one('grade.master',string="Grade")
    description = fields.Char('Description')

    _sql_constraints = [
        ('unique_degree_master','UNIQUE(name,stream_id,grade_id)','Combination of Degree, Stream and Grade shoule be unique!')
    ]


    @api.onchange('stream_id')
    def onchange_stream_id(self):
        self.grade_id = False
