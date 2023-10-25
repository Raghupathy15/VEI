# -*- coding: utf-8 -*-

from odoo import api,exceptions,fields, models, _


class CompanyMaster(models.Model):
    _inherit = 'res.company'
    
    @api.constrains('college_code')
    def _check_college_code(self):
        # if len(self.college_code) != 3:
        #     raise exceptions.UserError(_('The Code should be of three letters'))
        obj = self.search([('college_code','=',self.college_code)])
        if len(obj) > 1:
            raise exceptions.UserError(_('The Code already Exist'))
        
    admission_sequence = fields.Char(string="Admission Sequence Prefix", required=True)
    trust_id = fields.Many2one('trust.master',string="Trust", required=True)
    type = fields.Selection(string='Type', selection=[('autonomous', 'Autonomous'),
                            ('non_autonomous', 'Non Autonomous')],required=True, track_visibility='always')
    college_code = fields.Char(string='College Code',required=True)