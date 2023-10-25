from odoo import models,fields,api,_


class QuotaMaster(models.Model):
    _name = "quota.master"

    name = fields.Char(string="Name")
    bulk_create = fields.Boolean(string="Bulk Create?")
    is_default = fields.Boolean(string="Is Default?")
    active = fields.Boolean(string="Active",default=True)

    _sql_constraints = [
        ('unique_quota_master','UNIQUE(name,bulk_create)','Quota already exist!')
    ]