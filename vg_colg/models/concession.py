from odoo import models,fields,api,_
from odoo.exceptions import ValidationError


class StudentConcession(models.Model):
    _name = "student.concession"
    _desc = "Used to store student concession information General and Special"
    _inherit = ['mail.thread'] 
    _rec_name = 'roll_no_id'



    # name = fields.Char(string="Concession")
    admission_id = fields.Many2one('admission.confirmation',string="Admission Name",track_visibility='always')
    admission_no = fields.Char(string="Admission No")
    student_name = fields.Char(related="roll_no_id.name",string="Name of the Student")
    concession_type = fields.Many2one('general.concession.type',string="Concession Type", track_visibility="always")
    roll_no_id = fields.Many2one('student.details',string="Roll No.",required=True)
    company_id = fields.Many2one('res.company',string="College")
    courses_id = fields.Many2one('courses.master',string="Course")
    amount = fields.Float(string="Amount",digits=(12,2),track_visibility='always')
    remarks = fields.Text(string="Remarks",track_visibility='always')
    state = fields.Selection([('draft','Draft'),('to_approve','To First Level Approval'),('first_level_approve','First Level Approved'),('approved','Second Level Approved'),('rejected','Rejected')],default='draft',string="State",track_visibility='always')
    attachment_ids = fields.Many2many('ir.attachment',string="Documents",track_visibility="always")
    display_attachment_ids = fields.Char(compute='_compute_display_attachments', string='Display Attachments', store=True)
    parent_concession_id = fields.Many2one('student.concession',string="Concessions")
    child_concession_ids = fields.One2many('student.concession','parent_concession_id',string="Concessions",compute="compute_concessions")
   
    @api.onchange('admission_id')
    def compute_concessions(self):
        for concession in self:
            concession.child_concession_ids = self.search([('id','!=',(concession.id if concession.id else False)),('admission_id','=',concession.admission_id.id)]) or False
    
    @api.onchange('admission_id')
    def compute_roll_no_id(self):
        for itm in self:
            itm.roll_no_id = self.env['student.details'].sudo().search([('aadhar_no','=',itm.admission_id.aadhar_no)],limit=1).id

    @api.onchange('roll_no_id')
    def compute_admission_id(self):
        for itm in self:
            itm.admission_id = self.env['admission.confirmation'].sudo().search([('aadhar_no','=',itm.roll_no_id.aadhar_no)],limit=1).id
            itm.company_id = self.roll_no_id.company_id.id
            itm.courses_id = self.roll_no_id.courses_id.id

    @api.depends('attachment_ids')
    def _compute_display_attachments(self):
        for record in self:
            attachments = record.attachment_ids.mapped('name')
            record.display_attachment_ids = ', '.join(attachments)

    @api.onchange('amount')
    def onchange_amount(self):
        if self.amount and self.amount < 0:
            raise ValidationError(_("Amount should be always greater than or equal to Zero!"))
    
    # Load college and courses informations from the student details master
    @api.onchange('admission_id')
    def onchange_admission_id(self):
        self.company_id = self.admission_id.curr_collage.id
        self.courses_id = self.admission_id.courses_id.id

    @api.model
    def create(self,vals):
        # if 'admission_id' in vals.keys():
        #     existing_record = self.sudo().search([('admission_id', '=', vals['admission_id'])])
        #     print(existing_record,vals.get('admission_id'))
        #     if existing_record:
        #         raise ValidationError('Admission No must be unique.')
        res = super(StudentConcession,self).create(vals)
        if not res.roll_no_id:
            raise ValidationError(_("Roll No field is shouldn't be empty!"))
        else:
            res.compute_admission_id()
        return res

    def write(self,vals):
        # if 'admission_id' in vals.keys():
        #     existing_record = self.sudo().search([('admission_id', '=', vals['admission_id'])])
        #     if existing_record:
        #         raise ValidationError('Admission No must be unique.')
        res = super(StudentConcession,self).write(vals)
        if not self.roll_no_id:
            raise ValidationError(_("Roll No field is shouldn't be empty!"))
        
        return res

    # Make concession approval request
    def send_for_approval(self):
        concession_objs = self if self.id else self.browse(self.env.context.get('active_ids'))
        for concession in concession_objs:
            if concession.state != 'draft':
                raise ValidationError(_("Selected Concession state should be in the Draft!"))
            concession.state = 'to_approve'
            concession.message_post(body=_(f"Consession is sent for First Level Approval by {self.env.user.partner_id.name}!"))

    # Finally approve the concession
    def action_to_first_level_approve(self):
        concession_objs = self if self.id else self.browse(self.env.context.get('active_ids'))
        if self.env.user.has_group('fees_management.concession_first_level_approver'):
            for concession in concession_objs:
                if concession.state != 'to_approve':
                    raise ValidationError(_("Selected all concessions should be sent for Approval State!"))
                concession.state = 'first_level_approve'
                concession.message_post(body=_(f"Consession 1st Level was approved by {self.env.user.partner_id.name}!"))
        else:
            raise ValidationError(_("You are not allowed to Approve the Concession!"))
        
    # Finally approve the concession
    def action_to_second_level_approve(self):
        concession_objs = self if self.id else self.browse(self.env.context.get('active_ids'))
        if self.env.user.has_group('fees_management.concession_second_level_approver'):
            for concession in concession_objs:
                if concession.state != 'first_level_approve':
                    raise ValidationError(_("Selected all concessions should be in the First Level Approved State!"))
                concession.state = 'approved'
                concession.message_post(body=_(f"Consession 1st Level was approved by {self.env.user.partner_id.name}!"))
        else:
            raise ValidationError(_("You are not allowed to Approve the Concession!"))
    
    # Reject and Update the concession state
    def action_to_reject(self):
        concession_objs = self if self.ids else self.browse(self.env.context.get('active_ids'))
        if self.env.user.has_group('fees_management.concession_first_level_approver') or self.env.user.has_group('fees_management.concession_second_level_approver'):
            for concession in concession_objs:
                if concession.concession_type == "special_concession" and concession.state == "approved":
                    raise ValidationError(_("Unable to revoke the approval for Special concession!"))

                if concession.state not in ('first_level_approve','to_approve','approved'):
                    raise ValidationError(_("Selected all concessions should be in the First/Second Level Approval State!"))
                concession.state = 'rejected'
                concession.message_post(body=_(f"Consession was rejected by {self.env.user.partner_id.name}!"))
        else:
            raise ValidationError(_("You are not allowed to Reject the Concession!"))
        
    # Returns Concession Rejection wizard to get the Reason
    def return_reject_wizard(self):

        return {
            "name":"Reason For Concession Rejection",
            "type":"ir.actions.act_window",
            "res_model":"concession.rejection.wizard",
            "target":"new",
            "view_mode":"form",
            "context":{'concession_id':[self.id] if self.id else self.env.context.get('active_ids')}
        }
        
    # If the request made mistakenly then set it back to draft
    def action_to_draft(self):
        if self.id:
            objs = self
        else:
            objs = self.browse(self.env.context.get('active_ids'))
        for itm in objs:
            if itm.state == 'approved':
                raise ValidationError(_("Unable to revoke the Approval for the Concession!"))
            else:
                itm.state = 'draft'
                itm.message_post(body=_(f"Set to draft by {self.env.user.partner_id.name}!"))



class InheritStudentDetails(models.Model):
        _inherit = "student.details"


        concession_ids = fields.One2many("student.concession","roll_no_id",string="Concessions")