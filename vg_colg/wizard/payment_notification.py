# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import UserError
import requests
import json

class PaymentNotificationWizard(models.Model):
    _name = 'payment.notification.wizard'
    _description = 'Payment Notification Wizard'

    admission_ids = fields.Many2many('admission.list', string='Admission')
    document_mssg_subject = fields.Char(string='Subject')
    document_mssg_body = fields.Html(string='Body')

    def action_send_mail(self):
        if self.admission_ids:
            for admission_id in self.admission_ids:
                admission_id.sudo().write({
                    'payment_mssg_subject': self.document_mssg_subject,
                    'payment_mssg_body': self.document_mssg_body,
                })
            template_id = self.env.ref('vg_colg.payment_mail_notification_template').sudo()
            if template_id and self.admission_ids:
                for admission_id in self.admission_ids:
                    if admission_id.email:
                        template_id.send_mail(admission_id.id, force_send=True, email_values={"email_to": admission_id.email})


