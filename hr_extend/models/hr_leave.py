from odoo import models, fields, api, exceptions, _
from datetime import datetime, timedelta, time

class HolidaysRequest(models.Model):
    _inherit = "hr.leave"

    attendance_id = fields.Many2one('hr.attendance',string='Attendance')


    