from odoo import models,fields,api,_


class RoomAmenitiesMaster(models.Model):
    _name = "room.amenities.master"
    _desc = "Room Amenities Master"
    _inherit = ['mail.thread']


    name = fields.Char(string="Name")
    display_name = fields.Char(related="name",string="Display Name")
    amount = fields.Float(string="Amount")
    note = fields.Text(string="Notes")
    active = fields.Boolean(string="Active",default=True)