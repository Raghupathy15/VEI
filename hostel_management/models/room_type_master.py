import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class RoomType(models.Model):
	_name = 'room.type'
	_description = 'Room Type'
	_order = 'id desc'
	_inherit = ['mail.thread']


	name = fields.Char(string="Name", required=True)
	product_id = fields.Many2one("product.product",string="Fees Heads",track_visibility="always")
	courses_ids = fields.Many2many('courses.master',string="Courses",track_visibility="always")
	active = fields.Boolean(string="Active",default=True,track_visibility="always")
	floor_id = fields.Many2one("floor.master",string="Floor")
	room_ids = fields.One2many("room.master","type_id",string="Rooms")


	# @api.onchange('courses_ids')
	# def onchange_courses_ids(self):
	# 	if self.courses_ids:
	# 		self.product_id = False
	# 		return {
	# 			'domain':{
	# 				'product_id':[('courses_ids','in',self.courses_ids.ids)]
	# 			}
	# 		}

	# def action_open_floors(self):
    #     action = {
    #         'name': _("Floors"),
    #         'view_mode': 'tree',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'room.master',
    #         'domain': [('id','in',self.floor_ids.ids)]
    #     }
    #     return action
	