from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from datetime import datetime


class InheritStudentDetails(models.Model):
    _inherit = "student.details"


    room_type_id = fields.Many2one('room.type',string="Room Type")
    room_id = fields.Many2one('room.master',string="Room")
    special_care = fields.Boolean('Special Care',track_visibility="always")
    special_care_reason = fields.Char('Special Care Reason',track_visibility="always")
    room_attendance_ids = fields.One2many("student.hostel.calendar","student_id",string="Student Hostel Tracker")
    room_history_ids = fields.One2many("student.room.history","student_id",string="Student Room History")
    attendance_status = fields.Selection([('present','Present'),('absent','Absent')],string="Status",compute="get_student_room_status")


    def get_student_room_status(self):
        for itm in self:
            if self.room_id and itm.room_attendance_ids:
                if not itm.room_attendance_ids[-1].end_datetime:
                    itm.attendance_status = 'present'
                else:
                    itm.attendance_status = 'absent'

            else:
                itm.attendance_status = 'absent'


    def put_attendance(self):
        print('Control arrived!')
        if self.room_attendance_ids:
            if not self.room_attendance_ids[-1].end_datetime:
                self.room_attendance_ids[-1].end_datetime = datetime.now()
            else:
                self.room_attendance_ids.create({
                    'start_datetime':datetime.now(),
                    'student_id': self.id,
                    'room_id':self.room_id.id,
                    'name':f"Daily Attendance",
                })
        else:
            self.room_attendance_ids.create({
                    'start_datetime':datetime.now(),
                    'student_id': self.id,
                    'room_id':self.room_id.id,
                    'name':f"Daily Attendance",
                })
        self.room_id.message_post(body=_(f"Attendance Marked For {self.name} - [{self.role_no or ''}]!"))


    # def put_entry_for_room(self):

    def create(self,vals):
        print('-----------Student Create----------',vals)
        res = super(InheritStudentDetails,self).create(vals)

        for student in res:
            if student.room_id:
                student.room_history_ids.create({
                    'name': 'Room Allocation',
                    'room_id': student.room_id.id,
                    'start_date': datetime.now().date(),
                    'end_date': False,
                    'student_id': student.id,
                })

        return res
    
    def write(self,vals):
        print("-----------Student Write-----------",vals)
        res = super(InheritStudentDetails,self).write(vals)

        for student in self:
            if 'room_id' in vals.keys():
                if vals.get('room_id'):
                    student.room_history_ids.create({
                        'name': 'Room Allocation',
                        'room_id': student.room_id.id,
                        'start_date': datetime.now().date(),
                        'end_date': False,
                        'student_id': student.id,
                    })
                else:
                    if student.room_history_ids:
                        student.room_history_ids[-1].end_date = datetime.now().date()
                    if student.room_attendance_ids and not student.room_attendance_ids[-1].end_datetime:
                        student.room_attendance_ids[-1].end_datetime = datetime.now()

        return res


    @api.onchange('courses_id')
    def onchange_courses_id(self):
        res = super(InheritStudentDetails,self).onchange_courses_id()
        if self.courses_id:
            self.room_type_id = False


    # Remove Staff from the room
    def method_student_remove(self):
        self.room_id.message_post(body=_(f"{self.role_no} - {self.name} was removed!"))
        self.room_id = False


    def action_return_room_allocations_form(self):

        if len(self.mapped('room_type_id')) > 1:
            raise ValidationError(_("Selected Students Room Type Should be Same to Allocate, Please don't select different room at type in one go!"))

        return {
            "name":_("Room Allocations"),
            "type":"ir.actions.act_window",
            "res_model":"room.allocation.master",
            "view_mode":"form",
            "target":"new",
            "context":{"default_room_type_id":self[0].room_type_id.id},
        }
    
    def action_return_student_hostel_attendance(self):

        return {
            "name":_("Hostel Attendance"),
            "type":"ir.actions.act_window",
            "res_model":"student.hostel.calendar",
            "domain":[('id','in',self.room_attendance_ids.ids)],
            "view_mode":"calendar,tree,form",
            "target":"inline",
            "context":{'default_student_id':self.id},
        #     "views": [
        #     (self.env.ref('hostel_management.view_student_hostel_calendar_calendar').id, "calendar"),
        #     (self.env.ref('hostel_management.view_student_hostel_calendar_tree').id, "tree"),
        #     (False, "form"),  # Use "False" to indicate the default form view
        # ],
        }
    
    def action_return_student_room_history(self):
        return {
            "name":_("Room History"),
            "type":"ir.actions.act_window",
            "res_model":"student.room.history",
            "domain":[('id','in',self.room_history_ids.ids)],
            "view_mode":"tree,form",
            "target":"inline",
            "context":{'default_student_id':self.id},
        #     "views": [
        #     (self.env.ref('hostel_management.view_student_hostel_calendar_calendar').id, "calendar"),
        #     (self.env.ref('hostel_management.view_student_hostel_calendar_tree').id, "tree"),
        #     (False, "form"),  # Use "False" to indicate the default form view
        # ],
        }

class StudentHostelCalendar(models.Model):
    _name = 'student.hostel.calendar'
    _description = 'Student Hostel Calendar'

    name = fields.Char(string='Name', required=True)
    start_datetime = fields.Datetime(string='Check In Time', required=True)
    end_datetime = fields.Datetime(string='Check Out Time')
    student_id = fields.Many2one('student.details',string="Role No")
    room_id = fields.Many2one('room.master',string="Room")


class StudentRoomHistory(models.Model):
    _name = 'student.room.history'
    _description = 'Student Room History'

    name = fields.Char(string='Name', required=True)
    start_date= fields.Date(string='Allocated Date', required=True)
    end_date = fields.Date(string='Vacated Date')
    student_id = fields.Many2one('student.details',string="Role No")
    room_id = fields.Many2one('room.master',string="Room")