from odoo import models, fields, api, exceptions, _

class HrAttendance(models.Model):
	_inherit = "hr.attendance"

	late = fields.Boolean(string='Late?',readonly=True)
	late_time = fields.Char(string='Late Time',readonly=True,default='00:00:00')
	extra_hour = fields.Char(string='Extra Hours',readonly=True,default='00:00:00')
	empl_id = fields.Char(string='Employee ID') 
	status = fields.Selection(selection=[
		('working', 'Working'),
		('leave', 'Leave')], string='Status',tracking=True,copy=False)
	

	def action_raise_leave(self):
		attd_leave = self.env['hr.leave'].search([('attendance_id','=',self.id),('state','not in',('refuse','draft'))])
		view_id = self.env.ref('hr_holidays.hr_leave_view_form').id
		if attd_leave:
			return {
				'type': 'ir.actions.act_window',
				'name': 'Leave Form',
				'res_model': 'hr.leave',
				'view_mode': 'form',
				'views': [(view_id, 'form')],
				'view_id': view_id,
				'target': 'current',
				'res_id':attd_leave.id,
				'context': {'default_attendance_id':self.id},
			}
		else:
			return {
				'type': 'ir.actions.act_window',
				'name': 'Leave Form',
				'res_model': 'hr.leave',
				'view_mode': 'form',
				'views': [(view_id, 'form')],
				'view_id': view_id,
				'target': 'current',
				'context': {'default_attendance_id':self.id},
			}