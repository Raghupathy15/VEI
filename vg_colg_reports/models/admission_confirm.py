# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AdmissionConfirm(models.Model):
    _inherit = 'admission.confirmation'

    def get_field_value(self):
        for record in self:
            if record.gate_pass_id:
                get_val = self.env['student.admission'].search_read([('id', '=', self.gate_pass_id.id)], [])
            # Process or return get_val as needed
            return get_val[0]

