from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta


class AccountCounterMaster(models.Model):
	_name = "counter.master"
	
	name = fields.Char('Name')
	company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, default=lambda self: self.env.company)
	

