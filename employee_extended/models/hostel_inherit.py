from odoo import _, api, fields, models


class RoomandOccupancy(models.Model):
	_name = 'room.occupancy'

	def name_get(self):
		result = []
		for move in self:
			result.append((move.id, move.room_no))
		return result

	room_no = fields.Char(string='Room')
	occupancy = fields.Integer(string='Occupancy')

class HostelRoomLine(models.Model):
	_name = 'hostel.room.line'

	@api.onchange('room_no')
	def change_occupancy(self):
		for rec in self:
			rec.occupancy = rec.room_no.occupancy
			
	room_no = fields.Many2one('room.occupancy',string='Room',required=True)
	occupancy = fields.Integer(string='Occupancy')
	hostel_id = fields.Many2one('hostel.management',string='Hostel ID')

class HostelManagement(models.Model):
	_inherit = 'hostel.management'
		
	room_occupancy = fields.One2many('hostel.room.line','hostel_id',string='Room Occupancy')