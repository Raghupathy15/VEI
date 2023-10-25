from odoo import models,fields,api,_


class InheritStudentDetails(models.Model):
    _inherit = "student.details"

    invoice_line_ids = fields.One2many('account.move.line','student_id',string="Fees Line Details")
    invoice_ids = fields.One2many('account.move','details_id',string="Fees Details")
    wallet_balance = fields.Float(string="Balance Amount",compute="get_balance")
    incoming_payment_balance = fields.Float(string="Balance",compute="get_balance")
    outgoing_payment_balance = fields.Float(string="Balance",compute="get_balance")
    refund_total = fields.Float(string="Refund Total",compute="get_balance")
    invoice_due = fields.Float(string="Collection Due",compute="get_balance")
    concession_ids = fields.One2many('student.concession','roll_no_id',string="Concession")
    concession_balance = fields.Float(string="Concession Balance",compute="get_balance")


    # Compute get balance
    def get_balance(self):
        for student in self:
            student.wallet_balance = 0.0
            # Load partner obj
            partner_obj = self.env['res.partner'].search([('aadhar_no','=',student.aadhar_no)],limit=1)

            # Incoming and Outgoing payment
            payment_obj = self.env['account.payment'].search([('partner_id','=',partner_obj.id)])
            incoming_payment = sum([payment.amount_balance for payment in payment_obj if payment.payment_type == 'inbound']) 
            outgoing_payment = sum([payment.amount_balance for payment in payment_obj if payment.payment_type == 'outbound']) 
            student.incoming_payment_balance = incoming_payment
            student.outgoing_payment_balance = outgoing_payment
            
            # Invoice Due
            invoice_amount_due = sum([invoice.amount_residual for invoice in self.invoice_ids.filtered(lambda x:x.move_type == 'out_invoice')])
            student.invoice_due = invoice_amount_due

            # Refund Total
            refund_amount = sum([invoice.amount_residual for invoice in self.invoice_ids.filtered(lambda x:x.move_type == 'out_refund')])
            student.refund_total = refund_amount

            # Concession Balance
            student.concession_balance = sum([concession.concession_balance_amount for concession in student.concession_ids if concession.state == 'approved'])

            # Wallet Balance
            student.wallet_balance = (incoming_payment + student.concession_balance + refund_amount) - (invoice_amount_due - outgoing_payment)
            

    # Action method to return Concession
    def action_open_student_concession(self):
        self.env['student.concession']
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Concession',  
            'res_model': 'student.concession', 
            'view_mode': 'tree,form', 
            # 'views': [(self.env.ref('account.view_out_credit_note_tree').id, 'tree'),(False,'form')],
            'target': 'current',  
            'domain': [('id','in',self.concession_ids.ids)]
        }
        return action


    # Action method to return refund
    def action_open_student_refund(self):
        self.env['account.move']
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Refunds',  
            'res_model': 'account.move', 
            'view_mode': 'tree,form', 
            'views': [(self.env.ref('account.view_out_credit_note_tree').id, 'tree'),(False,'form')],
            'target': 'current',  
            'domain': [('id','in',self.invoice_ids.ids),('move_type','=','out_refund')]
        }
        return action

    # Action method to return Incoming Payments
    def action_open_incoming_payment(self):
        partner_obj = self.env['res.partner'].search([('aadhar_no','=',self.aadhar_no)],limit=1)
        payment_objs = self.env['account.payment'].search([('partner_id','=',partner_obj.id),('payment_type','=','inbound')])
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Student Payments',  
            'res_model': 'account.payment', 
            'view_mode': 'tree,form', 
            # 'views': [(self.env.ref('fees_management.fee_account_move_line_tree_view').id, 'tree')],
            'context': {'default_payment_type':'inbound','default_partner_id':self.partner_id.id},
            'target': 'current',  
            'domain': [('id','in',payment_objs.ids)]
        }
        return action
    
    # Action method to return Outgoing Payments
    def action_open_outgoing_payment(self):
        partner_obj = self.env['res.partner'].search([('aadhar_no','=',self.aadhar_no)],limit=1)
        payment_objs = self.env['account.payment'].search([('partner_id','=',partner_obj.id),('payment_type','=','outbound')])
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Student Payments',  
            'res_model': 'account.payment', 
            'view_mode': 'tree,form', 
            # 'views': [(self.env.ref('fees_management.fee_account_move_line_tree_view').id, 'tree')],
            'context': {'default_payment_type':'outbound','default_partner_id':self.partner_id.id},
            'target': 'current',  
            'domain': [('id','in',payment_objs.ids)]
        }
        return action

    # Action method to return Fees Details
    def action_open_fees_line_details(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Fees Line Details',  
            'res_model': 'account.move.line', 
            'view_mode': 'tree', 
            'views': [(self.env.ref('fees_management.fee_account_move_line_tree_view').id, 'tree')],
            'target': 'current',  
            'domain': [('id','in',self.invoice_line_ids.ids),('move_id.move_type','=','out_invoice')]
        }
        return action
    
    # Action method to return Fees Details
    def action_open_fees_details(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Fees Details',  
            'res_model': 'account.move', 
            'view_mode': 'tree,form', 
            'views': [(self.env.ref('account_extend.fee_account_move_tree_view').id, 'tree'),(False,'form')],
            'target': 'current',  
            'domain': [('id','in',self.invoice_ids.ids),('move_type','=','out_invoice')]
        }
        return action