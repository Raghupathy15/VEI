from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class HrLoanType(models.Model):
    _name = 'hr.loan.type'

    name = fields.Char(string="Loan Name")
    interest_rate = fields.Float(string="Interest Percentage",digits=(16, 4), default=0.0)