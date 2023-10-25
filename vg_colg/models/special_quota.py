from odoo import fields, models, api


class SpecialQuota(models.Model):
    _name = 'special.quota'
    _description = 'Special Quota Master'

    name = fields.Char()
