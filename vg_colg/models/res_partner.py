from odoo import fields, models, api, _
from odoo.osv import expression


class ResPartner(models.Model):
	_inherit = 'res.partner'
	# _rec_name = 'custom_display_name'

	aadhar_no = fields.Char(string="Aadhar No")
	student_role_no = fields.Char(string="Role No",compute="get_compute_role_no",store=True)

	def get_compute_role_no(self):
		for partner in self:
			student_obj = self.env['student.details'].search([('aadhar_no','=',partner.aadhar_no)],limit=1)
			if partner.partner_share and student_obj and partner.aadhar_no and not partner.is_company and not self.env['res.users'].sudo().search([('partner_id','=',partner.id)]):
				partner.student_role_no = student_obj.role_no or ''
				partner.name = (partner.student_role_no or '') + ' - ' + (student_obj.name or '')
			else:
				partner.student_role_no = ''
