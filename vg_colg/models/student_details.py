import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError
import barcode
from odoo.modules.module import get_module_path
import base64
import os
from datetime import datetime


class StudentDetails(models.Model):
	_name = 'student.details'
	_description = 'Student Details'
	_rec_name = "role_no"
	_order = 'id desc'
	_inherit = ['mail.thread']


	def _fees_count(self):
		for record in self:
			record.fees_count = len(self.env['account.move'].search([('move_type', '=', 'out_invoice'),
										('partner_id.aadhar_no', '=', record.aadhar_no)]))
			record.fees_structure_count = len(self.env['fees.management'].search([('course_ids', 'in', record.courses_id.id),
										('degree_ids', 'in', record.degree_id.id)]))

	display_name = fields.Char(string="Name",compute="get_compute_student_name")
	partner_id = fields.Many2one("res.partner",compute="_get_load_partner",string="Contact Ref.")
	fees_count = fields.Integer(string='Fees Receipt', compute='_fees_count')
	fees_structure_count = fields.Integer(string='Fees Structure', compute='_fees_count')
	role_no = fields.Char('Roll No')
	aadhar_no = fields.Char('Aadhar No')
	role_no_seq = fields.Char('Role No sequence')
	name = fields.Char('Name of the Student',track_visibility='always')
	email = fields.Char(string='Email ID',track_visibility='always')
	company_id = fields.Many2one('res.company', 'College Name', required=True, index=True)
	enquiry_id = fields.Many2one('student.admission', string="Enquiry No", readonly=True)
	section_id = fields.Many2one('section.master', string="Section", track_visibility='always')
	date_of_birth = fields.Date(string='Date Of Birth', track_visibility='always',required=True)
	age = fields.Char('Age')
	community_id = fields.Many2one('community.master', string="Community", track_visibility='always')
	caste = fields.Char('Caste', track_visibility='always')
	name_of_the_parent_guardian = fields.Char('Guardian Name', required=True, track_visibility='always')
	parent_guardian_occupation = fields.Char('Guardian occupation', required=True, track_visibility='always')
	referred_by = fields.Char('Referred By', track_visibility='always')
	emergeny_contact = fields.Char('Emergeny contact')
	courses_id = fields.Many2one('courses.master', string="Course", track_visibility='always')
	# quota = fields.Selection(string="Quota", selection=[('general', 'General Quota'), 
							# ('management', 'Management Quota')], required=True, track_visibility='always')
	quota_id = fields.Many2one('quota.master',string="Quota",track_visibility='always',required=True)
	accomodation_check_box = fields.Selection(string="Accommodation",
											  selection=[('dayscholar', 'Dayscholar'), ('hosteler', 'Hosteler')], 
											  default='dayscholar', required=True, track_visibility='always')
	stud_entry = fields.Selection(string="Student Entry", selection=[
		('new', 'New Joinee'),
		('lateral_entry', 'Lateral Entry'),
		('re_join', 'Re Joining'),
		('college_transfer', 'College Transfer')])
	state = fields.Selection(string='Student Status', selection=[('regular', 'Regular'), ('alumini','Alumini')],
			readonly=True, copy=False, index=True, track_visibility='always', default='regular')

	room = fields.Selection(string="Room", selection=[
							('ord', 'ORD'),
							('sr', 'SR'),
							('dlx_3', 'DLX(3)'),
							('dlx_4', 'DLX(4)'),
							('dlx_ac', 'DLX AC')],track_visibility='always')
	stages_id = fields.Many2one('stages.master', string='Stage')
	institute_last_studied = fields.Many2one('last.studied.institutions', string="Institute last studied", track_visibility='always')
	education_qualification = fields.Char('Education Qualification', track_visibility='always')
	degree_id = fields.Many2one('degree.master', string="Degree")
	degree_level_id = fields.Many2one('degree.level.master', string="Degree")

	# Communication address
	street = fields.Char()
	street2 = fields.Char()
	zip_code = fields.Char()
	city = fields.Char()
	state_id = fields.Many2one("res.country.state")
	country_id = fields.Many2one('res.country')
	c_phone = fields.Char('Phone')
	c_mobile = fields.Char('Mobile')

	remarks = fields.Text('Remarks')
	education_qualification_ids = fields.One2many('education.qualification', 'student_details_id', string="Education Qualification")
	fee_details_ids = fields.One2many('fee.details', 'student_details_id', string="Fee Details")
	inspection_ids = fields.One2many('inspection.image', 'student_details_id', string="Fees Details")
	special_quota_id = fields.Many2one('special.quota', string="Special Quota")
	bus_root = fields.Char('Bus Root')
	barcode_image = fields.Binary('Barcode Image', compute='_compute_barcode_image_set', attachment=True, store=True,
								  copy=False)
	gender = fields.Selection(string='Gender', selection=[('male', 'Male'), 
									('female','Female'),
									],copy=False, track_visibility='always')
	blood_group = fields.Selection(string='Blood Group', selection=[('a+', 'A+'), 
									('a-','A-'),
									('b+','B+'),
									('b-','B-'),
									('o+','O+'),
									('o-','O-'),
									('ab-','AB-'),
									('ab+','AB+'),
									('a1+','A1+'),
									('a1b+','A1B+'),
									],copy=False, track_visibility='always')
	sslc_school = fields.Char(string="SSLC School",track_visibility='always')
	hsc_school = fields.Char(string="HSC School",track_visibility='always')
	referred_name = fields.Char('Referred Name')
	ref_designation_id = fields.Many2one('hr.job', string='Designation')
	ref_college_id = fields.Many2one('res.company', string='College')
	ref_mobile = fields.Char(string='Mobile')

	batch_start_year = fields.Char(string='Batch starting year')
	duration = fields.Char(string='Duration')
	batch_ending_year = fields.Char(string='Batch ending year')
	barcode_no = fields.Char(string='Barcode No')
	fees_heads_count = fields.Integer(string="Fees Heads Count",default=0,compute="get_compute_fees_heads_count")
	one_time_fees_count = fields.Integer(string="One Time Fees Count",default=0,compute="get_compute_one_time_fees_count")
	name_initial = fields.Char(string="Initial",default = '')
	father_name = fields.Char(string="Father")
	father_mobile = fields.Char(string="Father Mobile No")
	father_whatsapp_no = fields.Char(string="Father WhatsApp No")
	father_occupation = fields.Char(string="Father Occupation")
	father_birth_place = fields.Char(string="Father Birth Place")
	father_aadhar_no = fields.Char(string="Father Aadhar No.")
	mother_name = fields.Char(string="Mother Name")
	mother_mobile = fields.Char(string="Mother Mobile")
	mother_whatsapp_no = fields.Char(string="Mother WhatsApp No")
	mother_occupation = fields.Char(string="Mother Occupation")
	mother_birth_place = fields.Char(string="Mother Birth Place")
	mother_aadhar_no = fields.Char(string="Mother Aadhar No.")

	guardian_mobile = fields.Char(string="Guardian Mobile No")
	guardian_whatsapp_no = fields.Char(string="Guardian WhatsApp No")

	present_door_no= fields.Char(string="Door No")
	present_street= fields.Char(string="Street Name")
	present_district= fields.Char(string="District")
	present_taluk= fields.Char(string="Taluk")
	present_city= fields.Char(string="City")
	present_state= fields.Many2one("res.country.state")
	present_zip= fields.Char(string="Zip Code")

	perm_door_no= fields.Char(string="Door No")
	perm_street= fields.Char(string="Street Name")
	perm_district= fields.Char(string="District")
	perm_taluk= fields.Char(string="Taluk")
	perm_city= fields.Char(string="City")
	perm_state= fields.Many2one("res.country.state")
	perm_zip= fields.Char(string="Zip Code")
	student_phone_no = fields.Char('Phone')
	student_whatsapp = fields.Char('WhatsApp Number')
	stream_id = fields.Many2one("stream.master",string="Stream")
	grade_id = fields.Many2one("grade.master",string="Grade")
	batch_id = fields.Many2one('batch.courses.master',string="Batch")
	active = fields.Boolean(string="Active",default=True)

	relationship_ids = fields.One2many('relationship.master', 'student_id', string="Relationship")
	health_info_ids = fields.One2many('health.information.master', 'student_id', string="Health Information")

	student_account_no = fields.Char('Student Account number')
	student_ifsc = fields.Char('IFSC code')
	student_bank = fields.Char('Bank Name')
	student_branch = fields.Char('Branch Name')
	father_account_no = fields.Char('Father Account number')
	father_ifsc = fields.Char('IFSC code')
	father_bank = fields.Char('Bank Name')
	father_branch = fields.Char('Branch Name')
	admission_id = fields.Many2one('admission.confirmation', string="Admission No")
	is_hod = fields.Boolean(string="HOD", default=False, compute="compute_is_hod")

	_sql_constraints = [
		('unique_student_details_constraints','UNIQUE(date_of_birth,aadhar_no,stream_id,company_id,grade_id,degree_level_id,courses_id,batch_id)','Combination of Date of Birth, Aadhar No, Stream, College, Grade, Degree, Course and Batch is already exist!'),
	]

	def compute_is_hod(self):
		for rec in self:
			if rec.env.user.has_group('vg_colg.vei_hod_group'):
				rec.is_hod = True
			else:
				rec.is_hod = False

	def get_compute_student_name(self):
		for student in self:
			student.display_name = (student.role_no or ' ') + ' - ' +(student.name or ' ')

	@api.onchange('aadhar_no')
	def onchange_aadhar_no(self):
		if self._origin.aadhar_no:
			partner_obj = self.env['res.partner'].search([('aadhar_no','=',self._origin.aadhar_no)])
			for i in partner_obj:
				i.aadhar_no = self.aadhar_no

	def action_move_alumini_list(self):
		active_ids = self.env.context.get('active_ids', [])
		for active in active_ids:
			rec = self.env['student.details'].browse(int(active))
			rec.write({'state':'alumini'})

	@api.onchange('stream_id')
	def onchange_stream_id(self):
		self.company_id = False

	@api.onchange("company_id")
	def onchange_company_id(self):
		self.grade_id = False

	@api.onchange("grade_id")
	def onchange_grade_id(self):
		self.degree_level_id = False

	@api.onchange("degree_level_id")
	def onchange_degree_level_id(self):
		self.courses_id = False

	@api.onchange("courses_id")
	@api.depends("courses_id")
	def onchange_courses_id(self):
		self.batch_id = self.courses_id.batch_id.id
		if self.batch_id:	
			self.onchange_batch_id()

	@api.depends("batch_id")
	def onchange_batch_id(self):
		if self.batch_id:
			self.batch_start_year = self.batch_id.start_year
			self.duration = str(self.batch_id.duration)
			self.batch_ending_year = self.batch_id.end_year
		else:
			self.batch_start_year = ''
			self.duration = ''
			self.batch_ending_year = ''


	def get_compute_one_time_fees_count(self):
		one_time_fees_obj = self.env['one.time.fees'].search([('course_ids','in',self.courses_id.id),('degree_ids','in',self.degree_id.id),('quota_id','=',self.quota_id.id)])
		one_time_fees_line_ids = []
		for fees in one_time_fees_obj:
			one_time_fees_line_ids.extend(fees.fees_ids.ids)

		self.one_time_fees_count = len(one_time_fees_line_ids)


	def action_open_one_time_fees(self):
		one_time_fees_obj = self.env['one.time.fees'].search([('course_ids','in',self.courses_id.id),('degree_ids','in',self.degree_id.id),('quota_id','=',self.quota_id.id)])
		one_time_fees_line_ids = []
		for fees in one_time_fees_obj:
			one_time_fees_line_ids.extend(fees.fees_ids.ids)

		action = {
			'name': _("One Time Fees"),
			'view_mode': 'tree',
			'type': 'ir.actions.act_window',
			'res_model': 'one.time.fees.line',
			'context':{'readonly':True},
			'domain': [('id','in',one_time_fees_line_ids)]
		}
		return action


	def get_compute_fees_heads_count(self):
		fees_obj = self.env['fees.management'].search([('course_ids','in',self.courses_id.id),('degree_ids','in',self.degree_id.id),('quota_id','=',self.quota_id.id)])
		fees_heads_ids = []
		for fees in fees_obj:
			fees_heads_ids.extend(fees.fees_ids.ids)

		self.fees_heads_count = len(fees_heads_ids)

	def action_open_fees_heads(self):
		fees_obj = self.env['fees.management'].search([('course_ids','in',self.courses_id.id),('degree_ids','in',self.degree_id.id),('quota_id','=',self.quota_id.id)])
		fees_heads_ids = []
		for fees in fees_obj:
			fees_heads_ids.extend(fees.fees_ids.ids)

		action = {
			'name': _("Fees Details"),
			'view_mode': 'tree',
			'type': 'ir.actions.act_window',
			'res_model': 'fees.details',
			'context':{'readonly':True},
			'domain': [('id','in',fees_heads_ids)]
		}
		return action

	@api.model
	def create(self, vals):
		result = super(StudentDetails, self).create(vals)
		if not vals.get('role_no') and result.company_id and result.courses_id:
			student_sequence_str = str(result.company_id.custom_sequence)
			student_sequence = student_sequence_str.zfill(3)
			if result.stud_entry == 'lateral_entry':
				result.role_no = str(datetime.now().year)[2:] + result.courses_id.token_num + 'LE' + student_sequence
			elif result.stud_entry == 're_join':
				result.role_no = str(datetime.now().year)[2:] + result.courses_id.token_num + 'RE' + student_sequence
			else:
				result.role_no = str(datetime.now().year)[2:] + result.courses_id.token_num + student_sequence
			result.company_id.write({'custom_sequence': result.company_id.custom_sequence + 1})
		result.server_action_create_contacts()
		return result
	
	def write(self,vals):
		res = super(StudentDetails, self).write(vals)
		self.server_action_create_contacts()
		return res

	def action_open_fees(self):
		action = {
			'name': _("Fees Receipt"),
			'view_mode': 'tree,form',
			'type': 'ir.actions.act_window',
			'res_model': 'account.move',
			'domain': [('move_type', '=', 'out_invoice'),('partner_id.aadhar_no', '=', self.aadhar_no),('partner_id.aadhar_no', '!=', False)],
		}
		return action

	def action_open_fees_structure(self):
		action = {
			'name': _("Fees Structure"),
			'view_mode': 'tree,form',
			'type': 'ir.actions.act_window',
			'res_model': 'fees.management',
			'domain': [('course_id', '=', self.courses_id.id),('degree_id', '=', self.degree_id.id)],
		}
		return action

	# To create imported records in res.partner
	def action_create_contacts(self):
		student_obj = self.env['student.details'].search([])
		for record in student_obj:
			partner_obj = self.env['res.partner'].search([('aadhar_no','=',record.aadhar_no)])
			if not partner_obj:
				obj = partner_obj.create({'name':record.name,
									'aadhar_no': record.aadhar_no})
				
	# Server Action
	def server_action_create_contacts(self):
		for record in self:
			partner_obj = self.env['res.partner'].search([('aadhar_no','=',record.aadhar_no)])
			if not partner_obj:
				obj = partner_obj.create({'name':record.name,
									'aadhar_no': record.aadhar_no})
				
	def _get_load_partner(self):
		for student in self:
			partner_obj = self.env['res.partner'].search([('aadhar_no','=',student.aadhar_no)],limit=1)
			student.partner_id = partner_obj.id
			
									
	def custom_create_contacts(self):
		partner_obj = self.env['res.partner'].search([('aadhar_no','=',self.aadhar_no)],limit=1)
		if not partner_obj:
			obj = partner_obj.create({'name':self.name,
								'aadhar_no': self.aadhar_no})
			return obj
		else:
			return partner_obj

	def action_transfer_college(self):
		if self._context and self._context.get('active_ids'):
			if len(self._context.get('active_ids')) != 1:
				raise UserError(_("Kindly select only record for College Transfer"))
			else:
				student_id = self.browse(self._context.get('active_id'))
				action = {
					'type': 'ir.actions.act_window',
					'name': _('Transfer College'),
					'res_model': 'transfer.college.wizard',
					'view_mode': 'form',
					'target': 'new',
					'context': {'active_id': self.id, 'default_student_id': student_id.id, 'default_current_company_id': student_id.company_id.id, },
					'views': [[False, 'form']]
				}
				return action

	def action_transfer_courses(self):
		if self._context and self._context.get('active_ids'):
			if len(self._context.get('active_ids')) != 1:
				raise UserError(_("Kindly select only record for College Transfer"))
			else:
				student_id = self.browse(self._context.get('active_id'))
				action = {
					'type': 'ir.actions.act_window',
					'name': _('Transfer Courses'),
					'res_model': 'transfer.courses.wizard',
					'view_mode': 'form',
					'target': 'new',
					'context': {'active_id': self.id, 'default_student_id': student_id.id,
								'default_courses_id': student_id.courses_id.id,
								'default_degree_id': student_id.degree_id.id},
					'views': [[False, 'form']]
				}
				return action

	@api.depends('barcode_no')
	def _compute_barcode_image_set(self):
		"""
		Trigger the change of barcode image when the aadhar_no is modified.
		-------------------------------------------------------------------
		@param barcode: object pointer
		"""
		for rec in self:
			if rec.barcode_no:
				my_code = barcode.get_barcode_class('code128')
				module_path = get_module_path('vg_colg')
				module_path += '/static/image/'
				my_code(rec.barcode_no).save(module_path + str(rec.barcode_no))
				module_path += str(rec.barcode_no) + '.svg'
				rec.write({'barcode_image': base64.encodebytes(open(module_path, "rb").read())})
				rec.barcode_image = base64.b64encode(open(module_path, "rb").read())
				os.remove(module_path)

	@api.onchange('barcode_no')
	def onchange_barcode_no(self):
		for record in self:
			self._compute_barcode_image_set()