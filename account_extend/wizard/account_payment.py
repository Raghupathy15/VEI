from odoo import models, fields, api, exceptions, _

class AccountPaymentRegister(models.TransientModel):
	_inherit = 'account.payment.register'
	
	from_fee = fields.Boolean(string="From Fee",default=False)
	fee_id = fields.Many2one('account.fees.details',string="Fee Details")