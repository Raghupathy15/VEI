from odoo import models,fields,api,_
from odoo.exceptions import ValidationError


class RoomAllocationMaster(models.Model):
    _name = "room.allocation.master"
    _desc = "Hostel Room Allocation"


    hostel_id = fields.Many2one('hostel.master',string="Hostel")
    floor_id = fields.Many2one('floor.master',string="Floor")
    room_type_id = fields.Many2one('room.type',string="Room Type")
    room_id = fields.Many2one('room.master',string="Room")
    state = fields.Selection([('ready_to_occupy','Ready'),('partially_occupied','Partially Occupied'),('occupied','Occupied'),('under_maintanance','Under Maintanance')],string="Status",track_visibility="always")
    occupancy = fields.Integer(string="Occupany")
    available = fields.Integer(string="Available")


    @api.onchange('room_id')
    def onchange_room_no(self):
        self.state = self.room_id.state
        self.occupancy = self.room_id.capacity
        self.available = self.room_id.available_count


    def final_allocation(self):
        if self.room_id.state == 'under_maintanance':
            raise ValidationError(_("Cannot allocate students, Hence the room is under maintanance!"))
        student_id_list = self.env.context.get('active_ids')
        student_id_objs = self.env['student.details'].browse(student_id_list)
        self.room_id.student_ids = [(4,student.id) for student in student_id_objs]

        return {
            "warning":
            {
                "title":"Some Title",
                "message":"Some Message"
            }
        }
    