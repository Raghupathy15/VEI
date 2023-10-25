from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class OneTimeFees(models.Model):
	_name = 'one.time.fees.category'
	_description = 'One Time Fees'
	_order = 'id desc'
	_inherit = ['mail.thread']


	name = fields.Char(string='Fees Name', track_visibility='always')
	