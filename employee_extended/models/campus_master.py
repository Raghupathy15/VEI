from odoo import _, api, fields, models

class CampusMaster(models.Model):
	_name = 'campus.master'
	_inherit = ['mail.thread']
			
	name = fields.Char(string='Campus Name',required=True,track_visibility='always')
	street = fields.Char('Street',  readonly=False)
	street2 = fields.Char('Street2',  readonly=False)
	zip_code = fields.Char('Zip', change_default=True,  readonly=False)
	city = fields.Char('City',  readonly=False)
	state_id = fields.Many2one(
		"res.country.state", string='State',
		readonly=False,
		domain="[('country_id', '=?', country_id)]")
	country_id = fields.Many2one(
		'res.country', string='Country',
		 readonly=False)

class CompanyMaster(models.Model):
	_inherit = 'res.company'
	
	campus_id = fields.Many2one('campus.master',string="Campus", required=True)
	