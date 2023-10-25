from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import format_time


class CertificateWithdraw(models.Model):
    _name = "certificate.withdrawn"
    _inherit = ['mail.thread']

    # name = fields.Selection(selection=[
	# 	('aadhar', 'Aadhar Card'),
    #     ('pan ', 'PAN Card'),
    #     ('birth ', 'Birth Certificate'),
    #     ('voter ', 'Voter ID'),
    #     ('passport ', 'Passport'),
    #     ('driver ', 'Drivers License '),
    #     ('other', 'Other')], string='Name',tracking=True,copy=False)
    
    state = fields.Selection(selection=[
		('draft','draft'),
        ('withdrawn','Withdrawn'),
        ('closed','Closed'),
        ('cancelled','Cancelled')],default='draft',string='State',tracking=True,copy=False)
    employee_id = fields.Many2one('hr.employee',string='Employee Id')
    withdrawn_date = fields.Date('Given Date')
    lastdate_date = fields.Date('Return Date')
    res_emp_id = fields.Many2one('hr.employee',string=' Responsible Employee')
    proof_lines = fields.One2many('id.proof.line','withdrawn_id',string='Employee Proof')

    def name_get(self):
        return [(w.id,w.employee_id.name) for w in self]
    
    def withdrawn_button(self):
        self.state = 'withdrawn'

    def closed_button(self):
        self.state = 'closed'

    def cancelled_button(self):
        self.state = 'cancelled'