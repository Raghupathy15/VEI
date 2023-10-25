from odoo import fields, models, api

class GradeMaster(models.Model):
    _name = 'grade.master'
    _description = 'Grade Master'

    name = fields.Char('Grade Name')
    stream_ids = fields.Many2many('stream.master',string="Stream")
