from odoo import models,fields,api,_


class InheritAdmissionConfirmation(models.Model):
    _inherit = "admission.confirmation"


    room_type_id = fields.Many2one('room.type',string="Room Type",track_visibility="always")


