from odoo import models,fields,api,_


class FloorMaster(models.Model):
    _name = "floor.master"
    _desc = "Floor Master"
    _inherit = ['mail.thread']


    name = fields.Char(string="Floor")
    display_name = fields.Char(related="name",string="Name")
    hostel_id = fields.Many2one("hostel.master",string="Hostel")
    room_type_ids = fields.One2many("room.type","floor_id",string="Room Types")
    room_ids = fields.One2many("room.master","floor_id",string="Rooms")
    active = fields.Boolean(string="Active",default=True)


    def action_open_room_types(self):
        print("Action Room Types")
        action = {
            'name': _("Room Types"),
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
            'res_model': 'room.type',
            'domain': [('id','in',self.room_type_ids.ids)]
        }
        return action
    
    def action_open_rooms(self):
        print("Action Rooms")
        action = {
            'name': _("Rooms"),
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
            'res_model': 'room.master',
            'domain': [('id','in',self.room_ids.ids)]
        }
        return action