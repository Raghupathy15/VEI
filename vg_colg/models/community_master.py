from odoo import fields, models, api


class CommunityMaster(models.Model):
    _name = 'community.master'
    _description = 'Community Master'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
