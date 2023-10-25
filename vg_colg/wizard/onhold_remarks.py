# -*- coding: utf-8 -*-
from odoo import fields, models, api,_
from odoo.exceptions import ValidationError


class  OnHoldRemark(models.TransientModel):
	_name = 'onhold.remark'
	_description = 'Onhold remark Wizard'

	name = fields.Text('Remarks',required=True)
	cancel = fields.Selection([('admission_list','Admission List'),('admission_confirm','Admission Confirmed')],'is Cancel')


	def action_reject_remark(self):
		active_id = self.env.context.get('active_id')
		rec = self.env['admission.list'].browse(int(active_id))
		rec.write({'onhold_state': rec.state})
		rec.write({'onhold_remarks':self.name,'state':'onhold'})

	def action_admission_list_cancel_remark(self):
		print("Admission list Cancel!")
		active_id = self.env.context.get('active_id')
		rec = self.env['admission.list'].browse(int(active_id))
		rec.write({'cancel_remark':self.name,'state':'cancelled'})
		for itm in rec:
			template_id = self.env.ref('vg_colg.mail_cancel_admission_list_template').sudo()
			if template_id:
				template_id.send_mail(itm.id, force_send=True, email_values={"email_to": itm.email})
			itm.message_post(body=_(f"This record was cancelled by {self.env.user.partner_id.name}!"))
			itm.admission_id.write({'cancel_remark':self.name,'state':'cancelled'})
	

	def action_admission_confirm_cancel_remark(self):
		# print("Admission Confirm Cancelled!")
		active_id = self.env.context.get('active_id')
		recs = self.env['admission.confirmation'].browse(int(active_id))
		for itm in recs:
			if itm.advance_payment_ids.filtered(lambda x:x.state == 'posted'):
				raise ValidationError(_("Please Cancel the payment which has posted, Inorder to cancel the Admission!"))
			itm.write({'cancel_remark':self.name,'state':'cancelled'})
			template_id = self.env.ref('vg_colg.mail_cancel_admission_template').sudo()
			if template_id:
				template_id.send_mail(itm.id, force_send=True, email_values={"email_to": itm.email})
			objs = self.env['admission.list'].search([('admission_id','=',itm.id)])
			# print(objs.admission_id.admission_no)
			for line in objs:
				line.message_post(body=_(f"This record was cancelled by {self.env.user.partner_id.name}!"))
				line.write({'cancel_remark':self.name,'state':'cancelled'})