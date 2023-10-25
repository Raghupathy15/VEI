from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import ValidationError, UserError


class AdmissionReportWizard(models.TransientModel):

    _name = "admission.report.wizard"
    _description = "Admission report wizard"

    date_from = fields.Date('Date from', required=True)
    date_to = fields.Date('Date to', required=True)
    course_ids = fields.Many2many('courses.master', string="courses")



class TransferStudentWizard(models.TransientModel):

    _name = "transfer.student.wizard"
    _description = "Transfer Student wizard"

    name = fields.Char('Student', required=True)
    curr_collage = fields.Many2one('res.company', readonly=True, string="Current Collage", default=lambda self: self.env.company)
    tras_collage = fields.Many2one('res.company', string="Transfer Collage")

    def action_transfer(self):
        admission = self.env['admission.confirmation'].browse(self._context.get('active_id'))
        student_fees = self.env['account.move'].search([('payment_state', '=', 'paid'), ('move_type', '=', 'out_invoice'), ('partner_id.name', '=', self.name)])
        if student_fees:
            raise ValidationError(_("Sorry..The student paid fees, Please refund."))
        else:
            admission.write({
                'curr_collage' : self.tras_collage
            })


