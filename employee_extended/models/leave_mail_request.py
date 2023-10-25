from datetime import datetime
import pytz
import xlsxwriter
from odoo.exceptions import ValidationError
from odoo import models, fields, api
from io import BytesIO
import base64
from urllib.request import urlopen



class HolidaysRequest(models.Model):
    _inherit = "hr.leave"


    def print_mail_report(self):
        print("self.employee_id.leave_manager_id.partner_id.ids = ",self.employee_id.leave_manager_id.partner_id.ids)
        print("self.employee_id.leave_manager_id.partner_id.id = ",self.employee_id.leave_manager_id.partner_id.id)
        template_id=self.env.ref('employee_extended.mail_template_order_report')
        ctx = {
            # 'default_model': 'hr.leave',
            # 'default_res_id': self.ids[0],
            'active_model': 'hr.leave',
            'default_use_template': bool(template_id),
            # 'default_partner_ids': self.employee_id.leave_manager_id.partner_id.ids,
            'default_template_id': template_id.id,
            'default_attachment_ids': self.supported_attachment_ids.ids,
            'default_composition_mode': 'comment',
            'active_id': self.ids[0],
            'active_ids': self.ids,
            'mark_so_as_sent': True,
            'force_email': False,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context':ctx
        }