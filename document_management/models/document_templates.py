from odoo import fields, models, api


class DocumentTemplates(models.Model):
    _name = 'document.templates'
    _description = 'Document Templates'

    name = fields.Char('Template Name')
    template_ids = fields.One2many('document.name', 'template_id', string='Templates')


class DocumentName(models.Model):
    _name = 'document.name'
    _description = 'Document Name'

    name = fields.Char('Document Name')
    is_mandatory = fields.Boolean('Is Mandatory', default=False)
    template_id = fields.Many2one('document.templates')

