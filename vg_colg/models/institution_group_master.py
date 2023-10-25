from odoo import fields, models, api


class InstitutionGroupMaster(models.Model):
    _name = 'institution.group.master'
    _description = 'Institution Group Master'

    name = fields.Char()
