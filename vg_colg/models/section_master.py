from odoo import fields, models, api


class SectionMaster(models.Model):
    _name = 'section.master'
    _description = 'Section Master'

    name = fields.Char('Name')
