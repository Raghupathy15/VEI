from odoo import fields, models, api


class TalukMaster(models.Model):
    _name = 'taluk.master'
    _description = 'Taluk Master'

    name = fields.Char()
