import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
import json


class FeesManagement(models.Model):
	_name = 'fees.management'
	_description = 'Fees Management'
	_order = 'id desc'
	_inherit = ['mail.thread']
	_rec_name = 'company_id'


	stream_id = fields.Many2one('stream.master',string="Stream", track_visibility="always",copy=False)
	course_ids = fields.Many2many('courses.master', string="Course Name", track_visibility='always',copy=False)
	degree_ids = fields.Many2many('degree.master', string="Degree Name", track_visibility='always',copy=False)
	grade_id = fields.Many2one('grade.master', string="Grade Name",readonly=False,copy=False)
	degree_level_id = fields.Many2one('degree.level.master', string="Degree",copy=False)
	fees_for_id = fields.Many2one('fees.for', string="Fees for", domain=[('state', '=', 'approved')], track_visibility='always',copy=False)
	payment_term_id = fields.Many2one('account.payment.term', string="Payment Term",copy=False)
	academice_year_from = fields.Date(string="Academic year",copy=False)
	academice_year_to = fields.Date(string="Academic year",copy=False)
	fees_ids = fields.One2many('fees.details', 'fees_id', string='Fees Details',copy=True)
	state = fields.Selection(string='State', selection=[('draft', 'Draft'),('waiting_for_approval', 'Waiting for Approval'),
							('approved', 'Approved'), ('rejected','Rejected')],readonly=False, 
							copy=False, index=True, track_visibility='always', default='draft')
	rejected_remarks = fields.Text(string='Rejected Remarks', track_visibility='always', readonly=False,copy=False)
	notes = fields.Text(string='Notes', track_visibility='always',copy=False)
	type = fields.Selection(string='Type', selection=[('autonomous', 'Autonomous'),
							('non_autonomous', 'Non Autonomous')], track_visibility='always',copy=False)
	quota_id = fields.Many2one('quota.master',string='Quota', track_visibility='always',copy=False)
	batch_id = fields.Many2one('batch.courses.master',string='Batch', track_visibility='always',copy=False)
	company_id = fields.Many2one('res.company', 'College Name', readonly=True, index=True,copy=False)
	course_year = fields.Integer(string="Course year",copy=False)
	invoice_ids = fields.One2many('account.move','fees_id',string="Collections")


	# Helper method will duplicate fees details lines for same record
	def duplicate_fees_details_lines(self):
		for itm in self.fees_ids:
			new_line = itm.copy()
			new_line.fees_id = self.id


	# Check Uniqueness of Fees Details
	def _check_uniqueness(self, vals):
        # Prepare the filter condition for the uniqueness check
		filter_condition = [
			('id','!=',self.id),
			('stream_id', '=', self.stream_id.id),
			('company_id', '=', self.company_id.id),
            ('grade_id', '=', self.grade_id.id),
            ('degree_level_id', '=', self.degree_level_id.id),
            ('quota_id', '=', self.quota_id.id),
            ('batch_id', '=', self.batch_id.id),
	    	('course_year','=',self.course_year),
        ]

		# If there are course_ids in the values, include them in the filter condition
		filter_condition.append(('course_ids', 'in', self.course_ids.ids))

		# Search for existing records that match the filter condition
		existing_records = self.search(filter_condition)
		if existing_records:
			raise ValidationError('Combination of Stream, Company, Grade, Degree, Course, Batch, Course Year and Quota is already exist!')


	@api.model
	def create(self, vals):
		# Check uniqueness before creating the record
		res = super(FeesManagement, self).create(vals)
		res._check_uniqueness(vals)
		return res

	def write(self, vals):
		# Check uniqueness before updating the record
		res = super(FeesManagement, self).write(vals)
		self._check_uniqueness(vals)
		return res


	@api.onchange('stream_id')
	def onchange_stream_id(self):
		if self.stream_id:
			self.company_id = False
		return {
				'domain':{
						'company_id':
						[('stream_ids','in',self.stream_id.id)]
					}
				}
	
	@api.onchange('company_id','stream_id')
	def onchange_company_id(self):
		domain = []
		if self.company_id:
			domain.append(('id','in',self.company_id.grade_ids.ids))

		if self.company_id:
			domain.append(('id','in',self.company_id.grade_ids.ids))

		if self.stream_id:
			domain.append(('stream_ids','in',self.stream_id.ids))
        
		if domain:
			self.grade_id = False

			return {
				'domain':{
					'grade_id':domain
				}
			}
	
	@api.onchange('grade_id')
	def onchange_grade_id(self):
		if self.grade_id:
			self.degree_ids = False
		return {
			'domain':{
				'degree_ids':
				[('grade_id','=',self.grade_id.id)]
			}
		}
	
	@api.onchange('stream_id','grade_id')
	def domain_for_degree_level(self):
		self.degree_level_id = False
		domain = []

		if self.stream_id:
			domain.append(('stream_id','=',self.stream_id.id))
		if self.grade_id:
			domain.append(('grade_id','=',self.grade_id.id))

		if domain:
			self.degree_level_id = False
			return {'domain':{
						'degree_level_id':domain
						}
			}
		

	@api.onchange('stream_id','company_id','grade_id','degree_level_id','batch_id')
	def domain_for_degree_course(self):
		domain = []
		if self.stream_id:
			domain.append(('stream_id','=',self.stream_id.id))
		if self.grade_id:
			domain.append(('grade_id','=',self.grade_id.id))
		if self.company_id:
			courses_college_objs = self.env['courses.college.master'].search([('company_id','=',self.company_id.id)])
			course_ids = []
			for itm in courses_college_objs:
				course_ids.append(itm.courses_ids.ids)

			domain.append(('degree_id','in',(course_ids[0] if course_ids else [])))
		if self.batch_id:
			domain.append(('batch_id','=',self.batch_id.id))

		if domain:
			self.course_ids = False
			return {'domain':{
						'course_ids':domain
						}
			}
		

	def button_reject(self):
		form_view = self.env.ref('fees_management.reject_remark_view_id')
		return {
			'name': "Reject Remarks",
			'view_mode': 'form',
			'view_type': 'form',
			'view_id': form_view.id,
			'res_model': 'reject.remark',
			'type': 'ir.actions.act_window',
			'target': 'new',
		}

	@api.onchange('course_ids')
	def _onchange_cource_ids(self):
		if self.course_ids:
			self.grade_id = self.course_ids[0].grade_id.id
			self.type = self.company_id.type
		

	def action_send_approval(self):
		fees_object = self.env["fees.management"].search([('company_id', '=', self.company_id.id),
														('fees_for_id', '=', self.fees_for_id.id),
														('course_ids', 'in', self.course_ids.ids),
														('degree_ids', 'in', self.degree_ids.ids),
														('academice_year_from', '=', self.academice_year_from),
														('academice_year_to', '=', self.academice_year_to),
														('quota_id', '=', self.quota_id.id),
														('id', '!=', self.id),
														])
		if fees_object:
			raise UserError(_("Fees is already created for this category !.."))
		self.state = 'waiting_for_approval'

	def action_approved(self):
		self.state = 'approved'

	# Creating Fees Collections
	def create_fee_invoice(self,fee,student_ids,grouped_data):
		existing_student = []
		new_moves = []
		for student_obj in student_ids:
			move_obj = self.env['account.move']
			fee_obj = self
			partner_id = self.env['res.partner'].search([('aadhar_no','=',student_obj.aadhar_no)],limit=1)
			journal = self.env['account.journal'].search([('company_id', '=', self.env.company.id),('type', '=', 'sale')],limit=1)
			for key,value in grouped_data.items():
				if self.env.context.get('solo_invoice'):
					if_exist = self.env['account.move'].search([('fees_id','=',fee.id),
															('fees_line_id','=',value[0].id),
															('partner_id','=',partner_id.id),
															('degree_level_id','=',student_obj.degree_level_id.id),
															('course_id','=',student_obj.courses_id.id),
															('semester_id','=', key[0].id),
															('term','=',value[0].terms),
															('details_id','=',student_obj.role_no), 
															('fees_for_id','=',value[0].fees_for_id.id),
															('is_true','=',True),
															('state','!=','cancel')]) 
				else:
					if_exist = self.env['account.move'].search([('fees_id','=',fee.id),
															('partner_id','=',partner_id.id),
															('degree_level_id','=',student_obj.degree_level_id.id),
															('course_id','=',student_obj.courses_id.id),
															('semester_id','=', key[0].id),
															('term','=',value[0].terms),
															('details_id','=',student_obj.role_no), 
															('fees_for_id','=',value[0].fees_for_id.id),
															('is_true','=',True),
															('state','!=','cancel')])
				if if_exist.ids:
					for i in if_exist:
						existing_student.append(i.details_id.role_no)
				else:
					fee_lines = []
					inv_lines = []
					tmp_line = False
					for i in value:
						if i.product_id.hostel_ok:
							if student_obj and student_obj.accomodation_check_box == 'hosteler' and ((student_obj.room_type_id and student_obj.room_type_id.product_id.id == i.product_id.id) or i.is_common) and not i.day_scholar_common:
								fee_val = {
									'product_id': i.product_id.id,
									'priority': i.priority,
									'terms': i.terms,
									'amount': i.amount,
									'unpaid': i.amount
								}

								inv_val = {
									'student_id': student_obj.id,
									'product_id': i.product_id.id,
									'priority': i.priority,
									'course_id':student_obj.courses_id.id,
									'fees_for_id': i.fees_for_id.id,
									'start_date': i.start_date,
									'end_date': i.end_date,
									'due_date': i.due_date,
									'price_unit': i.amount,
									'course_year': fee_obj.course_year,
									'tax_ids': [(6, 0, i.product_id.taxes_id.ids)],
								}

							else:
								fee_val = {}
								inv_val = {}
						else:
							if student_obj and student_obj.accomodation_check_box == 'hosteler' and i.day_scholar_common:
								fee_val = {}
								inv_val = {}
							else:
								fee_val = {
									'product_id': i.product_id.id,
									'priority': i.priority,
									'terms': i.terms,
									'amount': i.amount,
									'unpaid': i.amount
								}

								inv_val = {
									'student_id': student_obj.id,
									'product_id': i.product_id.id,
									'priority': i.priority,
									'course_id':student_obj.courses_id.id,
									'fees_for_id': i.fees_for_id.id,
									'start_date': i.start_date,
									'end_date': i.end_date,
									'due_date': i.due_date,
									'price_unit': i.amount,
									'course_year': fee_obj.course_year,
									'tax_ids': [(6, 0, i.product_id.taxes_id.ids)],
								}

						if fee_val:
							fee_lines.append((0, 0,fee_val))
						
						tmp_line = i

						if i.product_id.id and inv_val:
							inv_lines.append((0, 0,inv_val))
					if inv_lines:
						inv_vals = {
							'fees_id':fee.id,
							'fees_line_id': value[0].id if self.env.context.get('solo_invoice') else False,
							'details_id':student_obj.id,
							'partner_id':partner_id.id,
							'is_true':True,
							'journal_id': journal.id,
							'invoice_date': datetime.now().date(),
							'date': datetime.now().date(),
							'fees_for_id': tmp_line.fees_for_id.id,
							'term': tmp_line.terms,
							'semester_id': key[0].id,
							'batch_id': fee_obj.batch_id.id,
							'move_type':'out_invoice',
							'course_year':fee_obj.course_year,
							'fee_manage_id':fee_obj.id,
							'degree_level_id':student_obj.degree_level_id.id,
							'course_id':student_obj.courses_id.id,
							'payment_state':'not_paid',
							'state':'draft',
							'fee_line_ids': fee_lines,
							'invoice_line_ids': inv_lines,
						}
						move_obj += self.env['account.move'].sudo().create(inv_vals)
						new_moves.append(move_obj)
		else:
			if not self.env.context.get('solo_invoice') and not new_moves:
				raise ValidationError(_("There is nothing in pending to create a invoice!"))
			if self.env.context.get('solo_invoice') and not new_moves:
				return True

	# Button: (Generate Invoice)
	def generate_invoice(self):
		fees_objs = self.filtered(lambda x: x.quota_id.bulk_create and x.state == 'approved')
		line_fees_objs = self.filtered(lambda x: not x.quota_id.bulk_create and x.state == 'approved')
		msg = ''
		for fee in fees_objs:
			student_details_obj = self.env['student.details'].search([('stream_id','=',fee.stream_id.id),
							     									  ('company_id','=',fee.company_id.id),
																	  ('grade_id','=',fee.grade_id.id),
																	  ('degree_level_id','=',fee.degree_level_id.id),
							     									  ('courses_id','in',fee.course_ids.ids),
																	  ('quota_id','=',fee.quota_id.id),
																	  ('batch_id','=',fee.batch_id.id)])

			grouped_data = {}
        	# Group the records by 'semaster' ID and 'term'
			for record in fee.fees_ids:
				key = (record.semester_id, record.fees_for_id.id)
				if key not in grouped_data:
					grouped_data[key] = []
				grouped_data[key].append(record)
			msg = fee.create_fee_invoice(fee,student_details_obj,grouped_data)
		is_existing = []
		for fee in line_fees_objs:
			student_details_obj = self.env['student.details'].search([('stream_id','=',fee.stream_id.id),
							     									  ('company_id','=',fee.company_id.id),
																	  ('grade_id','=',fee.grade_id.id),
																	  ('degree_level_id','=',fee.degree_level_id.id),
							     									  ('courses_id','in',fee.course_ids.ids),
																	  ('quota_id','=',fee.quota_id.id),
																	  ('batch_id','=',fee.batch_id.id)])

			grouped_data = {}

        	# Group the records by 'semaster' ID and 'term'
			for record in fee.fees_ids:
				key = (record.semester_id, record.fees_for_id.id)
				grouped_data[key] = [record]
				tmp_bool = fee.with_context(solo_invoice=True).create_fee_invoice(fee,student_details_obj,grouped_data)
				is_existing.append(tmp_bool)
		else:
			if is_existing and all(is_existing):
				raise ValidationError(_("There is Nothing in pending to create a fees collection!"))
			else:
				self.message_post(body=_("Fees collections created successfully!"))
		return msg
	

class FeesDetails(models.Model):
	_name = 'fees.details'


	name = fields.Char(related="product_id.name",string="Name")
	product_id = fields.Many2one('product.product',string="Fees Heads",required=True)
	amount = fields.Monetary(string="Amount", currency_field='currency_id')
	currency_id = fields.Many2one('res.currency', string='Currency')
	fees_id = fields.Many2one('fees.management', string="Fees Details")
	semester_id = fields.Many2one('semester.master', string="Semester")
	start_date = fields.Date(string="Start Date")
	end_date = fields.Date(string="End Date")
	due_date = fields.Date(string="Due Date")
	is_hostel = fields.Boolean(related="product_id.hostel_ok",string="Is Hostel?")
	is_common = fields.Boolean(string="Is Common")
	terms = fields.Integer(string="Terms")
	attachment_binary = fields.Binary(string='Document')
	fees_for_id = fields.Many2one('fees.for', string="Fees for", domain=[('state', '=', 'approved')], track_visibility='always')
	domain_filter = fields.Char(string="Domain Filter",compute="compute_domain")
	day_scholar_common = fields.Boolean(string="Dayscholar Common",help="Selected lines will not come into hosteler collection!")

	@api.onchange('semester_id')
	def compute_domain(self):
		for itm in self:
			term_ids = []
			list_domain = [('company_id','=',itm.fees_id.company_id.id),
								('stream_id','=',itm.fees_id.stream_id.id),
								('grade_id','=',itm.fees_id.grade_id.id),
								('degree_level_id','=',itm.fees_id.degree_level_id.id),
								('course_ids','in',itm.fees_id.course_ids.ids),
								('quota_id','=',itm.fees_id.quota_id.id),
								('batch_id','=',itm.fees_id.batch_id.id)]
			if itm.fees_id.id:
				list_domain.append(('id','!=',itm.fees_id.id))

			if itm.fees_id._origin:
				list_domain.append(('id','!=',itm.fees_id._origin.id))
			
			fees_objs = self.fees_id.search(list_domain)

			for fee in fees_objs:
				term_objs = fee.fees_ids.mapped('fees_for_id')

				for term in term_objs:
					if term.id not in term_ids:
						term_ids.append(term.id)
		
			domain = [('id', 'not in', term_ids)] if term_ids else []
			itm.domain_filter = json.dumps(domain)
	
	def term_date_validation(self):
		if self.start_date and self.end_date and self.start_date > self.end_date:
			raise ValidationError(_("Term Start Date should be greater than End Date!"))
		
	@api.onchange("is_common")
	def onchange_is_common(self):
		if self.is_common and not self.is_hostel:
			raise ValidationError(_("Is Common field can be True for only Is Hostel Lines!"))

	# @api.onchange('payment_type')
	# def _onchange_payment_type(self):
	# 	if self.payment_type:
	# 		self.terms = '1'
	# 	else:
	# 		self.terms = '0'


	# @api.onchange('due_date')
	# def _onchange_due_date(self):
	# 	if self.end_date and self.start_date and self.due_date and self.start_date > self.due_date and self.end_date < self.due_date and datetime.now().date() > self.due_date:
	# 		raise ValidationError(_("Selected due date must be greater than Today!"))
