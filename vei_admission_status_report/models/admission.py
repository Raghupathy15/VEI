from odoo import fields, models, api


class StudentAdmission(models.Model):
    _inherit = 'student.admission'

    admission_report_id = fields.Many2one('admission.status.report', string="Admission Report")

    @api.model_create_multi
    def create(self, vals_lst):
        for vals in vals_lst:
            res = super(StudentAdmission, self).create(vals)
            if vals.get('name') :
                admission_report = self.env['admission.status.report'].sudo().create({
                    'name' : res.name,
                    'inquiry_id' : res.id,
                    'student_whatsapp' : res.whatsapp_number,
                    'inquiry_state' : res.state,
                    'degree_level_id' : res.degree_level_id.id if res.degree_level_id else False,
                    'courses_id' : res.courses_id.id if res.courses_id else False,
                    'stream_id' : res.stream_id.id if res.stream_id else False,
                    'company_id' : res.company_id.id if res.company_id else False,
                    'quota_id' : res.quota_id.id if res.quota_id else False,
                    'email' : res.email,
                })
                if admission_report:
                    res.write({
                        'admission_report_id' : admission_report.id
                    })
            return res

    def action_confirm_admission(self):
        res = super(StudentAdmission, self).action_confirm_admission()
        admission_confirmation = self.env['admission.confirmation'].search([('gate_pass_id','=',self.id)],limit=1)
        if admission_confirmation and self.admission_report_id:
            self.admission_report_id.sudo().write({
                'inquiry_state' : 'confirmed',
                'admission_id' : admission_confirmation.id,
                'admission_state' : 'new',
            })
            admission_confirmation.write({
                'admission_report_id': self.admission_report_id.id
            })



class AdmissionConfirmation(models.Model):
    _inherit = 'admission.confirmation'

    admission_report_id = fields.Many2one('admission.status.report', string="Admission Report")

    def write(self, vals):
        res = super(AdmissionConfirmation, self).write(vals)
        if vals.get('state'):
            if self.admission_report_id:
                self.admission_report_id.sudo().write({
                    'admission_state' : self.state
                })
        return res

    def action_send_admission_list(self):
        res = super(AdmissionConfirmation, self).action_send_admission_list()
        admission_list = self.env['admission.list'].search([('admission_id', '=', self.id)], limit=1)
        if admission_list and self.admission_report_id:
            admission_list.write({
                'admission_report_id': self.admission_report_id.id
            })


class AdmissionList(models.Model):
    _inherit = 'admission.list'

    admission_report_id = fields.Many2one('admission.status.report', string="Admission Report")

    def write(self, vals):
        res = super(AdmissionList, self).write(vals)
        if vals.get('document_state'):
            if self.admission_report_id:
                self.admission_report_id.sudo().write({
                    'document_state' : self.document_state
                })
        if vals.get('state'):
            if self.admission_report_id:
                self.admission_report_id.sudo().write({
                    'admission_list_state' : self.state
                })
        return res