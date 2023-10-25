import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class StudentAdmission(models.Model):
	_name = 'student.admission'
	_description = 'Student Admission'
	_rec_name = "seq_code"
	_order = 'id desc'
	_inherit = ['mail.thread']

	def compute_count(self):
		for record in self:
			record.admission_confirmation_count = self.env['admission.confirmation'].search_count([('gate_pass_id', '=', self.id)])

	@api.depends('name')
	def _compute_set_batch_of_year(self):
		for std in self:
			std.batch = "%s-%s"% (datetime.datetime.now().strftime("%Y"),int(datetime.datetime.now().strftime("%Y"))+1)

	def _default_welcome_mssg_subject(self):
		welcome_mssg_subject = self.env['ir.config_parameter'].sudo().get_param('welcome_mssg_subject')
		return welcome_mssg_subject

	def _default_welcome_mssg_body(self):
		welcome_mssg_body = self.env['ir.config_parameter'].sudo().get_param('welcome_mssg_body')
		return welcome_mssg_body

	welcome_mssg_subject = fields.Char(string='Subject',default=lambda self: self._default_welcome_mssg_subject())
	welcome_mssg_body = fields.Html(string='Body',default=lambda self: self._default_welcome_mssg_body())

	admission_confirmation_count = fields.Integer('Admission confirmation',compute='compute_count')
	name = fields.Char('Name of the Student')
	name_initial = fields.Char('Initial')
	email = fields.Char(string='Email ID', required=True)
	aadhar = fields.Integer(string='Aadhar No')
	seq_code = fields.Char('Seq Code')
	referred_name = fields.Char('Referred Name')
	ref_designation_id = fields.Many2one('hr.job', string='Designation')
	ref_college_id = fields.Many2one('res.company', string='College')
	ref_mobile = fields.Char(string='Mobile')
	batch = fields.Char('Batch', compute='_compute_set_batch_of_year')
	parent_guardian_name = fields.Char('Parent / Guardian Name', required=True)
	parent_guardian_occupation = fields.Char('Parent / Guardian Occupation', required=True)
	caste = fields.Char('Caste',required=True)
	pin_code = fields.Char(string="Pin Code", required=True)
	aadhaar_code = fields.Char('Aadhaar No.', required=True)
	mobile_number = fields.Char(string="Mobile Number",required=True)
	whatsapp_number = fields.Char(string="Whatsapp Number", required=True)
	ug_regn_number = fields.Char(string="+2 / UG Regn Number")
	group_ug_number = fields.Char(string="+2 Group / UG Branch")
	councelling_room = fields.Char(string="Councelling Room",track_visibility='always')
	total_marks_ug = fields.Integer(string="+2 Total Marks / UG %")
	birth_date = fields.Date('Date of Birth', required=True)
	institution_group_id = fields.Many2one('institution.group.master', string="Institution Group")
	courses_id = fields.Many2one('courses.master', string="Courses")
	place_id = fields.Many2one('place.city.master', string="Place", required=True)
	taluk_id = fields.Many2one('taluk.master', string="Taluk", required=True)
	district_id = fields.Many2one('district.master', string="District", required=True)
	last_studied_institution_id = fields.Many2one('last.studied.institutions', string="Last Studied Institution")
	community_id = fields.Many2one('community.master', string="Community", required=True)
	referred_by_id = fields.Many2one('reference.master', string="Referred By")
	degree_level_id = fields.Many2one('degree.level.master', string="Degree", required=True)
	company_id = fields.Many2one('res.company', 'College Name', required=True, index=True)
	location = fields.Selection(string='Location', selection=[('sankagiri', 'Sankagiri'), ('thirichengodu','Thirichengodu')], required=True)
	state = fields.Selection(string='Inquiry Status', selection=[('inquiry', 'Inquiry'), ('confirmed','Sent for Admission')],
			readonly=True, copy=False, index=True, track_visibility='always', default='inquiry')
	fees_count = fields.Integer(string='Fees', compute='_fees_count')
	token_num = fields.Char(string="Token Number")
	create_dt = fields.Date(compute='_compute_create_date', store=True,
							string="Create Date")
	inquiry_mode = fields.Selection(string='Inquiry mode', selection=[('direct', 'Direct'), 
									('reference','Reference'),
									('pro','PRO'),
									('others','Others'),
									],copy=False, track_visibility='always')
	gender = fields.Selection(string='Gender', selection=[('male', 'Male'), 
									('female','Female'),('others', 'Others')
									],copy=False, track_visibility='always')
	blood_group = fields.Selection(string='Blood Group', selection=[('a+', 'A+'), 
									('a-','A-'),
									('b+','B+'),
									('b-','B-'),
									('o+','O+'),
									('o-','O-'),
									('ab-','AB-'),
									('ab+','AB+'),
									('a1b+','A1B+'),
									],copy=False, track_visibility='always')

	batch_start_year = fields.Char(string='Batch starting year', default=lambda year: str(datetime.datetime.now().year))
	duration = fields.Char(string='Duration')
	batch_ending_year = fields.Char(string='Batch ending year')
	grade_id = fields.Many2one('grade.master',string="Grade")
	stream_id = fields.Many2one('stream.master',string="Stream")
	quota_id = fields.Many2one('quota.master',string="Quota",required=True)
	batch_id = fields.Many2one('batch.courses.master',string="Batch")
	active = fields.Boolean(string="Active",default=True)

	_sql_constraints = [
		('unique_admission_constraints','UNIQUE(birth_date,aadhaar_code,stream_id,company_id,grade_id,degree_level_id,courses_id,batch_id)','Combination of Date of Birth, Aadhar No, Stream, College, Grade, Degree, Course and Batch Must be Unique!'),
	]


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

	@api.depends('create_date')
	def _compute_create_date(self):
		for rec in self:
			rec.create_dt = rec.create_date.date()
	
	def _fees_count(self):
		for record in self:
			record.fees_count = len(self.env['account.move'].search([('partner_id.aadhar_no', '=', record.aadhaar_code)]))

	def action_open_fees(self):
		action = {
			'name': _("Fees"),
			'view_mode': 'tree,form',
			'type': 'ir.actions.act_window',
			'res_model': 'account.move',
			'domain': [('partner_id.aadhar_no', '=', self.aadhaar_code)],
			'context': {
				'create': False,
			}
		}
		return action

	@api.model_create_multi
	def create(self, vals_lst):
		from datetime import datetime, date
		for vals in vals_lst:
			current_year = datetime.now().year
			vals.update({
				'seq_code': 'INQ/'+ str(current_year) + "/" + self.env['ir.sequence'].next_by_code('student.admn.seq.no')
			})
		return super(StudentAdmission, self).create(vals_lst)

	def get_stud_confirm(self):
		"""Stud confirmation smart button"""
		self.ensure_one()
		return {
			'type': 'ir.actions.act_window',
			'name': 'Student Admission Confirmation',
			'view_mode': 'tree,form',
			'res_model': 'admission.confirmation',
			'domain': [('gate_pass_id', '=', self.id)],
			'context': "{'create': False}"
		}

	def action_confirm_admission(self):
		if not self.councelling_room:
			raise UserError(_("Kindly Allocate Councelling Room !.."))
		if not self.inquiry_mode:
			raise UserError(_("Kindly select 'Inquiry Mode' of the student !.."))
		# To generate Token No
		from datetime import datetime, date
		if self.courses_id:
			coursh = self.env['courses.master'].sudo().browse([self.courses_id.id])
			if coursh:
				inquiry = self.search([('courses_id','=',coursh.id),('create_dt','=',date.today())])
				# if not inquiry:
				if len(inquiry) <= 1:
					coursh.sudo().write({
						'sequence' : 1
					})
					self.token_num = coursh.token_num + '001'
				else:
					coursh.sudo().write({
						'sequence':  coursh.sequence + 1
					})
					sequence_str = str(coursh.sequence)
					sequence = sequence_str.zfill(3)
					self.token_num = coursh.token_num + sequence

		# template_id = self.env.ref('vg_colg.mail_student_admission_template').sudo()
		# if template_id:
		# 	template_id.send_mail(self.id, force_send=True, email_values={"email_to": self.email})

		pr_id = self.env['admission.confirmation'].create({
			'location': self.location,
			'father_name': self.parent_guardian_name,
			'father_occupation': self.parent_guardian_occupation,
			'student_whatsapp': self.whatsapp_number,
			'name': self.name,
			'name_initial': self.name_initial,
			'mobile_number': self.mobile_number,
			'gate_pass_id': self.id,
			'community_id': self.community_id.id,
			'caste': self.caste,
			'name_of_the_parent_guardian': self.parent_guardian_name,
			'parent_guardian_occupation': self.parent_guardian_occupation,
			'institute_last_studied': self.last_studied_institution_id.id,
			'referred_by': self.referred_by_id.name,
			'courses_id': self.courses_id.id,
			'quota_id': self.quota_id.id,
			'date_of_birth': self.birth_date,
			'street': self.place_id.name,
			'street2': self.taluk_id.name,
			'city': self.district_id.name,
			'zip_code': self.pin_code,
			'councelling_room': self.councelling_room,
			'aadhar_no': self.aadhaar_code,
			'email': self.email,
			'c_mobile': self.mobile_number,
			'token_num': self.token_num,
			'degree_level_id': self.degree_level_id.id,
			'curr_collage': self.company_id.id,
			'gender': self.gender,
			'blood_group': self.blood_group,
			'referred_name': self.referred_name,
			'ref_designation_id': self.ref_designation_id.id,
			'ref_college_id': self.ref_college_id.id,
			'ref_mobile': self.ref_mobile,
			'batch_start_year': self.batch_start_year,
			'duration': self.duration,
			'batch_ending_year': self.batch_ending_year,
			'batch_id':self.batch_id.id,
			'stream_id': self.stream_id.id,
			'grade_id': self.grade_id.id

		})

		partner_obj = self.env['res.partner'].search([('aadhar_no','=',self.aadhaar_code)])
		if not partner_obj:
			partner_obj.create({'name':self.name,
								'aadhar_no': self.aadhaar_code})
		self.state = 'confirmed'


class FeesMaster(models.Model):
    _name = 'fees.master'
    _description = 'Fees Master'

    name = fields.Char('Name')
    course_id = fields.Many2one('courses.master', string="courses")
    hotsel_fees = fields.Selection(string='Hotsel Fees', selection=[('dayscholar', 'Dayscholar'), ('hosteler', 'Hosteler')], default='dayscholar')
    room_type = fields.Selection(string="Room Type", selection=[
        ('ord', 'ORD'),
        ('sr', 'SR'),
        ('dlx_3', 'DLX(3)'),
        ('dlx_4', 'DLX(4)'),
        ('dlx_ac', 'DLX AC')])
    stages_id = fields.Many2one('stages.master', string='Stage')
    # fees_ids = fields.One2many('fees.detail.master', 'fees_id', string="Fees")