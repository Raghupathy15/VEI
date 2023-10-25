from odoo import fields, models, api


class ReferenceMaster(models.Model):
    _name = 'reference.master'
    _description = 'Reference Master'

    name = fields.Char()
