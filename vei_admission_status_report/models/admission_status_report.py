from odoo import fields, models, api


class AdmissionStatusReport(models.Model):
    _name = 'admission.status.report'
    _description = 'Admission Status Report'

    inquiry_no = fields.Char(string="Inquiry No")
    inquiry_id = fields.Many2one('student.admission', string="Inquiry No")
    admission_no = fields.Char(string="Admission No")
    admission_id = fields.Many2one('admission.confirmation', string="Admission No")
    name = fields.Char(string="Name of the Student")
    student_whatsapp = fields.Char('WhatsApp Number')
    inquiry_state = fields.Selection(string='Inquiry Status',
                             selection=[('inquiry', 'Inquiry'), ('confirmed', 'Sent for Admission')])
    degree_level_id = fields.Many2one('degree.level.master', string="Degree")
    courses_id = fields.Many2one('courses.master', string="Course")
    admission_state = fields.Selection(string='Admission Status', selection=[('new', 'Councelling'),
                                                                   ('partially_paid', 'Partially paid'),
                                                                   ('token_fees', 'Payment pending'),
                                                                   ('admission_list', 'Admission Confirmed'),
                                                                   ('cancelled', 'Cancelled')])
    document_state = fields.Selection(string='Document Status', selection=[
        ('doc_not_collected', 'Document Not collected'),
        ('doc_collected', 'Documents fully collected'),
        ('doc_partially_collected', 'Documents partially collected'), ],
                                      readonly=True, copy=False, index=True, track_visibility='always',
                                      default='doc_not_collected')
    admission_list_state = fields.Selection(string='Admission List Status', selection=[('draft', 'Document Collection'),
                                                                           ('partially_paid', 'Partially paid'),
                                                                           ('doc_collected',
                                                                            'Documents fully collected'),
                                                                           ('doc_partially_collected',
                                                                            'Documents partially collected'),
                                                                           ('onhold', 'On-Hold'),
                                                                           ('confirmed', 'Moved to college'),
                                                                           ('cancelled', 'Cancelled'),
                                                                           ('documents_returned', 'Documents Returned')],
                                            readonly=True, copy=False, index=True, track_visibility='always',
                                            default='draft')
    stream_id = fields.Many2one('stream.master', string="Stream")
    company_id = fields.Many2one('res.company', 'College Name', index=True)
    quota_id = fields.Many2one('quota.master', string="Quota")
    email = fields.Char(string='Email')





