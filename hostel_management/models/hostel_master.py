from odoo import models,fields,api,_


class HostelMaster(models.Model):
    _name = "hostel.master"
    _desc = "Students Hostel Master"
    _inherit = ['mail.thread']


    name = fields.Char(string="Hostel",required=True)
    floor_ids = fields.One2many("floor.master","hostel_id",string="Floors")
    active = fields.Boolean(string="Active",default=True)


    def action_open_floors(self):
        action = {
            'name': _("Floors"),
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
            'res_model': 'floor.master',
            'domain': [('id','in',self.floor_ids.ids)]
        }
        return action

