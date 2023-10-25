# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class TrustMaster(models.Model):
	_name = 'trust.master'
	_inherit = ['mail.thread']
	

	name = fields.Char(string="Trust Name", required=True, track_visibility='always')

	# Address fields
	street = fields.Char('Street', compute='_compute_partner_address_values', readonly=False, store=True)
	street2 = fields.Char('Street2', compute='_compute_partner_address_values', readonly=False, store=True)
	zip_code = fields.Char('Zip', change_default=True, compute='_compute_partner_address_values', readonly=False, store=True)
	city = fields.Char('City', compute='_compute_partner_address_values', readonly=False, store=True)
	state_id = fields.Many2one(
		"res.country.state", string='State',
		compute='_compute_partner_address_values', readonly=False, store=True,
		domain="[('country_id', '=?', country_id)]")
	country_id = fields.Many2one(
		'res.country', string='Country',
		compute='_compute_partner_address_values', readonly=False, store=True)