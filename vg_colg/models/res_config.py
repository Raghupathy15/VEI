# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HrLeaveConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    welcome_mssg_subject = fields.Char(string='Subject')
    welcome_mssg_body = fields.Html(string='Body')

    document_mssg_subject = fields.Char(string='Subject')
    document_mssg_body = fields.Html(string='Body')

    payment_mssg_subject = fields.Char(string='Subject')
    payment_mssg_body = fields.Html(string='Body')

    def set_values(self):
        super(HrLeaveConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].set_param
        set_param('welcome_mssg_subject', self.welcome_mssg_subject)
        set_param('welcome_mssg_body', self.welcome_mssg_body)
        set_param('document_mssg_subject', self.document_mssg_subject)
        set_param('document_mssg_body', self.document_mssg_body)
        set_param('payment_mssg_subject', self.payment_mssg_subject)
        set_param('payment_mssg_body', self.payment_mssg_body)


    @api.model
    def get_values(self):
        res = super(HrLeaveConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            welcome_mssg_subject=get_param('welcome_mssg_subject', default=''),
            welcome_mssg_body=get_param('welcome_mssg_body', default=''),
            document_mssg_subject=get_param('document_mssg_subject', default=''),
            document_mssg_body=get_param('document_mssg_body', default=''),
            payment_mssg_subject=get_param('payment_mssg_subject', default=''),
            payment_mssg_body=get_param('payment_mssg_body', default=''),
        )
        return res

