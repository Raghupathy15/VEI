from odoo import models,fields,api,_
import pytz
from datetime import datetime

class InheritCustomReportWizard(models.TransientModel):
    _inherit = "custom.report.wizard"


    def get_sum(self,fee_vals,paid_amount,fees_head):
        if fees_head in fee_vals.keys():
            fee_vals[fees_head] = fee_vals[fees_head] + paid_amount
        else:
            fee_vals[fees_head] = paid_amount
        print(fee_vals)
        return fee_vals
    
    # Current Indian Time
    def get_current_time(self):
        user_timezone = pytz.timezone(self.env.user.tz)
        current_time = datetime.now(pytz.utc).astimezone(user_timezone)
        return current_time.strftime('%d-%b-%Y %I:%M %p')
    
    def get_payments(self):
        start_date = self.start_date
        end_date = self.end_date
        domain_list = [('move_type','=','out_invoice')]
        if start_date:
            domain_list.append(('invoice_date','>=',self.start_date))
        if end_date:
            domain_list.append(('invoice_date','<=',self.end_date))
        if self.course_id:
            domain_list.append(('course_id','=',self.course_id.id))
        if self.batch_id:
            domain_list.append(('batch_id','=',self.batch_id.id))
        if self.semester_id:
            domain_list.append(('semester_id','=',self.semester_id.id))
        if self.term_id:
            domain_list.append(('fees_for_id','=',self.term_id.id))
        if self.cashier_ids:
            domain_list.append(('invoice_user_id','in',self.cashier_ids.ids))
        if self.status and self.status == 'true':
            domain_list.append(('details_id.active','=',True))
        if self.status and self.status == 'false':
            domain_list.append(('details_id.active','=',False))
        if not self.status:
            domain_list.append(('details_id.active','=',False))
        
        invoice_objs = self.env["account.move"].search(domain_list,order="invoice_user_id")
        invoice_line_objs = self.env['account.move.line']

        dict_vals = {}
        for move in invoice_objs:
            invoice_line_objs += move.invoice_line_ids.filtered(lambda x:x.payment_state != 'not_paid')
        
        # college code, Batch, Term,Sem,Fee Description, Cashier name, Payment type, Collected amount
        for line in invoice_line_objs:
            key = line.company_id.college_code if line.company_id.college_code else '-'
            key += '_'+line.batch_id.name if line.batch_id.name else '-'
            key += '_'+line.fees_for_id.name if line.fees_for_id.name else '-'
            key += '_'+line.semester_id.name if line.semester_id.name else '-'
            key += '_'+line.name if line.name else '-'
            key += '_'+line.move_id.invoice_user_id.name if line.move_id.invoice_user_id.name else '-'
            key = key.replace(' ','')
            
            if key in dict_vals.keys():
                dict_vals[key]['paid_amount'] = dict_vals[key]['paid_amount']+line.paid_amount
            else:
                dict_vals[key] = {'college_code':line.company_id.college_code,'batch':line.batch_id.name,'term':line.fees_for_id.name,\
                                    'semester':line.semester_id.name,'fees_head':line.name,'sales_person':line.move_id.invoice_user_id.name,\
                                    'paid_amount':line.paid_amount} #,'payment_method':payment.payment_method_line_id.name}
        
        return dict_vals