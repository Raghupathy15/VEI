from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta

class EmployeeType(models.Model):
    _name = "employee.type"
    _description = "Employee Type"
    _order = 'id'

    # @api.constrains('code')
    # def _check_code(self):
    #     if len(self.code) > 1 or len(self.code) == 0:
    #         raise exceptions.UserError(_('The Code should be of one letters'))
    #     obj = self.search([('code','=',self.code)])
    #     if len(obj) > 1:
    #         raise exceptions.UserError(_('The Code already Exist'))

    active = fields.Boolean(default=True)
    # code = fields.Char(string='Code',required=True)
    name = fields.Char(string="Name", required=True)
    description = fields.Char(string="Description", required=True)
    tech_or_non = fields.Selection([('teaching', 'Teaching'), ('non_teaching', 'Non Teaching')], string="Category", default='non_teaching',required=True)
    resource_calendar_id = fields.Many2one(
        'resource.calendar', 'Working Schedule', store=True, readonly=False,
        default=lambda self: self.env.company.resource_calendar_id.id, copy=False, index=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
