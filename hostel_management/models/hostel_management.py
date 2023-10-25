import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class HostelManagement(models.Model):
	_name = 'hostel.management'
	_description = 'Hostel Management'
	_order = 'id desc'
	_inherit = ['mail.thread']


	category_id = fields.Many2one('category.master', string="Category", required=True, track_visibility='always')
	course_id = fields.Many2one('courses.master', string="Course", required=True, track_visibility='always')
	room_id = fields.Many2one('room.type', string="Room type", required=True, track_visibility='always')
	occupancy = fields.Integer(string="Occupancy", required=True, track_visibility='always')
	fees = fields.Integer(string="Fees Amount", required=True, track_visibility='always')
	term = fields.Integer(string="Term", required=True, track_visibility='always')
	total_fees = fields.Integer(string="Total Fees/Year", readonly=True, track_visibility='always')
	notes = fields.Text(string="Notes", track_visibility='always')
	room_no = fields.Char(string="Room No", track_visibility='always')

	@api.onchange('fees','term')
	def onchange_total_fees(self):
		if self.fees and self.term:
			self.total_fees = self.fees * self.term


	