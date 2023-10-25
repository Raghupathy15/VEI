from odoo import fields, models, api


class DistrictMaster(models.Model):
    _name = 'district.master'
    _description = 'District Master'

    name = fields.Char(string="Name")
