from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import ValidationError, UserError, MissingError
import ast,base64


class AdmissionReportWizard(models.TransientModel):
    _name = "admission.concession.report.wizard"
    _description = "Admission Concession report wizard"


    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    course_ids = fields.Many2many('courses.master', string="Courses")
    rec_list_ids = fields.Char()
    report_type = fields.Selection([('approved_report','Approved'),('rejected_report','Rejected')],string="Report Type")
    send_by_mail = fields.Boolean(string="Send by Mail",default=False)
    users_ids = fields.Many2many('res.users',string="Receipients")
    mail_subject = fields.Char(string="Subject",default="Req. Approval - Admission Concession Report")
    mail_body = fields.Html(string="Body")

    @api.onchange('send_by_mail','users_ids')
    def onchange_mail_info(self):
        if self.send_by_mail and self.users_ids:
            default_content = f"""<pre>Dear {self.users_ids[0].partner_id.name},
    Please find the attached document for your review and approval. Your prompt response would be greatly appreciated.</pre>"""
            self.mail_body = default_content
        elif self.send_by_mail:
            default_content = f"""<pre>Dear Approver,
    Please find the attached document for your review and approval. Your prompt response would be greatly appreciated.</pre>"""
            self.mail_body = default_content
        else:
            self.mail_body = ""

    # Redirect Approved and Rejected Concession Reports
    def load_approved_rejected_reports(self,domain):
        report_dict = {}
        if self.report_type == 'approved_report':
            domain.append(('state','=','approved'))
            print(domain)
            student_concession_objs = self.env['student.concession'].search(domain,order='id asc')
            print(student_concession_objs)
            if not student_concession_objs:
                raise MissingError(_("Based on the given input nothing to print!"))
            self.rec_list_ids = str(student_concession_objs.ids)
            report_dict = self.env.ref('fees_management.action_report_student_approved_concession').report_action(self)
        elif self.report_type == 'rejected_report':
            domain.append(('state','=','rejected'))
            student_concession_objs = self.env['student.concession'].search(domain,order='id asc')
            if not student_concession_objs:
                raise MissingError(_("Based on the given input nothing to print!"))
            self.rec_list_ids = str(student_concession_objs.ids)
            report_dict = self.env.ref('fees_management.action_report_student_rejected_concession').report_action(self)
        return report_dict

    # Loading data based on the given input
    def print_report(self):
        domain = []
        if self.start_date:
            domain.append(('date','>=',self.start_date))
        if self.end_date:
            domain.append(('date','<=',self.end_date))
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError(_("Selected Start date must be greater than the End date!"))
        if self.course_ids:
            domain.append(('courses_id','in',self.course_ids.ids))
        if self.send_by_mail and not self.users_ids:
            raise ValidationError(_("Please select at least one receipient to send a mail!"))
        
        if self.report_type:
            return self.load_approved_rejected_reports(domain)
        
        admission_list_objs = self.env['admission.list'].search(domain,order='id asc')
        
        self.rec_list_ids = str(admission_list_objs.ids)

        if admission_list_objs and not self.send_by_mail:
            report_dict = self.env.ref('vg_colg.action_report_admission_concession').report_action(self)
            return report_dict
        elif admission_list_objs and self.send_by_mail:
            self.send_a_mail_with_an_attachment()
        else:
            raise MissingError(_("Based on the given input nothing to print/mail!"))
        
    # From the Qweb template just load the admission list data
    def load_admission_list_data(self):
        if self.report_type:
            if self.rec_list_ids:
                data = self.env['student.concession'].sudo().browse(ast.literal_eval(self.rec_list_ids))
            else:
                data = self.env['student.concession'].browse([])
            return data

        if self.rec_list_ids:
            data = self.env['admission.list'].sudo().browse(ast.literal_eval(self.rec_list_ids))
        else:
            data = self.env['admission.list'].browse([])
        return data
    
    # Generate a report and send it to the repective selected users as a individual mail
    def send_a_mail_with_an_attachment(self):
        # Get the report action
        report_action = self.env.ref('vg_colg.action_report_admission_concession').sudo()
        
        # Get the report data
        data = {'context':self.env.context.copy()}
        data.update({'report_type':'pdf'})
        report_data = report_action._render_qweb_pdf('vg_colg.action_report_admission_concession',res_ids=self.ids,data=data)
        datas = base64.b64encode(report_data[0])

        # Create the attachment options
        attachment_options = {
            'name': f"Admission Concession Report From {self.start_date or 'Day one '} To {self.end_date or 'Till Today'}.pdf",
            'type': 'binary',
            'datas': datas,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype':'application/pdf',
        }

        # Create the attachment
        attachment = self.env['ir.attachment'].sudo().create(attachment_options)

        # Get the selected users
        selected_users = self.env['res.users'].sudo().browse(self.users_ids.ids)

        # Send the email with the attachment to each selected user
        for user in selected_users:
            self.sudo().send_mail_with_attachment(user, attachment)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'admission.concession.report.wizard',
            'view_mode': 'form',
            'target': 'current',
            'flags': {'form': {'action_buttons': True}},
            'context': {'form_view_initial_mode': 'edit'},
            'message': 'Sent successfully!',  # Add a success message here
        }

    # Helper Method - Sending an email to the user
    def send_mail_with_attachment(self, user, attachment):
        # Prepare the email parameters
        mail_values = {
            'subject': self.mail_subject if self.mail_subject else 'Admission Concession Report Approval',
            'body_html': self.mail_body if self.mail_body else f'Dear {user.partner_id.name},<br/><p>Please find the attached report and we are awaiting for your approval.</p>',
            'email_to': user.email,
            'attachment_ids': [(4, attachment.id)],
        }

        # Create the email
        mail = self.env['mail.mail'].create(mail_values)

        # Send the email
        mail.send()

        # Inorder to track the approval state we can maintain the sent state we can add state field in the attachment master
        # Once if got sent we can set it to sent.