from odoo import models,fields,api,_


class InheritHrEmployee(models.Model):
    _inherit = "hr.employee"


    room_id = fields.Many2one("room.master",string="Room")
    empl_id = fields.Char(string='Employee ID')
    display_name = fields.Char(related="name",string="Display Name")
    accomodation_type = fields.Selection([('hosteler','Hosteler'),('dayscholar','Dayscholar')],string="Accomodation")


    # Remove Staff from the room
    def method_staff_remove(self):
        self.room_id.message_post(body=_(f"{self.role_no} - {self.name} was removed!"))
        self.room_id = False