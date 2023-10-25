from odoo import api, fields, models, _, tools

class AccountAccount(models.Model):
    _inherit = "account.account"

    ifsc_code = fields.Char(string='IFSC CODE')
    account_number = fields.Char(string='ACCOUNT NUMBER')
    account_name = fields.Char(string="Account holder's Name")