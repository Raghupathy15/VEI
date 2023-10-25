# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class GatePass(models.Model):
	_name = 'gate.pass'
	_description = "Gate Pass"
	_inherit = ['mail.thread']

	def _comute_time(self):
		for record in self:
			if record.date:		
				record.time = record.date + timedelta(minutes=330)
				record.time = record.time[10:19]

	name = fields.Char(string='GP. No', default='New')
	visitor_name = fields.Char(string='Visitor Name', required=True, track_visibility='always')
	date_in = fields.Datetime(string='In Time', readonly=True)
	date_out = fields.Datetime(string='Out Time', readonly=True)
	mob_no = fields.Char(string="Mobile number", track_visibility='always')
	company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
	state = fields.Selection([
		('new', 'New'),
		('check_in', 'Visitor In'),
		('check_out', 'Visitor Out'),
	], string='Status', readonly=True, copy=False, index=True, track_visibility='always', default='new')


	@api.model
	def create(self, vals):
		vals['name'] = self.env['ir.sequence'].next_by_code('gate.pass')
		return super(GatePass, self).create(vals)

	def visitor_check_in(self):
		self.date_in = datetime.now()
		self.state = 'check_in'

	def visitor_check_out(self):
		self.date_out = datetime.now()
		self.state = 'check_out'