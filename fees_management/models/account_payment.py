from odoo import models,fields,api,_
from datetime import datetime


class ModeofPayment(models.Model):
    _name = "mode.of.payment"


    name = fields.Char(string="Mode")
    active = fields.Boolean(string="Active",default=True)


    _sql_constraints = [
        ('unique_mode_of_payment','UNIQUE(name)','Mode of Payment Should be UNIQUE!')
    ]


class InheritAccountPayment(models.Model):
    _inherit = "account.payment"


    is_custom_method = fields.Boolean(string="Is Custom Payment Method")
    payment_method_bank = fields.Char(string="Bank", copy=False)
    payment_method_number = fields.Char(string="Number", copy=False)
    payment_method_date = fields.Date(string="Date", copy=False)
    amount_balance = fields.Float(string="Balance",compute="get_payment_balance")


    def get_payment_balance(self):
        for payment in self:
            # if payment.payment_type == 'inbound':
            balance = 0
            for line in payment.move_id.line_ids:
                balance += line.amount_residual
            payment.amount_balance = payment.amount - balance

    @api.onchange('payment_method_line_id')
    def onchange_payment_method_line_id(self):
        if self.payment_method_line_id:
            if self.payment_method_line_id.name in ['Cheque', 'DD']:
                self.is_custom_method = True
            else:
                self.is_custom_method = False
    
    