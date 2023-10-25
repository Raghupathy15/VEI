from odoo import fields, models, api


class LastStudiedInstitutions(models.Model):
    _name = 'last.studied.institutions'
    _description = 'Last Studied Institutions'

    name = fields.Char('Name')
    address = fields.Text('Address')
