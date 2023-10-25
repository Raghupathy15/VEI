import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date

class SpecialConsessionType(models.Model):
    _name = "special.concession.type"
    _desc = "Configuration master to store special consession the type"

    name = fields.Char(string="Name",required=True)
    technical_name = fields.Char(string="Technical Name",required=True)
    
class GeneralConcessionType(models.Model):
    _name = "general.concession.type"
    _desc = "Configuration master to store general consession the type"

    name = fields.Char(string="Name",required=True)
    technical_name = fields.Char(string="Technical Name",required=True)

class AdmissionList(models.Model):
	_name = 'admission.list'
	_description = 'Admission List'
	_order = 'id desc'
	_inherit = ['mail.thread', 'mail.activity.mixin']


	def compute_count(self):
		for record in self:
			record.admission_inquiry_count = self.env['student.admission'].search_count([('id', '=', self.inquiry_id.id)])
			record.adm_confirm_count = self.env['admission.confirmation'].search_count([('id', '=', self.admission_id.id)])

	def _fees_count(self):
		for record in self:
			obj = self.env['account.move'].search([('move_type', '=', 'out_invoice'),
									('partner_id.name', '=', record.name)])
			record.fees_sum = sum(obj.mapped('amount_total'))
			record.fees_count = len(obj)

	admission_inquiry_count = fields.Integer('Admission Inquiry',compute='compute_count')
	adm_confirm_count = fields.Integer('Admission Confirm',compute='compute_count')
	date = fields.Date(string="Date", readonly=True, default=datetime.today())
	inquiry_id = fields.Many2one('student.admission', string="Enquiry No")
	admission_id = fields.Many2one('admission.confirmation', string="Admission No")
	name = fields.Char('Name of the Student')
	name_initial = fields.Char(string="Initial",default = '')
	birth_date = fields.Date('Date of Birth', required=True)
	email = fields.Char(string='Email ID', readonly=True)
	aadhar_no = fields.Char(string='Aadhar No', readonly=True)
	courses_id = fields.Many2one('courses.master', string="Courses")
	quota_id = fields.Many2one('quota.master',string="Quota",required=True)
	special_quota_id = fields.Many2one('special.quota', string="Special Quota")
	accomodation_check_box = fields.Selection(string="Accommodation",
											  selection=[('dayscholar', 'Dayscholar'),
											  ('hosteler', 'Hosteler')], default='dayscholar', required=True)
	room = fields.Selection(string="Room", selection=[
		('ord', 'ORD'),
		('sr', 'SR'),
		('dlx_3', 'DLX(3)'),
		('dlx_4', 'DLX(4)'),
		('dlx_ac', 'DLX AC')])
	stages_id = fields.Many2one('stages.master', string='Stage')
	bus_root = fields.Char('Bus Root')
	institute_last_studied = fields.Many2one('last.studied.institutions', string="Institute last studied")
	name_of_the_parent_guardian = fields.Char('Name of the parent/Guardian')
	parent_guardian_occupation = fields.Char('Name of the parent/Guardian')
	education_qualification = fields.Char('Education Qualification')
	curr_collage = fields.Many2one('res.company', string="Collage Name")
	referred_by = fields.Char('Referred By')
	emergeny_contact = fields.Char('Emergeny contact')
	degree_level_id = fields.Many2one('degree.level.master', string="Degree", required=True)
	stud_entry = fields.Selection(string="Student Entry", selection=[
		('new', 'New Joinee'),
		('lateral_entry', 'Lateral Entry'),
		('re_join', 'Re Joining'),
		('college_transfer', 'College Transfer')])
	age = fields.Char('Age')

	community_id = fields.Many2one('community.master', string="Community")
	caste = fields.Char('Caste')
	fees_count = fields.Integer(string='Fees Receipt', compute='_fees_count')
	onhold_remarks = fields.Html(string="On-Hold Remarks", track_visibility='always')

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
	education_qualification_ids = fields.One2many('education.qualification', 'admission_list_id', string="Education Qualification")
	fee_details_ids = fields.One2many('fee.details', 'admission_confirmation_id', string="Fee Details")
	inspection_ids = fields.One2many('inspection.image', 'admission_list_id', string="Fee Details")
	state = fields.Selection(string='Status', selection=[('draft', 'Document Collection'),
														('partially_paid', 'Partially paid'),
														('doc_collected', 'Documents fully collected'),
														('doc_partially_collected', 'Documents partially collected'),
														('onhold', 'On-Hold'),
														('confirmed', 'Moved to college'),
														('cancelled', 'Cancelled'),
														('documents_returned','Documents Returned')],
			readonly=True, copy=False, index=True, track_visibility='always', default='draft')
	onhold_state = fields.Selection(string='Status', selection=[('draft', 'Document Collection'),
														 ('partially_paid', 'Partially paid'),
														 ('doc_collected', 'Documents fully collected'),
														 ('doc_partially_collected', 'Documents partially collected'),
														 ('onhold', 'On-Hold'),
														 ('confirmed', 'Moved to college'),
														 ('cancelled', 'Cancelled'),
														 ('documents_returned', 'Documents Returned')],
							 readonly=True, copy=False, index=True, track_visibility='always', default='draft')
	document_state = fields.Selection(string='Document Status', selection=[
														('doc_not_collected', 'Document Not collected'),
														('doc_collected', 'Documents fully collected'),
														('doc_partially_collected', 'Documents partially collected'),],
			readonly=True, copy=False, index=True, track_visibility='always', default='doc_not_collected')

	token_num = fields.Char('Token No')
	payment_state = fields.Selection(
		selection=[
			('not_paid', 'Not Paid'),
			('in_payment', 'In Payment'),
			('paid', 'Paid'),
			('partial', 'Partially Paid'),
			('reversed', 'Reversed'),
			('invoicing_legacy', 'Invoicing App Legacy'),
		], string="Payment Status", store=True, copy=False,
		tracking=True, readonly=True)
	document_templates_id = fields.Many2one('document.templates', string="Document Template")
	concession_type = fields.Selection([('general_concession','General Concession'),('special_concession','Special Concession')],string='Type')
	special_concession_type = fields.Many2one('special.concession.type',string="Special Concession Type")

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
	cancel_remark = fields.Text(string="Cancel Remarks")
	refund_count = fields.Integer(compute="get_credit_note_count",string="Refund")
	refund_sum = fields.Float(compute="get_credit_note_count",string="Refund Sum")
	fees_sum = fields.Float(compute="_fees_count",string="Fees Sum")
	refunded = fields.Boolean(string="Refunded",default=False)
	documents_returned = fields.Boolean(string="Documents Returned",default=False)
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
	grade_id = fields.Many2one('grade.master',string="Grade")
	stream_id = fields.Many2one('stream.master',string="Stream")
	batch_id = fields.Many2one('batch.courses.master',string="Batch")
	active = fields.Boolean(string="Active",default=True)

	document_mssg_subject = fields.Char(string='Subject')
	document_mssg_body = fields.Html(string='Body')

	payment_mssg_subject = fields.Char(string='Subject')
	payment_mssg_body = fields.Html(string='Body')

	relationship_ids = fields.One2many('relationship.master', 'admission_list_id', string="Relationship")
	health_info_ids = fields.One2many('health.information.master', 'admission_list_id', string="Health Information")

	student_account_no = fields.Char('Student Account number')
	student_ifsc = fields.Char('IFSC code')
	student_bank = fields.Char('Bank Name')
	student_branch = fields.Char('Branch Name')
	father_account_no = fields.Char('Father Account number')
	father_ifsc = fields.Char('IFSC code')
	father_bank = fields.Char('Bank Name')
	father_branch = fields.Char('Branch Name')

	partially_paid = fields.Boolean('Partially Paid', default=True)
	fully_paid = fields.Boolean('Fully Paid')
	is_principal_approval = fields.Boolean('Principal Approval',default=False)

	_sql_constraints = [
		('unique_admission_constraints','UNIQUE(birth_date,aadhar_no,stream_id,curr_collage,grade_id,degree_level_id,courses_id,batch_id)','Combination of Date of Birth, Aadhar No, Stream, College, Grade, Degree, Course and Batch Must be Unique!'),
	]


	@api.onchange('stream_id')
	def onchange_stream_id(self):
		self.curr_collage = False

	@api.onchange("curr_collage")
	def onchange_curr_collage(self):
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

    
	def documents_return(self):
		self.documents_returned = True
		self.state = 'documents_returned'


	# Get Related credit note count
	def get_credit_note_count(self):
		for itm in self:
			objs = self.env['account.move'].search([('admission_id','=',itm.admission_id.id),('move_type','=','out_refund'),('state','=','posted')])
			count = len(objs)
			itm.refund_sum = sum(objs.mapped('amount_total'))
			itm.refund_count = count

	def action_mark_refunded(self):
		for itm in self:
			itm.refunded = True
			itm.admission_id.refunded = True

	def action_open_credit_note(self):
		action = {
			'name':_("Refund"),
			'view_mode':'tree,form',
			'type':'ir.actions.act_window',
			'res_model':'account.move',
			'domain':[('move_type','=','out_refund'),('admission_id','=',self.admission_id.id)]
		}
		return action


	def action_documents_colelcted(self):
		if not self.state == 'confirmed':
			self.state = 'doc_collected'
		self.document_state = 'doc_collected'

	def action_documents_partially_colelcted(self):
		self.state = 'doc_partially_collected'
		self.document_state = 'doc_partially_collected'

	def action_multi_confirm_admission(self):
		for rec in self:
			if rec.state == 'draft':
				if not rec.curr_collage:
					raise UserError(_("Kindly select the Collage Name !.."))
				from datetime import datetime
				last_seq_no = self.env["student.details"].sudo().search([('company_id', '=', rec.curr_collage.id)],
																		limit=1, order='id desc')
				if last_seq_no and last_seq_no.role_no_seq:
					for vals in rec:
						current_year = datetime.now().year
						updated = last_seq_no.role_no_seq
						updated_1 = int(updated) + 1
						new_rec = last_seq_no.sudo().create({'name': rec.name,
													'enquiry_id': rec.inquiry_id.id,
													'company_id': rec.curr_collage.id,
															 'admission_id': rec.admission_id.id,
													'degree_level_id': rec.degree_level_id.id,
													'grade_id':rec.grade_id.id,
													'stream_id':rec.stream_id.id,
													'date_of_birth': rec.birth_date,
													'aadhar_no': rec.aadhar_no,
													'stud_entry': rec.stud_entry,
													'community_id': rec.community_id.id,
													'caste': rec.caste,
													'bus_root': rec.bus_root,
													'name_of_the_parent_guardian': rec.name_of_the_parent_guardian,
													'parent_guardian_occupation': rec.parent_guardian_occupation,
													'referred_by': rec.referred_by,
													'emergeny_contact': rec.emergeny_contact,
													'courses_id': rec.courses_id.id,
													'quota_id': rec.quota_id.id,
													'accomodation_check_box': rec.accomodation_check_box,
													'room': rec.room,
													'stages_id': rec.stages_id.id,
													'institute_last_studied': rec.institute_last_studied.id,
													'education_qualification': rec.education_qualification,
													'street': rec.street,
													'street2': rec.street2,
													'zip_code': rec.zip_code,
													'city': rec.city,
													'state_id': rec.state_id.id,
													'country_id': rec.country_id.id,
													'c_phone': rec.c_phone,
													'c_mobile': rec.c_mobile,
													'gender': rec.gender,
													'blood_group': rec.blood_group,
													'sslc_school': rec.sslc_school,
													'hsc_school': rec.hsc_school,
													'remarks': rec.remarks,
													'referred_name': rec.referred_name,
													'ref_designation_id': rec.ref_designation_id.id,
													'ref_college_id': rec.ref_college_id.id,
													'ref_mobile': rec.ref_mobile,
													"name_initial" : self.name_initial,
													"father_name" : self.father_name,
													"father_mobile" : self.father_mobile,
													"father_whatsapp_no" : self.father_whatsapp_no,
													"father_occupation" : self.father_occupation,
													"father_birth_place" : self.father_birth_place,
													"father_aadhar_no" : self.father_aadhar_no,
													"mother_name" : self.mother_name,
													"mother_mobile" : self.mother_mobile,
													"mother_whatsapp_no" : self.mother_whatsapp_no,
													"mother_occupation" : self.mother_occupation,
													"mother_birth_place" : self.mother_birth_place,
													"mother_aadhar_no" : self.mother_aadhar_no,
													"guardian_mobile" : self.guardian_mobile,
													"guardian_whatsapp_no" : self.guardian_whatsapp_no,
													"present_door_no" : self.present_door_no,
													"present_street" : self.present_street,
													"present_district" : self.present_district,
													"present_taluk" : self.present_taluk,
													"present_city" : self.present_city,
													"present_state" : self.present_state.id,
													"present_zip" : self.present_zip,
													"perm_door_no" : self.perm_door_no,
													"perm_street" : self.perm_street,
													"perm_district" : self.perm_district,
													"perm_taluk" : self.perm_taluk,
													"perm_city" : self.perm_city,
													"perm_state" : self.perm_state.id,
													"perm_zip" : self.perm_zip,
													"student_phone_no" : self.student_phone_no,
													"student_whatsapp" : self.student_whatsapp,
													 "student_account_no": rec.student_account_no,
													 "student_ifsc": rec.student_ifsc,
													 "student_bank": rec.student_bank,
													 "student_branch": rec.student_branch,

													 "father_account_no": rec.father_account_no,
													 "father_ifsc": rec.father_ifsc,
													 "father_bank": rec.father_bank,
													 "father_branch": rec.father_branch,
													'education_qualification_ids': [
														(6, 0, rec.education_qualification_ids.ids)],
													'health_info_ids': [
														(6, 0, rec.health_info_ids.ids)],
															 'inspection_ids': [
														(6, 0, rec.inspection_ids.ids)],
													# 'role_no': str(rec.curr_collage.admission_sequence) + "/" + str(
														#    current_year) + "/" + str(updated_1),
													'role_no_seq': str(updated_1)})
				else:
					for vals in rec:
						current_year = datetime.now().year
						new_rec = last_seq_no.sudo().create({'name': rec.name,
													'company_id': rec.curr_collage.id,
															 'admission_id': rec.admission_id.id,
													'enquiry_id': rec.inquiry_id.id,
													'date_of_birth': rec.birth_date,
													'degree_level_id': rec.degree_level_id.id,
													'grade_id':rec.grade_id.id,
													'stream_id':rec.stream_id.id,
													'aadhar_no': rec.aadhar_no,
													'stud_entry': rec.stud,
													'community_id': rec.community_id.id,
													'caste': rec.caste,
													'bus_root': rec.bus_root,
													'name_of_the_parent_guardian': rec.name_of_the_parent_guardian,
													'parent_guardian_occupation': rec.parent_guardian_occupation,
													'referred_by': rec.referred_by,
													'emergeny_contact': rec.emergeny_contact,
													'courses_id': rec.courses_id.id,
													'quota_id': rec.quota_id.id,
													'accomodation_check_box': rec.accomodation_check_box,
													'room': rec.room,
													'stages_id': rec.stages_id.id,
													'institute_last_studied': rec.institute_last_studied.id,
													'education_qualification': rec.education_qualification,
													'street': rec.street,
													'street2': rec.street2,
													'zip_code': rec.zip_code,
													'city': rec.city,
													'state_id': rec.state_id.id,
													'country_id': rec.country_id.id,
													'c_phone': rec.c_phone,
													'c_mobile': rec.c_mobile,
													'gender': rec.gender,
													'blood_group': rec.blood_group,
													'sslc_school': rec.sslc_school,
													'hsc_school': rec.hsc_school,
													'remarks': rec.remarks,
													'referred_name': rec.referred_name,
													'ref_designation_id': rec.ref_designation_id.id,
													'ref_college_id': rec.ref_college_id.id,
													'ref_mobile': rec.ref_mobile,
													"name_initial" : self.name_initial,
													"father_name" : self.father_name,
													"father_mobile" : self.father_mobile,
													"father_whatsapp_no" : self.father_whatsapp_no,
													"father_occupation" : self.father_occupation,
													"father_birth_place" : self.father_birth_place,
													"father_aadhar_no" : self.father_aadhar_no,
													"mother_name" : self.mother_name,
													"mother_mobile" : self.mother_mobile,
													"mother_whatsapp_no" : self.mother_whatsapp_no,
													"mother_occupation" : self.mother_occupation,
													"mother_birth_place" : self.mother_birth_place,
													"mother_aadhar_no" : self.mother_aadhar_no,
													"guardian_mobile" : self.guardian_mobile,
													"guardian_whatsapp_no" : self.guardian_whatsapp_no,
													"present_door_no" : self.present_door_no,
													"present_street" : self.present_street,
													"present_district" : self.present_district,
													"present_taluk" : self.present_taluk,
													"present_city" : self.present_city,
													"present_state" : self.present_state.id,
													"present_zip" : self.present_zip,
													"perm_door_no" : self.perm_door_no,
													"perm_street" : self.perm_street,
													"perm_district" : self.perm_district,
													"perm_taluk" : self.perm_taluk,
													"perm_city" : self.perm_city,
													"perm_state" : self.perm_state.id,
													"perm_zip" : self.perm_zip,
													"student_phone_no" : self.student_phone_no,
													"student_whatsapp" : self.student_whatsapp,
													 "student_account_no": rec.student_account_no,
													 "student_ifsc": rec.student_ifsc,
													 "student_bank": rec.student_bank,
													 "student_branch": rec.student_branch,

													 "father_account_no": rec.father_account_no,
													 "father_ifsc": rec.father_ifsc,
													 "father_bank": rec.father_bank,
													 "father_branch": rec.father_branch,
													'education_qualification_ids': [
														(6, 0, rec.education_qualification_ids.ids)],
													'health_info_ids': [
																 (6, 0, rec.health_info_ids.ids)],
															 'inspection_ids': [
																 (6, 0, rec.inspection_ids.ids)],
													'role_no_seq': '000001',
													# 'role_no': str(rec.curr_collage.admission_sequence) + "/" + str(
														#    current_year) + "/" + '1'
																})
				rec.state = "confirmed"

	def action_open_fees(self):
		action = {
			'name': _("Fees Receipt"),
			'view_mode': 'tree,form',
			'type': 'ir.actions.act_window',
			'res_model': 'account.move',
			'domain': [('move_type', '=', 'out_invoice'),('partner_id.name', '=', self.name)],
		}
		return action
	
	def action_onhold(self):
		form_view = self.env.ref('vg_colg.onhold_remark_view_id')
		return {
			'name': "Onhold Remarks",
			'view_mode': 'form',
			'view_type': 'form',
			'view_id': form_view.id,
			'res_model': 'onhold.remark',
			'type': 'ir.actions.act_window',
			'target': 'new',
		}

	def action_retrive(self):
		self.write({
			'state' : self.onhold_state
		})
	
	def action_cancel(self):
		form_view = self.env.ref('vg_colg.onhold_remark_view_id')
		return {
			'name': "Cancel Remarks",
			'view_mode': 'form',
			'view_type': 'form',
			'view_id': form_view.id,
			'res_model': 'onhold.remark',
			'type': 'ir.actions.act_window',
			'context': {'default_cancel':'admission_list'},
			'target': 'new',
		}
	
	def action_back_to_document_collection(self):
		self.state = 'draft'
		self.refunded = False
		self.documents_returned = False
		self.admission_id.write({'state':'admission_list'})
		self.message_post(body=_(f"Record set back to counselling state by {self.env.user.partner_id.name}!"))

	def action_confirm_admission(self):
		company_obj = self.env['res.company'].search([('principle_id','=',self.env.uid)])
		if not company_obj:
			raise UserError(_("Only principal can move the students to college."))
		if not self.state == 'confirmed':
			for admission in self:
				token_fees = self.env['token.fees'].search([('stream_id','=',admission.stream_id.id),('company_id','=',admission.curr_collage.id),('grade_id','=',admission.grade_id.id),('course_id', '=', admission.courses_id.id),
														('degree_level_id', '=', admission.degree_level_id.id),('batch_id','=',admission.batch_id.id)])
				admission_obj = admission.admission_id

				payment_total = sum(admission_obj.advance_payment_ids.filtered(lambda x:x.payment_type == 'inbound').mapped("amount"))

				token_fees_total = sum(token_fees.fees_lines.mapped('amount'))

				if payment_total < token_fees_total:
					raise ValidationError(_("Token fees is not fully paid, So can't move to college!"))

				# admission.write({
				# 	'partially_paid' : False,
				# 	'fully_paid' : True,
				# })
				if not admission.curr_collage:
					raise UserError(_("Kindly select the Collage Name !.."))
				from datetime import datetime


				relationship_data = []
				if admission.relationship_ids:
					for relationship_id in admission.relationship_ids:
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

				last_seq_no = self.env["student.details"].sudo().search([('company_id', '=', admission.curr_collage.id)], limit=1,order='id desc')
				if last_seq_no and last_seq_no.role_no_seq:
					for vals in self:
						current_year = datetime.now().year
						updated = last_seq_no.role_no_seq
						updated_1 = int(updated) + 1
					last_seq_no.sudo().create({	'name': admission.name,
												   'enquiry_id': admission.inquiry_id.id,
												   'admission_id': admission.admission_id.id,
												   'company_id': admission.curr_collage.id,
												   'degree_level_id': admission.degree_level_id.id,
												   'grade_id':admission.grade_id.id,
												   'stream_id':admission.stream_id.id,
												   'date_of_birth': admission.birth_date,
												   'email': admission.email,
												   'stud_entry': admission.stud_entry,
												   'aadhar_no': admission.aadhar_no,
												   'community_id': admission.community_id.id,
												   'caste': admission.caste,
												   'bus_root': admission.bus_root,
												   'name_of_the_parent_guardian': admission.name_of_the_parent_guardian,
												   'parent_guardian_occupation': admission.parent_guardian_occupation,
												   'referred_by': admission.referred_by,
												   'emergeny_contact': admission.emergeny_contact,
												   'courses_id': admission.courses_id.id,
												   'quota_id': admission.quota_id.id,
												   'accomodation_check_box': admission.accomodation_check_box,
												   'room': admission.room,
												   'stages_id': admission.stages_id.id,
												   'institute_last_studied': admission.institute_last_studied.id,
												   'education_qualification': admission.education_qualification,
												   'street': admission.street,
												   'street2': admission.street2,
												   'zip_code': admission.zip_code,
												   'city': admission.city,
												   'state_id': admission.state_id.id,
												   'country_id': admission.country_id.id,
												   'c_phone': admission.c_phone,
												   'c_mobile': admission.c_mobile,
												   'remarks': admission.remarks,
												   'gender': admission.gender,
												   'sslc_school': admission.sslc_school,
												   'hsc_school': admission.hsc_school,
												   'blood_group': admission.blood_group,
												   'referred_name': admission.referred_name,
												   'ref_designation_id': admission.ref_designation_id.id,
												   'ref_college_id': admission.ref_college_id.id,
												   'ref_mobile': admission.ref_mobile,
												   'batch_start_year': admission.batch_start_year,
												   'batch_id': admission.batch_id.id,
												   'duration': admission.duration,
												   'batch_ending_year': admission.batch_ending_year,
												   "name_initial" : self.name_initial,
												   "father_name" : self.father_name,
												   "father_mobile" : self.father_mobile,
												   "father_whatsapp_no" : self.father_whatsapp_no,
												   "father_occupation" : self.father_occupation,
												   "father_birth_place" : self.father_birth_place,
												   "father_aadhar_no" : self.father_aadhar_no,
												   "mother_name" : self.mother_name,
												   "mother_mobile" : self.mother_mobile,
												   "mother_whatsapp_no" : self.mother_whatsapp_no,
												   "mother_occupation" : self.mother_occupation,
												   "mother_birth_place" : self.mother_birth_place,
												   "mother_aadhar_no" : self.mother_aadhar_no,
												   "guardian_mobile" : self.guardian_mobile,
												   "guardian_whatsapp_no" : self.guardian_whatsapp_no,
												   "present_door_no" : self.present_door_no,
												   "present_street" : self.present_street,
												   "present_district" : self.present_district,
												   "present_taluk" : self.present_taluk,
												   "present_city" : self.present_city,
												   "present_state" : self.present_state.id,
												   "present_zip" : self.present_zip,
												   "perm_door_no" : self.perm_door_no,
												   "perm_street" : self.perm_street,
												   "perm_district" : self.perm_district,
												   "perm_taluk" : self.perm_taluk,
												   "perm_city" : self.perm_city,
												   "perm_state" : self.perm_state.id,
												   "perm_zip" : self.perm_zip,
												   "student_phone_no" : self.student_phone_no,
												   "student_whatsapp" : self.student_whatsapp,
												   "student_account_no": admission.student_account_no,
												   "student_ifsc": admission.student_ifsc,
												   "student_bank": admission.student_bank,
												   "student_branch": admission.student_branch,

												   "father_account_no": admission.father_account_no,
												   "father_ifsc": admission.father_ifsc,
												   "father_bank": admission.father_bank,
												   "father_branch": admission.father_branch,
												   "relationship_ids": relationship_data if relationship_data else False,
												   'education_qualification_ids': [(6, 0, admission.education_qualification_ids.ids)],
												   'health_info_ids': [
													   (6, 0, admission.health_info_ids.ids)],
												   'inspection_ids': [
													   (6, 0, admission.inspection_ids.ids)],
												   # 'role_no': str(admission.curr_collage.admission_sequence) + "/" + str(current_year) + "/" + str(updated_1),
												   'role_no_seq': str(updated_1)})
					# Send Email Alert
					if self.curr_collage and self.curr_collage.principle_id:
						ctx = {}
						ctx['today'] = date.today().strftime("%d/%m/%Y")
						mail_template = self.env.ref('vg_colg.mail_student_admission_confirmation_details_template')
						mail_template.with_context(ctx).sudo().send_mail(self.id, force_send=True, email_values={
							'email_to': self.curr_collage.principle_id.login})
				else:
					for vals in self:
						current_year = datetime.now().year
						last_seq_no.sudo().create({'name': admission.name,
																	 'company_id': admission.curr_collage.id,
																	 'admission_id': admission.admission_id.id,
																	 'enquiry_id': admission.inquiry_id.id,
																	 'date_of_birth': admission.birth_date,
																	 'degree_level_id': admission.degree_level_id.id,
																	 'grade_id':admission.grade_id.id,
																	 'stream_id':admission.stream_id.id,
																	 'aadhar_no': admission.aadhar_no,
																	 'community_id': admission.community_id.id,
																	 'caste': admission.caste,
																	 'stud_entry': admission.stud_entry,
																	 'email': admission.email,
																	 'name_of_the_parent_guardian': admission.name_of_the_parent_guardian,
																	 'parent_guardian_occupation': admission.parent_guardian_occupation,
																	 'referred_by': admission.referred_by,
																	 'emergeny_contact': admission.emergeny_contact,
																	 'courses_id': admission.courses_id.id,
																	 'quota_id': admission.quota_id.id,
																	 'bus_root': admission.bus_root,
																	 'accomodation_check_box': admission.accomodation_check_box,
																	 'room': admission.room,
																	 'stages_id': admission.stages_id.id,
																	 'institute_last_studied': admission.institute_last_studied.id,
																	 'education_qualification': admission.education_qualification,
																	 'street': admission.street,
																	 'street2': admission.street2,
																	 'zip_code': admission.zip_code,
																	 'city': admission.city,
																	 'state_id': admission.state_id.id,
																	 'country_id': admission.country_id.id,
																	 'c_phone': admission.c_phone,
																	 'c_mobile': admission.c_mobile,
																	 'gender': admission.gender,
																	 'blood_group': admission.blood_group,
																	 'remarks': admission.remarks,
																	 'sslc_school': admission.sslc_school,
																	 'hsc_school': admission.hsc_school,
																	 'referred_name': admission.referred_name,
																	 'ref_designation_id': admission.ref_designation_id.id,
																	 'ref_college_id': admission.ref_college_id.id,
																	 'ref_mobile': admission.ref_mobile,
																	 'batch_start_year': admission.batch_start_year,
																	 'batch_id': admission.batch_id.id,
																	 'duration': admission.duration,
																	 'batch_ending_year': admission.batch_ending_year,
																	 "name_initial" : self.name_initial,
																	 "father_name" : self.father_name,
																	 "father_mobile" : self.father_mobile,
																	 "father_whatsapp_no" : self.father_whatsapp_no,
																	 "father_occupation" : self.father_occupation,
																	 "father_birth_place" : self.father_birth_place,
																	 "father_aadhar_no" : self.father_aadhar_no,
																	 "mother_name" : self.mother_name,
																	 "mother_mobile" : self.mother_mobile,
																	 "mother_whatsapp_no" : self.mother_whatsapp_no,
																	 "mother_occupation" : self.mother_occupation,
																	 "mother_birth_place" : self.mother_birth_place,
																	 "mother_aadhar_no" : self.mother_aadhar_no,
																	 "guardian_mobile" : self.guardian_mobile,
																	 "guardian_whatsapp_no" : self.guardian_whatsapp_no,
																	 "present_door_no" : self.present_door_no,
																	 "present_street" : self.present_street,
																	 "present_district" : self.present_district,
																	 "present_taluk" : self.present_taluk,
																	 "present_city" : self.present_city,
																	 "present_state" : self.present_state.id,
																	 "present_zip" : self.present_zip,
																	 "perm_door_no" : self.perm_door_no,
																	 "perm_street" : self.perm_street,
																	 "perm_district" : self.perm_district,
																	 "perm_taluk" : self.perm_taluk,
																	 "perm_city" : self.perm_city,
																	 "perm_state" : self.perm_state.id,
																	 "perm_zip" : self.perm_zip,
																	 "student_phone_no" : self.student_phone_no,
																	 "student_whatsapp" : self.student_whatsapp,
																	 "student_account_no": admission.student_account_no,
																	 "student_ifsc": admission.student_ifsc,
																	 "student_bank": admission.student_bank,
																	 "student_branch": admission.student_branch,

																	 "father_account_no": admission.father_account_no,
																	 "father_ifsc": admission.father_ifsc,
																	 "father_bank": admission.father_bank,
																	 "father_branch": admission.father_branch,
																	 "relationship_ids": relationship_data if relationship_data else False,
																	 'education_qualification_ids': [(6, 0, admission.education_qualification_ids.ids)],
																	 'health_info_ids': [
																		 (6, 0, admission.health_info_ids.ids)],
																	 'inspection_ids': [
																		 (6, 0, admission.inspection_ids.ids)],
																	 'role_no_seq':'000001',
																	 # 'role_no': str(admission.curr_collage.admission_sequence) + "/" + str(current_year) + "/" + '1'
																	 })
						# Send Email Alert
						if self.curr_collage and self.curr_collage.principle_id:
							ctx = {}
							ctx['today'] = date.today().strftime("%d/%m/%Y")
							mail_template = self.env.ref('vg_colg.mail_student_admission_confirmation_details_template')
							mail_template.with_context(ctx).sudo().send_mail(self.id, force_send=True, email_values={
								'email_to': self.curr_collage.principle_id.login})
			self.state = "confirmed"

	@api.model
	def action_mail_notification(self):
		view = self.env.ref('vg_colg.view_mail_notification_wizard_form')
		document_mssg_subject = self.env['ir.config_parameter'].sudo().get_param('document_mssg_subject')
		document_mssg_body = self.env['ir.config_parameter'].sudo().get_param('document_mssg_body')

		return {
			'name': _('Mail Notification'),
			'type': 'ir.actions.act_window',
			'view_mode': 'form',
			'res_model': 'mail.notification.wizard',
			'views': [(view.id, 'form')],
			'view_id': view.id,
			'target': 'new',
			'context': {
				'default_admission_ids': self.ids,
				'default_document_mssg_subject': document_mssg_subject,
				'default_document_mssg_body': document_mssg_body,
			},
		}

	@api.model
	def action_payment_notification(self):
		view = self.env.ref('vg_colg.view_payment_notification_wizard_form')
		document_mssg_subject = self.env['ir.config_parameter'].sudo().get_param('payment_mssg_subject')
		document_mssg_body = self.env['ir.config_parameter'].sudo().get_param('payment_mssg_body')

		return {
			'name': _('Payment Notification'),
			'type': 'ir.actions.act_window',
			'view_mode': 'form',
			'res_model': 'mail.notification.wizard',
			'views': [(view.id, 'form')],
			'view_id': view.id,
			'target': 'new',
			'context': {
				'default_admission_ids': self.ids,
				'default_document_mssg_subject': document_mssg_subject,
				'default_document_mssg_body': document_mssg_body,
			},
		}

	@api.model
	def action_move_to_principal_approval(self):
		for rec in self:
			rec.is_principal_approval = True

	@api.model
	def action_multi_confirm_admissions(self):
		company_obj = self.env['res.company'].search([('principle_id','=',self.env.uid)])
		if not company_obj:
			raise UserError(_("Only principal can move the students to college."))
		if not self.state == 'confirmed':
			admission_datas = []
			sr_no = 1
			for rec in self:
				admission_dic = {
					'sr_no': sr_no,
					'name': rec.name,
					'admission_no': rec.admission_id.admission_no,
				}
				admission_datas.append(admission_dic)
				sr_no += 1
				# if rec.state == 'doc_collected':
				if not rec.curr_collage:
					raise UserError(_("Kindly select the Collage Name !.."))
				token_fees = self.env['token.fees'].search([('stream_id','=',rec.stream_id.id),('company_id','=',rec.curr_collage.id),('grade_id','=',rec.grade_id.id),('course_id', '=', rec.courses_id.id),
														('degree_level_id', '=', rec.degree_level_id.id),('batch_id','=',rec.batch_id.id)])
				admission_obj = rec.admission_id

				payment_total = sum(admission_obj.advance_payment_ids.filtered(lambda x:x.payment_type == 'inbound').mapped("amount"))

				token_fees_total = sum(token_fees.fees_lines.mapped('amount'))

				if payment_total < token_fees_total:
					raise ValidationError(_("Token fees is not fully paid, So can't move to college!"))

				from datetime import datetime
				last_seq_no = self.env["student.details"].sudo().search([('company_id', '=', self.curr_collage.id)],
																		limit=1, order='id desc')

				relationship_data = []
				if rec.relationship_ids:
					for relationship_id in rec.relationship_ids:
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

				if last_seq_no and last_seq_no.role_no_seq:
					for vals in rec:
						current_year = datetime.now().year
						updated = last_seq_no.role_no_seq
						updated_1 = int(updated) + 1
						last_seq_no.sudo().create({ 'name': rec.name,
													'enquiry_id': rec.inquiry_id.id,
													'stud_entry': rec.stud_entry,
													'aadhar_no': rec.aadhar_no,
													'company_id': rec.curr_collage.id,
													'admission_id': rec.admission_id.id,
													'date_of_birth': rec.birth_date,
													'degree_level_id': rec.degree_level_id.id,
													'grade_id':rec.grade_id.id,
													'stream_id':rec.stream_id.id,
													'age': rec.age,
													'email': rec.email,
													'community_id': rec.community_id.id,
													'caste': rec.caste,
													'bus_root': rec.bus_root,
													'name_of_the_parent_guardian': rec.name_of_the_parent_guardian,
													'parent_guardian_occupation': rec.parent_guardian_occupation,
													'referred_by': rec.referred_by,
													'emergeny_contact': rec.emergeny_contact,
													'courses_id': rec.courses_id.id,
													'quota_id': rec.quota_id.id,
													'accomodation_check_box': rec.accomodation_check_box,
													'room': rec.room,
													'stages_id': rec.stages_id.id,
													'institute_last_studied': rec.institute_last_studied.id,
													'education_qualification': rec.education_qualification,
													'street': rec.street,
													'street2': rec.street2,
													'zip_code': rec.zip_code,
													'city': rec.city,
													'state_id': rec.state_id.id,
													'country_id': rec.country_id.id,
													'c_phone': rec.c_phone,
													'c_mobile': rec.c_mobile,
													'remarks': rec.remarks,
													'referred_name': rec.referred_name,
													'ref_designation_id': rec.ref_designation_id.id,
													'ref_college_id': rec.ref_college_id.id,
													'ref_mobile': rec.ref_mobile,
													'batch_start_year': rec.batch_start_year,
													'batch_id': rec.batch_id.id,
													'duration': rec.duration,
													'batch_ending_year': rec.batch_ending_year,
													"name_initial" : rec.name_initial,
													"father_name" : rec.father_name,
													"father_mobile" : rec.father_mobile,
													"father_whatsapp_no" : rec.father_whatsapp_no,
													"father_occupation" : rec.father_occupation,
													"father_birth_place" : rec.father_birth_place,
													"father_aadhar_no" : rec.father_aadhar_no,
													"mother_name" : rec.mother_name,
													"mother_mobile" : rec.mother_mobile,
													"mother_whatsapp_no" : rec.mother_whatsapp_no,
													"mother_occupation" : rec.mother_occupation,
													"mother_birth_place" : rec.mother_birth_place,
													"mother_aadhar_no" : rec.mother_aadhar_no,
													"guardian_mobile" : rec.guardian_mobile,
													"guardian_whatsapp_no" : rec.guardian_whatsapp_no,
													"present_door_no" : rec.present_door_no,
													"present_street" : rec.present_street,
													"present_district" : rec.present_district,
													"present_taluk" : rec.present_taluk,
													"present_city" : rec.present_city,
													"present_state" : rec.present_state.id,
													"present_zip" : rec.present_zip,
													"perm_door_no" : rec.perm_door_no,
													"perm_street" : rec.perm_street,
													"perm_district" : rec.perm_district,
													"perm_taluk" : rec.perm_taluk,
													"perm_city" : rec.perm_city,
													"perm_state" : rec.perm_state.id,
													"perm_zip" : rec.perm_zip,
													"student_phone_no" : rec.student_phone_no,
													"student_whatsapp" : rec.student_whatsapp,
													"student_account_no": rec.student_account_no,
													"student_ifsc": rec.student_ifsc,
													"student_bank": rec.student_bank,
													"student_branch": rec.student_branch,

													"father_account_no": rec.father_account_no,
													"father_ifsc": rec.father_ifsc,
													"father_bank": rec.father_bank,
													"father_branch": rec.father_branch,
													"relationship_ids": relationship_data if relationship_data else False,
													'education_qualification_ids': [
														(6, 0, rec.education_qualification_ids.ids)],
													'health_info_ids': [
														(6, 0, rec.health_info_ids.ids)],
													'inspection_ids': [
														(6, 0, rec.inspection_ids.ids)],
													# 'role_no': str(rec.curr_collage.admission_sequence) + "/" + str(
														#    current_year) + "/" + str(updated_1),
													'role_no_seq': str(updated_1)})
				else:
					for vals in rec:
						current_year = datetime.now().year
						last_seq_no.sudo().create({ 'name': rec.name,
													'company_id': rec.curr_collage.id,
													'stud_entry': rec.stud_entry,
													'aadhar_no': rec.aadhar_no,
													'admission_id': rec.admission_id.id,
													'enquiry_id': rec.inquiry_id.id,
													'date_of_birth': rec.birth_date,
													'degree_level_id': rec.degree_level_id.id,
													'grade_id':rec.grade_id.id,
													'stream_id':rec.stream_id.id,
													'age': rec.age,
													'community_id': rec.community_id.id,
													'caste': rec.caste,
													'bus_root': rec.bus_root,
													'name_of_the_parent_guardian': rec.name_of_the_parent_guardian,
													'parent_guardian_occupation': rec.parent_guardian_occupation,
													'referred_by': rec.referred_by,
													'emergeny_contact': rec.emergeny_contact,
													'courses_id': rec.courses_id.id,
													'quota_id': rec.quota_id.id,
													'accomodation_check_box': rec.accomodation_check_box,
													'room': rec.room,
													'stages_id': rec.stages_id.id,
													'institute_last_studied': rec.institute_last_studied.id,
													'education_qualification': rec.education_qualification,
													'street': rec.street,
													'street2': rec.street2,
													'zip_code': rec.zip_code,
													'city': rec.city,
													'state_id': rec.state_id.id,
													'country_id': rec.country_id.id,
													'c_phone': rec.c_phone,
													'c_mobile': rec.c_mobile,
													'remarks': rec.remarks,
													'referred_name': rec.referred_name,
													'ref_designation_id': rec.ref_designation_id.id,
													'ref_college_id': rec.ref_college_id.id,
													'ref_mobile': rec.ref_mobile,
													'batch_start_year': rec.batch_start_year,
													'batch_id': rec.batch_id.id,
													'duration': rec.duration,
													'batch_ending_year': rec.batch_ending_year,
													"name_initial" : rec.name_initial,
													"father_name" : rec.father_name,
													"father_mobile" : rec.father_mobile,
													"father_whatsapp_no" : rec.father_whatsapp_no,
													"father_occupation" : rec.father_occupation,
													"father_birth_place" : rec.father_birth_place,
													"father_aadhar_no" : rec.father_aadhar_no,
													"mother_name" : rec.mother_name,
													"mother_mobile" : rec.mother_mobile,
													"mother_whatsapp_no" : rec.mother_whatsapp_no,
													"mother_occupation" : rec.mother_occupation,
													"mother_birth_place" : rec.mother_birth_place,
													"mother_aadhar_no" : rec.mother_aadhar_no,
													"guardian_mobile" : rec.guardian_mobile,
													"guardian_whatsapp_no" : rec.guardian_whatsapp_no,
													"present_door_no" : rec.present_door_no,
													"present_street" : rec.present_street,
													"present_district" : rec.present_district,
													"present_taluk" : rec.present_taluk,
													"present_city" : rec.present_city,
													"present_state" : rec.present_state.id,
													"present_zip" : rec.present_zip,
													"perm_door_no" : rec.perm_door_no,
													"perm_street" : rec.perm_street,
													"perm_district" : rec.perm_district,
													"perm_taluk" : rec.perm_taluk,
													"perm_city" : rec.perm_city,
													"perm_state" : rec.perm_state.id,
													"perm_zip" : rec.perm_zip,
													"student_phone_no" : rec.student_phone_no,
													"student_whatsapp" : rec.student_whatsapp,
													"student_account_no": rec.student_account_no,
													"student_ifsc": rec.student_ifsc,
													"student_bank": rec.student_bank,
													"student_branch": rec.student_branch,
													"father_account_no": rec.father_account_no,
													"father_ifsc": rec.father_ifsc,
													"father_bank": rec.father_bank,
													"father_branch": rec.father_branch,
													"relationship_ids": relationship_data if relationship_data else False,
													'education_qualification_ids': [
														(6, 0, rec.education_qualification_ids.ids)],
													'health_info_ids': [
														(6, 0, rec.health_info_ids.ids)],
													'inspection_ids': [
														(6, 0, rec.inspection_ids.ids)],
													'role_no_seq': '000001',
													# 'role_no': str(rec.curr_collage.admission_sequence) + "/" + str(
														#    current_year) + "/" + '1'
													})
				rec.state = "confirmed"
			if admission_datas:
				# Send Email Alert
				if self[0].curr_collage and self[0].curr_collage.principle_id:
					ctx = {}
					ctx['today'] = date.today().strftime("%d/%m/%Y")
					ctx['admission_datas'] = admission_datas
					mail_template = self.env.ref('vg_colg.mail_student_admission_confirmation_details_multi_template')
					mail_template.with_context(ctx).sudo().send_mail(self[0].id, force_send=True, email_values={
						'email_to': self[0].curr_collage.principle_id.login})

	def get_inquiry(self):
		"""Inquiry smart button"""
		self.ensure_one()
		return {
			'type': 'ir.actions.act_window',
			'name': 'Student Inquiry',
			'view_mode': 'tree,form',
			'res_model': 'student.admission',
			'domain': [('id', '=', self.inquiry_id.id)],
			'context': "{'create': False}"
		}

	def get_admission(self):
		"""Admission smart button"""
		self.ensure_one()
		return {
			'type': 'ir.actions.act_window',
			'name': 'Student Inquiry',
			'view_mode': 'tree,form',
			'res_model': 'admission.confirmation',
			'domain': [('id', '=', self.admission_id.id)],
			'context': "{'create': False}"
		}

	def send_mail_document_verification(self):
		"""Send mail for the document verification """
		admission_sutdunt = self.env['inspection.image'].search([('verified','=', False), ('is_mandatory', '=', True)])
		for stduent in admission_sutdunt.mapped('admission_list_id'):
			template_id = self.env.ref('vg_colg.mail_template_student_mandatory_documents')
			if template_id:
				template_id.send_mail(stduent.id)

	@api.onchange('document_templates_id')
	def _onchange_document_templates(self):
		"""Set Document Templates"""
		for document in self:
			self.inspection_ids= [(5,0,0)]
			template_list = []
			for template in document.document_templates_id.template_ids:
				template_list.append((0, 0, {
					'name': template.name,
					'is_mandatory': template.is_mandatory
				}))
			self.write({'inspection_ids': template_list})

