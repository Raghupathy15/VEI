from odoo import models,fields,api,_
from datetime import datetime
import pytz


class InheritCustomPaymentConsolidatedReport(models.TransientModel):
    _inherit = "daily.detailed.payment.report.wizard"


    # Current Indian Time
    def get_current_time(self):
        user_timezone = pytz.timezone(self.env.user.tz)
        current_time = datetime.now(pytz.utc).astimezone(user_timezone)
        return current_time.strftime('%d-%b-%Y %I:%M %p')

    def get_fromatted_date_str(self,date_obj):
        user_timezone = pytz.timezone(self.env.user.tz)
        if date_obj:
            date_str = user_timezone.localize(date_obj).strftime('%d-%b-%Y %I:%M %p')
            return date_str
        else:
            return ''
        
    def get_payments(self):
        
        domain_list = [('move_type','=','out_invoice'),('state','=','posted'),('payment_state','in',['partial','in_payment','paid'])]
        payment_domain_list = [('payment_type','=','inbound'),('company_id','=',self.env.company.id)]
        
        if self.start_date:
            payment_domain_list.append(('date','>=',self.start_date))
        if self.end_date:
            payment_domain_list.append(('date','<=',self.end_date))
        else:
            self.end_date = datetime.now().date()
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
        if self.cashier_ids:
            payment_domain_list.append(('create_uid','in',self.cashier_ids.ids))

        load_payment_objs = self.env["account.payment"].search(payment_domain_list)
        invoice_ids = load_payment_objs.mapped('reconciled_invoice_ids').ids
        domain_list.append(('id','in',invoice_ids))
        invoice_objs = self.env["account.move"].search(domain_list,order="invoice_user_id asc")
       
        move_vals = {}
        move_total = 0.0
        payment_method_total = {}
        for move in invoice_objs:
            content = move.invoice_payments_widget.get('content') if move.invoice_payments_widget else []
			# content = line.get_reconciled_data()
            payment_vals = {}
            payment_ids = []
            for payment in reversed(content):

                if payment.get('account_payment_id') and payment.get('account_payment_id') in load_payment_objs.ids:
                    key = str(payment.get('account_payment_id')).strip()
                    if key in payment_vals.keys():
                        payment_vals[key]['amount'] = payment_vals.get(key)['amount'] + payment.get('amount')
                    else:
                        payment_vals[key] = {'id':payment.get('account_payment_id'),'amount':payment.get('amount'),'':payment.get('date')}
                        payment_ids.append(payment.get('account_payment_id'))

                    if payment.get('payment_method_name') in payment_method_total.keys():
                        payment_method_total[payment.get('payment_method_name')] = payment_method_total[payment.get('payment_method_name')] + payment.get('amount')
                    else:
                        payment_method_total[payment.get('payment_method_name')] = payment.get('amount')

            payment_objs = self.env['account.payment'].browse(payment_ids)
            move_vals[move.name] = {'move_obj':move,'payment_objs':payment_objs,'payment_vals':payment_vals}
            move_total += move.amount_total
        if move_vals:
            move_vals['move_total'] = move_total
            move_vals['method_vals'] = payment_method_total
        return move_vals
        