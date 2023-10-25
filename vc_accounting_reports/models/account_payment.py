# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountPaymentMethod(models.Model):
    _inherit = "account.payment.method"

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res['dd'] = {'mode': 'multi', 'domain': [('type', '=', 'bank')]}
        res['cheque'] = {'mode': 'multi', 'domain': [('type', '=', 'bank')]}
        return res



class AccountRegisterPayments(models.TransientModel):
    _inherit = "account.payment.register"

    is_custom_method = fields.Boolean(string="Is Custom Payment Method")
    payment_method_bank = fields.Char(string="Bank",copy=False)
    payment_method_number = fields.Char(string="Number",copy=False)
    payment_method_date = fields.Date(string="Date",copy=False)

    @api.onchange('payment_method_line_id')
    def onchange_payment_method_line_id(self):
        if self.payment_method_line_id:
            if self.payment_method_line_id.name in ['Cheque','DD']:
                self.is_custom_method = True
            else:
                self.is_custom_method = False

    def _create_payment_vals_from_wizard(self, batch_result):
        # OVERRIDE
        payment_vals = super()._create_payment_vals_from_wizard(batch_result)
        payment_vals['is_custom_method'] = self.is_custom_method
        payment_vals['payment_method_bank'] = self.payment_method_bank
        payment_vals['payment_method_number'] = self.payment_method_number
        payment_vals['payment_method_date'] = self.payment_method_date
        return payment_vals

    def _prepare_payment_vals(self, invoices):
        res = super(AccountRegisterPayments, self)._prepare_payment_vals(
            invoices)
        # Check payment method is Check or PDC
        check_pdc_ids = self.env['account.payment.method'].search(
            [('code', 'in', ['dd', 'cheque'])])
        if self.payment_method_id.id in check_pdc_ids.ids:
            currency_id = self.env['res.currency'].browse(res['currency_id'])
            journal_id = self.env['account.journal'].browse(res['journal_id'])
            # Updating values in case of Multi payments
            res.update({
                'is_custom_method': self.is_custom_method,
                'payment_method_bank': self.payment_method_bank,
                'payment_method_number': self.payment_method_number,
                'payment_method_date': self.payment_method_date,
            })
        return res


# class AccountPayment(models.Model):
#     _inherit = "account.payment"

#     is_custom_method = fields.Boolean(string="Is Custom Payment Method")
#     payment_method_bank = fields.Char(string="Bank", copy=False)
#     payment_method_number = fields.Char(string="Number", copy=False)
#     payment_method_date = fields.Date(string="Date", copy=False)

#     @api.onchange('payment_method_line_id')
#     def onchange_payment_method_line_id(self):
#         if self.payment_method_line_id:
#             if self.payment_method_line_id.name in ['Cheque', 'DD']:
#                 self.is_custom_method = True
#             else:
#                 self.is_custom_method = False


