from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.exceptions import UserError, ValidationError

class FeesDetails(models.Model):
	_inherit = 'fees.details'
	
	# @api.constrains('priority')
	# def _check_priority(self):
	# 	for rec in self:
	# 		obj = self.env['fees.details'].search([('priority','=',rec.priority),('fees_id','=',rec.fees_id.id)])
	# 		if len(obj)>1:
	# 			raise UserError(_('You cannot have two records with the same priority'))


	priority = fields.Integer(string='Priority')