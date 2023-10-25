import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class AdmissionConfirmation(models.Model):
	_name = 'admission.confirmation'
	_description = 'Admission Confirmation'
	_order = 'id desc'
	_rec_name = "admission_no"
	_inherit = ['mail.thread']

	
	admission_inquiry_count = fields.Integer('Admission Inquiry',compute='compute_count')
	token_fees_count = fields.Integer('Token Fees',compute='compute_count')
	name = fields.Char(string="Name of the Student")
	name_initial = fields.Char(string="Initial",default = '')
	admission_no = fields.Char(string="Admission No")
	caste = fields.Char('Caste', required=True)
	name_of_the_parent_guardian = fields.Char('Name of the parent/Guardian', required=True)
	parent_guardian_occupation = fields.Char('Parent/Guardian occupation', required=True)
	last_institute_name = fields.Char('Name')
	education_qualification = fields.Char('Education Qualification')
	stages_id = fields.Many2one('stages.master', string='Stage')
	date_of_birth = fields.Date(string='Date Of Birth', required=True)
	age = fields.Char('Age')
	bus_root = fields.Char('Bus Root')
	email = fields.Char('Email', required=True)
	location = fields.Selection(string='Location', selection=[('sankagiri', 'Sankagiri'), ('thirichengodu','Thirichengodu')], required=True)
	aadhar_no = fields.Char('Aadhar No')
	degree_level_id = fields.Many2one('degree.level.master', string="Degree", required=True)
	quota_id = fields.Many2one('quota.master',string="Quota", required=True)
	accomodation_check_box = fields.Selection(string="Accommodation",
											  selection=[('dayscholar', 'Dayscholar'), ('hosteler', 'Hosteler')], default='dayscholar', required=True)
	room = fields.Selection(string="Room", selection=[
		('ord', 'ORD'),
		('sr', 'SR'),
		('dlx_3', 'DLX(3)'),
		('dlx_4', 'DLX(4)'),
		('dlx_ac', 'DLX AC')])
	stud_entry = fields.Selection(string="Student Entry", selection=[
		('new', 'New Joinee'),
		('lateral_entry', 'Lateral Entry'),
		('re_join', 'Re Joining'),
		('college_transfer', 'College Transfer')])
	gate_pass_id = fields.Many2one('student.admission', string="Gate Pass ID", readonly=True)
	courses_id = fields.Many2one('courses.master', string="Course")
	community_id = fields.Many2one('community.master', string="Community", required=True)
	institute_last_studied = fields.Many2one('last.studied.institutions', string="Institute last studied")
	accomadation = fields.Char()
	c_phone = fields.Char('Phone')
	c_mobile = fields.Char('Mobile')
	remarks = fields.Text('Remarks')
	referred_by = fields.Char('Referred By', readonly=True)
	emergeny_contact = fields.Char('Emergeny contact')
	parent_signature = fields.Char('Parent Signature')
	student_signature = fields.Char('Student Signature')
	staff_signature = fields.Char('Staff Signature')
	education_qualification_ids = fields.One2many('education.qualification', 'admission_confirmation_id', string="Education Qualification")
	fee_details_ids = fields.One2many('fee.details', 'admission_confirmation_id', string="Fee Details")
	inspection_ids = fields.One2many('inspection.image', 'admission_confirmation_id', string="Fee Details")
	fees_count = fields.Integer(string='Fees Receipt', compute='_fees_count')
	curr_collage = fields.Many2one('res.company', string="Collage Name", required=True)
	# Communication address
	street = fields.Char()
	street2 = fields.Char()
	zip_code = fields.Char()
	city = fields.Char()
	state_id = fields.Many2one("res.country.state")
	country_id = fields.Many2one('res.country')
	special_quota_id = fields.Many2one('special.quota', string="Special Quota")
	state = fields.Selection(string='Admission Status', selection=[('new', 'Councelling'),
																	('partially_paid', 'Partially paid'),
																	('token_fees', 'Payment pending'),
																	('admission_list', 'Admission Confirmed'),
																	('cancelled','Cancelled')],
			readonly=True, copy=False, index=True, track_visibility='always', default='new')
	cancel_remark = fields.Text(string="Canceled Remarks", track_visibility='always', readonly=True)
	councelling_room = fields.Char(string="Councelling Room",track_visibility='always')
	token_num = fields.Char(string="Token Number")
	mobile_number = fields.Char(string="Mobile Number", required=True)
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
	refunded = fields.Boolean(string="Refunded",default=False)
	refund_count = fields.Integer(compute="get_credit_note_count",string="Refund")
	refund_sum = fields.Float(compute="get_credit_note_count",string="Refund Sum")
	fees_sum = fields.Float(compute="_fees_count",string="Fees Sum")
	concession_ids = fields.One2many('student.concession','admission_id',string="Concessions")
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

	guardian_mobile = fields.Char(string="Gaurdian Mobile No")
	guardian_whatsapp_no = fields.Char(string="Gaurdian WhatsApp No")

	present_door_no= fields.Char(string="Door No")
	present_street= fields.Char(string="Street Name")
	present_district= fields.Char(string="District", required=False)
	present_taluk= fields.Char(string="Taluk", required=False)
	present_city= fields.Char(string="City")
	present_state= fields.Many2one("res.country.state")
	present_zip= fields.Char(string="Zip Code", required=False)

	perm_door_no= fields.Char(string="Door No")
	perm_street= fields.Char(string="Street Name")
	perm_district= fields.Char(string="District")
	perm_taluk= fields.Char(string="Taluk")
	perm_city= fields.Char(string="City")
	perm_state= fields.Many2one("res.country.state")
	perm_zip= fields.Char(string="Zip Code")
	student_phone_no = fields.Char('Phone')
	student_whatsapp = fields.Char('WhatsApp Number')
	grade_id = fields.Many2one('grade.master',string="Grade")
	stream_id = fields.Many2one('stream.master',string="Stream")
	batch_id = fields.Many2one('batch.courses.master',string="Batch")
	active = fields.Boolean(string="Active",default=True)
	advance_payment_ids = fields.One2many("account.payment","admission_id",string="Advance Payments")

	relationship_ids = fields.One2many('relationship.master', 'admission_id', string="Relationship")
	health_info_ids = fields.One2many('health.information.master', 'admission_id', string="Health Information")

	student_account_no = fields.Char('Student Account number')
	student_ifsc = fields.Char('IFSC code')
	student_bank = fields.Char('Bank Name')
	student_branch = fields.Char('Branch Name')
	father_account_no = fields.Char('Father Account number')
	father_ifsc = fields.Char('IFSC code')
	father_bank = fields.Char('Bank Name')
	father_branch = fields.Char('Branch Name')

	_sql_constraints = [
		('unique_admission_constraints','UNIQUE(date_of_birth,aadhar_no,stream_id,company_id,grade_id,degree_level_id,courses_id,batch_id)','Combination of Date of Birth, Aadhar No, Stream, College, Grade, Degree, Course and Batch Must be Unique!'),
		('unique_admission_no','UNIQUE(admission_no)','Admission No should be unique per record!'),
	]


	@api.onchange('stream_id')
	def onchange_stream_id(self):
		self.curr_collage = False

	@api.onchange("curr_collage")
	def onchange_curr_collage_id(self):
		self.grade_id = False

	@api.onchange("grade_id")
	def onchange_grade_id(self):
		self.degree_level_id = False

	@api.onchange("degree_level_id")
	def onchange_degree_level_id(self):
		self.courses_id = False

	@api.onchange("courses_id")
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
		one_time_fees_obj = self.env['one.time.fees'].search([('stream_id','=',self.stream_id.id),('college_id','=',self.ref_college_id.id),('course_ids','in',self.courses_id.id),('degree_level_id','=',self.degree_level_id.id),('quota_id','=',self.quota_id.id)])
		one_time_fees_line_ids = []
		for fees in one_time_fees_obj:
			one_time_fees_line_ids.extend(fees.fees_ids.ids)

		self.one_time_fees_count = len(one_time_fees_line_ids)


	def action_open_one_time_fees(self):
		one_time_fees_obj = self.env['one.time.fees'].search([('stream_id','=',self.stream_id.id),('college_id','=',self.ref_college_id.id),('course_ids','in',self.courses_id.id),('degree_level_id','=',self.degree_level_id.id),('quota_id','=',self.quota_id.id)])
		one_time_fees_line_ids = []
		for fees in one_time_fees_obj:
			one_time_fees_line_ids.extend(fees.fees_ids.ids)

		action = {
			'name': _("Fees Details"),
			'view_mode': 'tree',
			'type': 'ir.actions.act_window',
			'res_model': 'one.time.fees.line',
			'context':{'readonly':True},
			'domain': [('id','in',one_time_fees_line_ids)]
		}
		return action
	

	def action_open_advance_payments(self):
		partner_obj = self.env['res.partner'].search([('aadhar_no','=',self.aadhar_no)],limit=1)

		action = {
			'name': _("Advance Payment"),
			'view_mode': 'tree,form',
			'type': 'ir.actions.act_window',
			'res_model': 'account.payment',
			'context':
					{'default_partner_id': partner_obj.id,
						'default_payment_type': 'inbound',
						'default_partner_type': 'customer',
						'default_is_advance_payment': True,
						'default_admission_id': self.id,},
			'domain': [('id','in',self.advance_payment_ids.filtered(lambda x:x.is_advance_payment).ids)]
		}
		return action


	def get_compute_fees_heads_count(self):
		fees_obj = self.env['fees.management'].search([('stream_id','=',self.stream_id.id),('company_id','=',self.ref_college_id.id),('course_ids','in',self.courses_id.id),('degree_level_id','=',self.degree_level_id.id),('quota_id','=',self.quota_id.id)])
		fees_heads_ids = []
		for fees in fees_obj:
			fees_heads_ids.extend(fees.fees_ids.ids)

		self.fees_heads_count = len(fees_heads_ids)

	def action_open_fees_heads(self):
		fees_obj = self.env['fees.management'].search([('stream_id','=',self.stream_id.id),('company_id','=',self.ref_college_id.id),('course_ids','in',self.courses_id.id),('degree_level_id','=',self.degree_level_id.id),('quota_id','=',self.quota_id.id)])
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


	# Get Related credit note count
	def get_credit_note_count(self):
		for itm in self:
			objs = self.env['account.move'].search([('admission_id','=',itm.id),('move_type','=','out_refund'),('state','=','posted')])
			count = len(objs)
			itm.refund_sum = sum(objs.mapped('amount_total'))
			itm.refund_count = count

	def action_open_credit_note(self):
		action = {
			'name':_("Refund"),
			'view_mode':'tree,form',
			'type':'ir.actions.act_window',
			'res_model':'account.move',
			'domain':[('move_type','=','out_refund'),('admission_id','=',self.id)]
		}
		return action

	def compute_count(self):
		for record in self:
			record.admission_inquiry_count = self.env['student.admission'].search_count([('id', '=', record.gate_pass_id.id)])
			record.token_fees_count = len(self.env['token.fees'].search([('stream_id','=',record.stream_id.id),('company_id','=',record.curr_collage.id),('grade_id','=',record.grade_id.id),('course_id', '=', record.courses_id.id),
													('degree_level_id', '=', record.degree_level_id.id),('batch_id','=',record.batch_id.id)]))

	@api.model_create_multi
	def create(self, vals_lst):
		from datetime import datetime, date
		for vals in vals_lst:
			current_year = datetime.now().year
			vals.update({
				'admission_no': 'ADM'+ "/" + str(current_year) + "/" +self.env['ir.sequence'].next_by_code('admission.confirmation.seq', sequence_date=False) or _('New')
			})
		return super(AdmissionConfirmation, self).create(vals_lst)

	def _fees_count(self):
		for record in self:
			objs = self.env['account.move'].search([('move_type', '=', 'out_invoice'),('partner_id.aadhar_no', '=', record.aadhar_no)])
			record.fees_count = len(objs)
			record.fees_sum = sum(objs.mapped('amount_total'))

	def action_open_fees(self):
		action = {
			'name': _("Fees Receipt"),
			'view_mode': 'tree,form',
			'type': 'ir.actions.act_window',
			'res_model': 'account.move',
			'domain': [('move_type', '=', 'out_invoice'),('partner_id.aadhar_no', '=', self.aadhar_no)],
		}
		return action
	
	def action_mark_refunded(self):
		for itm in self:
			itm.refunded = True	
			objs = self.env['admission.list'].search([('admission_id','=',self.id)])
			for line in objs:
				line.refunded = True

	def action_back_to_councelling(self):
		for itm in self:
			itm.state = 'new'	
			itm.refunded = False
			itm.message_post(body=_(f"Set back to Councelling set by {self.env.user.partner_id.name}!"))
			objs = self.env['admission.list'].search([('admission_id','=',self.id)])
			for line in objs:
				line.state = 'draft'
				line.message_post(body=_(f"Set back to Document collection set by {self.env.user.partner_id.name}!"))
	

	def action_cancel(self):
		form_view = self.env.ref('vg_colg.onhold_remark_view_id')
		return {
			'name': "Cancel Remarks",
			'view_mode': 'form',
			'view_type': 'form',
			'view_id': form_view.id,
			'res_model': 'onhold.remark',
			'type': 'ir.actions.act_window',
			'context': {'default_cancel':'admission_confirm'},
			'target': 'new',
		}


	def get_inquiry(self):
		"""Inquiry smart button"""
		self.ensure_one()
		return {
			'type': 'ir.actions.act_window',
			'name': 'Student Inquiry',
			'view_mode': 'tree,form',
			'res_model': 'student.admission',
			'domain': [('id', '=', self.gate_pass_id.id)],
			'context': "{'create': False}"
		}

	def action_open_token_fees(self):
		action = {
			'name': _("Token Fees Structure"),
			'view_mode': 'tree',
			'type': 'ir.actions.act_window',
			'res_model': 'token.fees',
			'domain': [('stream_id','=',self.stream_id.id),('company_id','=',self.curr_collage.id),('grade_id','=',self.grade_id.id),('course_id', '=', self.courses_id.id),
													('degree_level_id', '=', self.degree_level_id.id),('batch_id','=',self.batch_id.id)],
		}
		return action

	@api.onchange('gate_pass_id')
	def _onchange_cgate_pass_id(self):
		if self.gate_pass_id:
			self.community_id = self.gate_pass_id.community_id
			self.caste = self.gate_pass_id.caste
			self.name_of_the_parent_guardian = self.gate_pass_id.parent_guardian_name
			self.parent_guardian_occupation = self.gate_pass_id.parent_guardian_occupation
			self.date_of_birth = self.gate_pass_id.birth_date
			self.courses_id = self.gate_pass_id.courses_id.id
			self.name = self.gate_pass_id.name
			self.institute_last_studied = self.gate_pass_id.last_studied_institution_id.id
			self._onchange_set_age()

	@api.onchange('date_of_birth')
	def _onchange_set_age(self):
		today = datetime.date.today()
		for admission in self:
			if admission.date_of_birth:
				admission.age = today.year - admission.date_of_birth.year - (
							(today.month, today.day) < (admission.date_of_birth.month, admission.date_of_birth.day))

	def calculate_fees(self):
		for admission in self:
			if admission.courses_id.id:
				fees_list = []
				courses = self.env['fees.management'].search([('course_ids', 'in', admission.courses_id.id),('quota_id', '=', admission.quota_id.id)]).ids
				for course in self.env['fees.management'].browse(courses):
					for line in course.fees_ids:
							admission_fee = self.env['fee.details'].create({'name': line.product_id.name, 'amount': line.amount})
							fees_list.append(admission_fee.id)
				admission.write({'fee_details_ids': [(6,0,fees_list)]})

	def action_token_fees(self):
		advance_pay_object = self.env['account.payment']
		token_fees = self.env['token.fees'].search([('stream_id','=',self.stream_id.id),('company_id','=',self.curr_collage.id),('grade_id','=',self.grade_id.id),('course_id', '=', self.courses_id.id),
													('degree_level_id', '=', self.degree_level_id.id),('batch_id','=',self.batch_id.id)],
															  limit=1)
		# token_fees = self.env['token.fees'].search([],limit=1)
		if not token_fees:
			raise ValidationError(_("Unable to Generate Token Fees Please check the Token Fees Master in the combination of Stream, College, Grade, Degree, Course and Batch!"))
		
		partner_obj = self.env['res.partner'].search([('aadhar_no','=',self.aadhar_no)])
		# for record in self:
		# 	move = self.env['account.move'].create({
		# 									'admission_id':record.id,
		# 									'move_type':'out_invoice',
		# 									'partner_id':partner_obj.id,
		# 									'is_advance_payment':True,
		# 									})
		# 	product = self.env.ref('vg_colg.product_product_token_fees')
		# 	move_line_values = [
		# 		(0, 0, {
		# 			'product_id': product.id,
		# 			'name': product.name,
		# 			'move_id': move.id,
		# 			'price_unit': token_fees.fees,
		# 			'tax_ids': False,
		# 			'account_id': 1,
		# 		}),
		# 	]

		# 	move.write({'line_ids': move_line_values})
		# self.state='token_fees'
		amount = sum([fee.amount for fee in token_fees.fees_lines])
		return {
				'type': 'ir.actions.act_window',
				'name': 'Advance Payment',
				'res_model': 'account.payment',
				'view_mode': 'form',
				'view_id': self.env.ref('account.view_account_payment_form').id,
				'target': 'new',
				'context': {
					        'token_amount' : amount,
					        'student_advance_payment_flag': True,
					        'default_partner_id': partner_obj.id,
							'default_payment_type': 'inbound',
							'default_partner_type': 'customer',
							'default_is_advance_payment': True,
							'default_token_fee_id': token_fees.id,
							'default_admission_id': self.id,
							'default_amount': sum([fee.amount for fee in token_fees.fees_lines]) or 0.0},
			}

	def action_send_admission_list(self):
		if not self.curr_collage:
			raise UserError(_("Kindly select the Collage Name !.."))
		admission_list_obj = self.env["admission.list"]
		relationship_data = []
		if self.relationship_ids:
			for relationship_id in self.relationship_ids:
				relationship_data.append((0, 0, {
					'guardian_id': relationship_id.guardian_id.id,
					'status': relationship_id.status,
					'company': relationship_id.company,
					'mobile': relationship_id.mobile,
					'whatsapp': relationship_id.whatsapp,
					'occupation': relationship_id.occupation,
					'birth_place': relationship_id.birth_place,
					'aadhar_no': relationship_id.aadhar_no,
					'phote': relationship_id.phote,
					'phote_name': relationship_id.phote_name,
				}))
		documents = self.env['document.templates'].sudo().search([])
		template_list = []
		for document in documents:
			for template in document.template_ids:
				if self.courses_id and template.courses_ids and self.courses_id.id in template.courses_ids.ids:
					template_list.append((0, 0, {
						'name': template.name,
						'is_mandatory': template.is_mandatory
					}))

		for vals in self:
			admission = admission_list_obj.sudo().create({'name': self.name,
											  'name_initial': self.name_initial,
											  'inquiry_id': self.gate_pass_id.id,
											  'admission_id': self.id,
											  'aadhar_no': self.aadhar_no,
											  'email': self.email,
											  'curr_collage': self.curr_collage.id,
											  'birth_date': self.date_of_birth,
											  'age': self.age,
											  'community_id': self.community_id.id,
											  'caste': self.caste,
											  'bus_root': self.bus_root,
											  'name_of_the_parent_guardian': self.name_of_the_parent_guardian,
											  'parent_guardian_occupation': self.parent_guardian_occupation,
											  'referred_by': self.referred_by,
											  'emergeny_contact': self.emergeny_contact,
											  'courses_id': self.courses_id.id,
											  'quota_id': self.quota_id.id,
											  'accomodation_check_box': self.accomodation_check_box,
											  'room': self.room,
											  'token_num': self.token_num,
											  'stages_id': self.stages_id.id,
											  'institute_last_studied': self.institute_last_studied.id,
											  'education_qualification': self.education_qualification,
											  'street': self.street,
											  'street2': self.street2,
											  'zip_code': self.zip_code,
											  'city': self.city,
											  'state_id': self.state_id.id,
											  'country_id': self.country_id.id,
											  'c_phone': self.c_phone,
											  'c_mobile': self.c_mobile,
											  'remarks': self.remarks,
											  'batch_start_year': self.batch_start_year,
											  'batch_id': self.batch_id.id,
											  'duration': self.duration,
											  'batch_ending_year': self.batch_ending_year,
											  'education_qualification': self.education_qualification,
											  'stud_entry': self.stud_entry,
											  'stream_id': self.stream_id.id,
											  'grade_id': self.grade_id.id,
											  'degree_level_id': self.degree_level_id.id,
											  'gender': self.gender,
											  'blood_group': self.blood_group,
											  'sslc_school': self.sslc_school,
											  'hsc_school': self.hsc_school,
											  'referred_name': self.referred_name,
											  'ref_designation_id': self.ref_designation_id.id,
											  'ref_college_id': self.ref_college_id.id,
											  'ref_mobile': self.ref_mobile,
											  "name_initial": self.name_initial,
											  "father_name": self.father_name,
											  "father_mobile": self.father_mobile,
											  "father_whatsapp_no": self.father_whatsapp_no,
											  "father_occupation": self.father_occupation,
											  "father_birth_place": self.father_birth_place,
											  "father_aadhar_no": self.father_aadhar_no,
											  "mother_name": self.mother_name,
											  "mother_mobile": self.mother_mobile,
											  "mother_whatsapp_no": self.mother_whatsapp_no,
											  "mother_occupation": self.mother_occupation,
											  "mother_birth_place": self.mother_birth_place,
											  "mother_aadhar_no": self.mother_aadhar_no,
											  "guardian_mobile": self.guardian_mobile,
											  "guardian_whatsapp_no": self.guardian_whatsapp_no,
											  "present_door_no": self.present_door_no,
											  "present_street": self.present_street,
											  "present_district": self.present_district,
											  "present_taluk": self.present_taluk,
											  "present_city": self.present_city,
											  "present_state": self.present_state.id,
											  "present_zip": self.present_zip,
											  "perm_door_no": self.perm_door_no,
											  "perm_street": self.perm_street,
											  "perm_district": self.perm_district,
											  "perm_taluk": self.perm_taluk,
											  "perm_city": self.perm_city,
											  "perm_state": self.perm_state.id,
											  "perm_zip": self.perm_zip,
											  "student_phone_no": self.student_phone_no,
											  "student_whatsapp": self.student_whatsapp,

											  "student_account_no": self.student_account_no,
											  "student_ifsc": self.student_ifsc,
											  "student_bank": self.student_bank,
											  "student_branch": self.student_branch,

											  "father_account_no": self.father_account_no,
											  "father_ifsc": self.father_ifsc,
											  "father_bank": self.father_bank,
											  "father_branch": self.father_branch,

											  "relationship_ids": relationship_data if relationship_data else False,
											  "inspection_ids": template_list if template_list else False,
											  'education_qualification_ids': [
												  (6, 0, self.education_qualification_ids.ids)],
											  'health_info_ids': [(6, 0, self.health_info_ids.ids)],
											  })

			# NEW CODE FOR TOKEN FEE FILTER
			token_fees = self.env['token.fees'].search(
				[('stream_id', '=', admission.stream_id.id), ('company_id', '=', admission.curr_collage.id),
				 ('grade_id', '=', admission.grade_id.id), ('course_id', '=', admission.courses_id.id),
				 ('degree_level_id', '=', admission.degree_level_id.id), ('batch_id', '=', admission.batch_id.id)])
			admission_obj = admission.admission_id

			if token_fees :
				payment_total = sum(
					admission_obj.advance_payment_ids.filtered(lambda x: x.payment_type == 'inbound').mapped("amount"))

				token_fees_total = sum(token_fees.fees_lines.mapped('amount'))
				if payment_total >= token_fees_total:
					admission.write({
						'partially_paid': False,
						'fully_paid': True,
					})

			self.state = "admission_list"


class AccountMove(models.Model):
	_inherit = 'account.move'

	word_num = fields.Char(string="Amount In Words:", compute='_amount_in_word')

	is_advance_payment= fields.Boolean(string="Is Advance Payment")
	admission_id = fields.Many2one(comodel_name="admission.confirmation", string="Admission No")
	mobile_number = fields.Char('Mobile',related='admission_id.c_mobile',store=True)
	aadhaar_code = fields.Char('Aadhaar No.',related='admission_id.aadhar_no', store=True)
	date = fields.Date(string="Date", default=fields.Date.today)
	courses_id = fields.Many2one('courses.master', string="Courses",related='admission_id.courses_id',store=True)
	email = fields.Char(string='Email ID', related='admission_id.email',store=True)
	concession_available = fields.Boolean(string="Concession Applicable",compute="get_concession_applicablility")
	concession_applied = fields.Boolean(string="Concession Applied",default=False)
	allocated_concession_amount = fields.Boolean(string="Allocated Concession Amount")
	fees_id = fields.Many2one('fees.management',string="Fees")


	def get_concession_applicability(self):
		for move in self:
			if move.move_type == 'out_invoice' and move.details_id.concession_ids.filtered(lambda x:x.state == 'approved'):
				if move.concession_balance > 0:
					move.concession_available = True
				else:
					move.concession_available = False
			else:
				move.concession_available = False

	@api.onchange('admission_id')
	def _onchange_admission_id(self):
		if self.admission_id and self.admission_id.courses_id:
			token_fees = self.env['token.fees'].search([('stream_id','=',self.admission_id.stream_id.id),('company_id','=',self.admission_id.curr_collage.id),('grade_id','=',self.admission_id.grade_id.id),('course_id', '=', self.admission_id.courses_id.id),
													('degree_level_id', '=', self.admission_id.degree_level_id.id),('batch_id','=',self.admission_id.batch_id.id)],limit=1)
			if token_fees:
				product = self.env.ref('vg_colg.product_product_token_fees')
				self.invoice_line_ids = [(6, 0, [])]
				self.invoice_line_ids = [(0, 0, {
					'product_id': product.id,
					'name': product.name,
					'price_unit': token_fees.fees,
					'tax_ids': False
				})]

	def _amount_in_word(self):
		for rec in self:
			amount_total = rec.amount_total_signed
			rec.word_num = str(rec.company_id.currency_id.amount_to_text(amount_total))

	@api.onchange('admission_id')
	def _onchange_partner(self):
		if self.admission_id:
			partner_obj = self.env['res.partner'].search([('aadhar_no','=',self.admission_id.aadhar_no)])
			if partner_obj:
				self.partner_id = partner_obj.id
			if not partner_obj:
				partner_obj.create({'name':self.admission_id.name,
									'aadhar_no': self.admission_id.aadhar_no})
				self._onchange_partner()

	@api.model
	def create(self, values):
		result = super(AccountMove, self).create(values)
		admission_rec = self.env['admission.list'].search([('admission_id', '=', result.admission_id.id)])
		if admission_rec:
			admission_rec.write({'payment_state': result.payment_state})			
		return result

# class AccountPaymentRegister(models.TransientModel):
# 	_inherit = 'account.payment.register'

# 	def action_create_payments(self):
# 		res = super(AccountPaymentRegister, self).action_create_payments()
# 		active_ids = self._context.get("active_ids", [])
# 		invoices = self.env["account.move"].browse(active_ids)
# 		if invoices:
# 			admission_rec = self.env['admission.list'].search(
# 				[('admission_id', '=', invoices.admission_id.id)])
# 			admission_rec.payment_state = invoices.payment_state
# 			if invoices.payment_state =='paid':
# 				invoices.admission_id.action_send_admission_list()
# 				pass
# 			elif invoices.payment_state =='partial':
# 				invoices.admission_id.sudo().write({
# 					'state' : 'partially_paid'
# 				})
# 		return res