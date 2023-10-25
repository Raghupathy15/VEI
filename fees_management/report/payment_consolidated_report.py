from odoo import models,fields,api,_
from datetime import datetime
import pytz
import logging

class InheritPaymentConsolidatedReport(models.TransientModel):
    _inherit = "payment.consolidated.report.wizard"


    # Current Indian Time
    def get_current_time(self):
        user_timezone = pytz.timezone(self.env.user.tz)
        current_time = datetime.now(pytz.utc).astimezone(user_timezone)
        return current_time.strftime('%d-%b-%Y %I:%M %p')

    def get_payments(self):
        
        domain_list = [('move_type','=','out_invoice')]
        
        if self.start_date:
            domain_list.append(('invoice_date','>=',self.start_date))
        if self.end_date:
            domain_list.append(('invoice_date','<=',self.end_date))
        
        if self.env.company:
            domain_list.append(('company_id','=',self.env.company.id))
        if self.course_id:
            domain_list.append(('course_id','=',self.course_id.id))
        if self.batch_id:
            domain_list.append(('batch_id','=',self.batch_id.id))
        if self.semester_id:
            domain_list.append(('semester_id','=',self.semester_id.id))
        if self.term_id:
            domain_list.append(('fees_for_id','=',self.term_id.id))
        if self.status and self.status == 'true':
            domain_list.append(('details_id.active','=',True))
        if self.status and self.status == 'false':
            domain_list.append(('details_id.active','=',False))
        if not self.status:
            domain_list.append(('details_id.active','=',False))

        invoice_objs = self.env["account.move"].search(domain_list)
        logging.info('--------------------Move Domain--------------------')
        logging.info(domain_list)
        invoice_line_objs = self.env['account.move.line']

        for move in invoice_objs:
            invoice_line_objs += move.invoice_line_ids #.filtered(lambda x:x.payment_state != 'not_paid')

        line_vals = {}
        for line in invoice_line_objs:
            # print('-----payment-----',line.payment_ref_ids)
            key = str(line.student_id)
            if key in line_vals.keys():
                line_vals[key]['lines'] = line_vals[key]['lines'] + line
            else:
                line_vals[key] = {'student_id':line.student_id,'lines':line}
        
        return line_vals