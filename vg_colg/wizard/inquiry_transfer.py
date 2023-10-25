from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import ValidationError, UserError


class TransferInquiryWizard(models.TransientModel):

    _name = "transfer.inquiry.wizard"
    _description = "Transfer Inquiry wizard"

    name = fields.Char('Student', required=True)
    curr_collage = fields.Many2one('res.company', readonly=True, string="Current Enquiry", default=lambda self: self.env.company)
    tras_collage = fields.Many2one('res.company', string="Transfer Inquiry To")

    def action_transfer(self):
        admission = self.env['admission.confirmation'].browse(self._context.get('active_id'))
        admission.sudo().write({'curr_collage' : self.tras_collage})