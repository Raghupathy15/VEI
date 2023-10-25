from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
import json


class RoomMaster(models.Model):
    _name = "room.master"
    _desc = "Hostel Room Master"
    _inherit = ['mail.thread']


    name = fields.Char(string="Room No",required=True,track_visibility="always")
    display_name = fields.Char(related="name",string="Display Name")
    state = fields.Selection([('ready_to_occupy','Ready'),('partially_occupied','Partially Occupied'),('occupied','Occupied'),('under_maintanance','Under Maintanance')],default="ready_to_occupy",string="Status",track_visibility="always",copy=False)
    student_ids = fields.One2many('student.details','room_id',string="Students",track_visibility="always",copy=False)
    student_domain = fields.Char(string="Student List",compute="get_unassigned_student_list")
    guest_employee_ids = fields.One2many('hr.employee','room_id',string="Staffs/Guest",track_visibility="always",help="Above linked Guest will display as line items for better view!",copy=False)
    warden_employee_ids = fields.Many2many('hr.employee',string="Wardens",track_visibility="always",help="Above linked Students will display as line items for better view!")
    type_id = fields.Many2one("room.type",string="Room Type",track_visibility="always")
    room_fees = fields.Float(string="Fees")
    amenities_ids = fields.Many2many('room.amenities.master',string="Amenities",help="Above linked amenities will display as line items for better view!")
    capacity = fields.Integer(string="Room Capacity",required=True,track_visibility="always")
    total_count = fields.Integer(string="Occupied Count",compute="get_room_count")
    available_count = fields.Integer(string="Available Count",compute="get_room_count")
    floor_id = fields.Many2one('floor.master',string="Floor",required=True,track_visibility="always")
    hostel_id = fields.Many2one('hostel.master',string="Hostel",track_visibility="always")
    active = fields.Boolean(string="Active",default=True,track_visibility="always")
    # attendance_status = fields.Selection([('present','Present'),('absent','Absent')],string="Attendance Status")


    # def get_student_room_status(self):
    #     for itm in self:
    #         if self.room_id and itm.room_history_ids:
    #             if not itm.room_history_ids[-1].end_datetime:
    #                 itm.attendance_status = 'present'
    #             else:
    #                 itm.attendance_status = 'absent'
    #         else:
    #             itm.attendance_status = 'absent'

    def get_unassigned_student_list(self):
        student_objs = self.env['student.details'].search([('room_id','=',False)])
        list_ids = json.dumps([('id','in',student_objs.mapped('id'))])
        for room in self:
            room.student_domain = list_ids

    # Helper method set room status
    @api.onchange('student_ids')
    @api.depends('student_ids','guest_employee_ids')
    def set_room_status(self):
        if self.state != 'under_maintanance':
            if not self.total_count:
                self.state = 'ready_to_occupy'
            elif self.capacity > self.total_count:
                self.state = 'partially_occupied'
            elif self.capacity == self.total_count or self.capacity < self.total_count:
                self.state = 'occupied'

        else:
            ...
        
    @api.model
    def create(self,vals):
        if 'capacity' in vals.keys() and not vals.get('capacity'):
            raise ValidationError(_("Room Capacity should be greater than zero!"))
        res = super(RoomMaster,self).create(vals)
        if 'student_ids' in vals.keys() or 'guest_employee_ids' in vals.keys():
            res.get_room_count()
        return res
        
    def write(self,vals):
        if 'capacity' in vals.keys() and not vals.get('capacity'):
            raise ValidationError(_("Room Capacity should be greater than zero!"))
        res = super(RoomMaster,self).write(vals)
        if 'student_ids' in vals.keys()  or 'guest_employee_ids' in vals.keys():
            self.get_room_count()
        return res

    # Get available count
    @api.depends('student_ids')
    def get_room_count(self):
        for room in self:
            room.total_count = len(room.guest_employee_ids) + len(room.student_ids)
            room.available_count = room.capacity - room.total_count if room.capacity - room.total_count > 0 else 0
            room.set_room_status()

    # If its ready then it will cut the link of students and staffs
    def set_as_ready(self):
        for room in self:
            room.student_ids = [(6,0,[])]
            room.guest_employee_ids = [(6,0,[])]
            room.state = 'ready_to_occupy'

    # It will be a state change only
    def set_as_partial(self):
        for room in self:
            if not room.student_ids and not room.guest_employee_ids:
                raise ValidationError(_("Can't set as Parilly occupied hence no one has assinged!"))
            room.state = 'partially_occupied'

    # It will be a state change only
    def set_as_full(self):
        for room in self:
            if not room.student_ids and not room.guest_employee_ids:
                raise ValidationError(_("Can't set as Fully occupied hence no one has assinged!"))
            room.state = 'occupied'

    # It will cut the link of students and staffs
    def set_as_under_maintanance(self):
        for room in self:
            room.student_ids = [(6,0,[])]
            room.guest_employee_ids = [(6,0,[])]
            room.message_post(body=_(f"Due to Room Maintanance Student and Guest was Removed from {room.name} !"))
            room.state = 'under_maintanance'

    # Remove Staff from the room
    def method_student_remove(self):
        self.message_post(body=_(f"{self.empl_id} - {self.name} was removed!"))
        self.room_id = False

