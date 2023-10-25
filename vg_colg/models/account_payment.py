from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class AccountPaymentMethod(models.Model):
    _inherit = "account.payment.method"

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res['gpay'] = {'mode': 'multi', 'domain': [('type', '=', 'bank')]}
        return res

class InheritAccountPayment(models.Model):
    _inherit = "account.payment"


    is_advance_payment = fields.Boolean(string="Is Advance Payment?")
    token_fee_id = fields.Many2one('token.fees',string="Token Fees")
    admission_id = fields.Many2one('admission.confirmation',string="Admission Id")

    is_gpay_method = fields.Boolean(string="Is Gpay Method")
    gpay_mobile = fields.Char(string="Gpay mobile", copy=False)
    gpay_upi = fields.Char(string="UPI ID", copy=False)
    gpay_remarks = fields.Char(string="Remarks", copy=False)
    gpay_attachment = fields.Binary(string="Attachment", copy=False)
    gpay_attachment_name = fields.Char(string="Attachment name", copy=False)

    @api.onchange('payment_method_line_id')
    def onchange_gpay_payment_method_line_id(self):
        if self.payment_method_line_id:
            if self.payment_method_line_id.name in ['Cheque', 'DD']:
                self.is_custom_method = True
            else:
                self.is_custom_method = False
            if self.payment_method_line_id.name in ['Gpay']:
                self.is_gpay_method = True
            else:
                self.is_gpay_method = False


    _sql_constraints = [
        ('unique_admission_token','UNIQUE(admission_id,token_fee_id,is_advance_payment)','Payment already exist for in the combination of Admission and Token fee!')
    ]

    @api.model
    def create(self,vals):
        res = super(InheritAccountPayment,self).create(vals)
        if self.env.context.get('student_advance_payment_flag'):
            for payment in res:
                payment.action_post()
                payment.admission_id.state = ('admission_list' if payment.amount >= self.env.context.get('token_amount') else 'partially_paid')
                payment.admission_id.action_send_admission_list()
        else:
            if res.admission_id:
                # NEW CODE FOR TOKEN FEE FILTER
                admission = self.env['admission.list'].search([('admission_id','=',res.admission_id.id)],limit=1)
                if admission:
                    token_fees = self.env['token.fees'].search(
                        [('stream_id', '=', admission.stream_id.id), ('company_id', '=', admission.curr_collage.id),
                         ('grade_id', '=', admission.grade_id.id), ('course_id', '=', admission.courses_id.id),
                         ('degree_level_id', '=', admission.degree_level_id.id), ('batch_id', '=', admission.batch_id.id)])
                    admission_obj = admission.admission_id
                    if token_fees:
                        payment_total = sum(
                            admission_obj.advance_payment_ids.filtered(lambda x: x.payment_type == 'inbound').mapped(
                                "amount"))
                        token_fees_total = sum(token_fees.fees_lines.mapped('amount'))
                        if payment_total >= token_fees_total:
                            admission.write({
                                'partially_paid': False,
                                'fully_paid': True,
                            })
        return res
    

    def action_draft(self):
        for payment in self:
            if payment.token_fee_id and payment.admission_id and not self.env.context.get('admin_here'):
                raise ValidationError(_("Payment has been posted so can't set it back to draft, as it is Advance payment. Please contact your administrator!"))
        
            # if payment.reconciled_bill_ids or payment.reconciled_invoice_ids and not self.env.context.get('admin_here'):
            #     raise ValidationError(_("Payment has been posted so can't set it back to draft, as it is Used for Invoice/Bills. Please contact your administrator!"))
            
        res = super(InheritAccountPayment,self).action_draft()
        return res


class AccountRegisterPayments(models.TransientModel):
    _inherit = "account.payment.register"

    is_gpay_method = fields.Boolean(string="Is Gpay Method")
    gpay_mobile = fields.Char(string="Gpay mobile", copy=False)
    gpay_upi = fields.Char(string="UPI ID", copy=False)
    gpay_remarks = fields.Char(string="Remarks", copy=False)
    gpay_attachment = fields.Binary(string="Attachment", copy=False)
    gpay_attachment_name = fields.Char(string="Attachment name", copy=False)

    @api.onchange('payment_method_line_id')
    def onchange_gpay_payment_method_line_id(self):
        if self.payment_method_line_id:
            if self.payment_method_line_id.name in ['Cheque','DD']:
                self.is_custom_method = True
            else:
                self.is_custom_method = False
            if self.payment_method_line_id.name in ['Gpay']:
                self.is_gpay_method = True
            else:
                self.is_gpay_method = False

    def _create_payment_vals_from_wizard(self, batch_result):
        payment_vals = super()._create_payment_vals_from_wizard(batch_result)
        payment_vals['is_gpay_method'] = self.is_gpay_method
        payment_vals['gpay_mobile'] = self.gpay_mobile
        payment_vals['gpay_upi'] = self.gpay_upi
        payment_vals['gpay_remarks'] = self.gpay_remarks
        payment_vals['gpay_attachment'] = self.gpay_attachment
        payment_vals['gpay_attachment_name'] = self.gpay_attachment_name
        return payment_vals

    def _prepare_payment_vals(self, invoices):
        res = super(AccountRegisterPayments, self)._prepare_payment_vals(
            invoices)
        check_gpay_ids = self.env['account.payment.method'].search(
            [('code', 'in', ['gpay'])])
        if self.payment_method_id.id in check_gpay_ids.ids:
            res.update({
                'is_gpay_method': self.is_gpay_method,
                'gpay_mobile': self.gpay_mobile,
                'gpay_upi': self.gpay_upi,
                'gpay_remarks': self.gpay_remarks,
                'gpay_attachment': self.gpay_attachment,
                'gpay_attachment_name': self.gpay_attachment_name,
            })
        return res