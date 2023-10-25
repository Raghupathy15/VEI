import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class Categorymaster(models.Model):
	_name = 'category.master'
	_description = 'Category  Master'
	_order = 'id desc'
	_inherit = ['mail.thread']


	name = fields.Char(string="Name", required=True)