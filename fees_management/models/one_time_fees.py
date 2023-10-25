from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class OneTimeFees(models.Model):
	_name = 'one.time.fees'
	_description = 'One Time Fees'
	_order = 'id desc'
	_inherit = ['mail.thread']


	name = fields.Many2one('one.time.fees.category', string='Fees Name', track_visibility='always')
	stream_id = fields.Many2one('stream.master',string="Stream",track_visibility='always')
	created_date = fields.Date(string="Created Date", readonly=True, default=datetime.today())
	course_ids = fields.Many2many('courses.master', string="Course Name", track_visibility='always')
	degree_ids = fields.Many2many('degree.master', string="Degree Name", track_visibility='always')	
	degree_level_id = fields.Many2one('degree.level.master', string="Degree")
	college_id = fields.Many2one('res.company', 'College Name', readonly=False, 
								index=True, default=lambda self: self.env.company)
	grade_id = fields.Many2one('grade.master', string="Grade Name",readonly=False)
	academice_year_from = fields.Date(string="Academic year",required=False, track_visibility='always')
	academice_year_to = fields.Date(string="Academic year",required=False, track_visibility='always')
	notes = fields.Text(string='Notes', track_visibility='always')
	fees_ids = fields.One2many('one.time.fees.line','fees_id', string='Fees Details')
	section_id = fields.Many2one('section.master',string='Section', track_visibility='always')
	course_year = fields.Char(string='Course year', required=True, track_visibility='always')
	due_date = fields.Date(string="Due Date",required=True, track_visibility='always')
	quota = fields.Selection(string='Quota', selection=[('general', 'General Quota'),
							('management', 'Management Quota')], track_visibility='always')
	quota_id = fields.Many2one('quota.master',string='Quota', track_visibility='always')
	batch_id = fields.Many2one('batch.courses.master',string='Batch', track_visibility='always')
	semester_id = fields.Many2one('semester.master',string="Semester",required=True)
	term_id = fields.Many2one('fees.for',string="Term",required=True)
	state = fields.Selection(string='State', selection=[('draft', 'Draft'),
							('confirmed', 'Confirmed'),('invoiced', 'Invoiced')],required=True,default='draft',track_visibility='always')
	generated_number = fields.Integer(compute='compute_number')
	invoice_generated_number = fields.Integer(compute='compute_invoice_number')
	details_id = fields.Many2one('student.details',string='Roll Number')
	last_payment = fields.Boolean(string='Last Payment',default=False)

	@api.onchange('details_id')
	def changing_student_number(self):
		if self.details_id:
			# self.write({'
			self.grade_id=self.details_id.grade_id.id
			self.college_id=self.details_id.company_id.id
			self.degree_level_id=self.details_id.degree_level_id.id
			self.quota_id=self.details_id.quota_id.id
			self.batch_id=self.details_id.batch_id.id
			self.write({'course_ids': [(5, 0, 0)]})
		if not self.details_id:
			self.grade_id=''
			self.college_id=''
			self.degree_level_id=''
			self.quota_id=''
			self.batch_id=''
	

	def compute_number(self):
		for res in self:
			obj = self.env['student.onetime.fees'].search([('onetimefees_id','=',res.id)])
			res.generated_number = len(obj)
	
	def compute_invoice_number(self):
		for res in self:
			obj = self.env['account.move'].search([('one_time_fee_id','=',res.id)])
			res.invoice_generated_number = len(obj)


	@api.onchange('semester_id')
	def onchange_semester_id(self):
		return {
			'domain':{'term_id':[('id','in',self.semester_id.term_ids.ids)]}
		}
	
	@api.onchange('stream_id')
	def onchange_stream_id(self):
		if self.stream_id:
			self.college_id = False
		return {
				'domain':{
						'college_id':
						[('stream_ids','in',self.stream_id.id)]
					}
				}
	
	@api.onchange('college_id','stream_id')
	def onchange_college_id(self):
		domain = []
		if self.college_id:
			domain.append(('id','in',self.college_id.grade_ids.ids))

		if self.college_id:
			domain.append(('id','in',self.college_id.grade_ids.ids))

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
		

	@api.onchange('stream_id','college_id','grade_id','degree_level_id','batch_id')
	def domain_for_degree_course(self):
		domain = []
		if self.stream_id:
			domain.append(('stream_id','=',self.stream_id.id))
		if self.grade_id:
			domain.append(('grade_id','=',self.grade_id.id))
		if self.college_id:
			courses_college_objs = self.env['courses.college.master'].search([('company_id','=',self.college_id.id)])
			course_ids = []
			for itm in courses_college_objs:
				course_ids.append(itm.courses_ids.ids)

			domain.append(('degree_id','in',(course_ids[0] if course_ids else [])))

		if self.batch_id:
			domain.append(('batch_id','=',self.batch_id.id))

		if domain:
			self.degree_ids = False
			return {'domain':{
						'course_ids':domain
						}
			}
		
	# @api.onchange('course_ids')
	# def _onchange_cource_ids(self):
	# 	if self.course_ids:
	# 		self.grade_id = self.course_ids[0].grade_id.id
	# 		# self.type = self.college_id.type
		
	# 		return {
	# 				'domain':{
	# 					'batch_id':[('courses_id','in',self.course_ids.ids)]
	# 					}
	# 				}


	def action_open_student_onefees(self):
		action = {
			'type': 'ir.actions.act_window',
			'name': 'Student One Time Fees Details',  	
			'res_model': 'student.onetime.fees', 
			'view_mode': 'tree', 
			'views': [(self.env.ref('fees_management.student_onetime_fees_tree_view').id, 'tree')],
			'target': 'current',  
			'domain': [('onetimefees_id','=',self.id)]
		}
		return action
	
	def action_open_student_onefees_invoice(self):
		action = {
			'type': 'ir.actions.act_window',
			'name': 'One Time Fees Invoice',  
			'res_model': 'account.move', 
			'view_mode': 'tree,form', 
			'views': [(self.env.ref('account_extend.fee_account_move_tree_view').id, 'tree'),(False,'form')],
			'target': 'current',  
			'domain': [('one_time_fee_id','=',self.id)]
		}
		return action
	
	def generate_student_onetime_fee(self):
		if not self.fees_ids:
			raise UserError(_("Please select a Fee before generating the student's details!!"))
		amnt = 0.00
		for i in self.fees_ids:
			amnt +=float(i.amount)
		if amnt == 0:
			raise UserError(_("The Fees Amount should be greater than zero!!"))
		if self.details_id:
			vals = {
				'student_id':self.details_id.id,
				'onetimefees_id':self.id,
				'course_id':self.details_id.courses_id.id,
				'degree_level_id':self.degree_level_id.id,
				'college_id':self.college_id.id,
				'currency_id':self.env.company.currency_id.id,
				'amount':float(amnt)
				}
			self.env['student.onetime.fees'].create(vals)
			self.write({'state':'confirmed'})
			return True
		quota = self.quota_id.id if self.quota_id else False

		search_param = []
		if self.quota_id:
			search_param.append(('quota_id','=',quota))
		if self.college_id:
			search_param.append(('company_id','=',self.college_id.id))
		if self.course_ids:			
			search_param.append(('courses_id','in',self.course_ids.ids))
		if self.batch_id:			
			search_param.append(('batch_id','=',self.batch_id.id))
		if self.section_id:			
			search_param.append(('section_id','=',self.section_id.id))
		
		if not search_param:
			raise UserError(_("Please select any one of the following: Quota,College,Course,Batch,Section"))
		student_details_obj = self.env['student.details'].search(search_param)

		if not student_details_obj:
			raise UserError(_("No Students matching this criteria"))
		
		for obj in student_details_obj:
			vals = {
				'student_id':obj.id,
				'onetimefees_id':self.id,
				'course_id':obj.courses_id.id,
				'degree_level_id':self.degree_level_id.id,
				'college_id':self.college_id.id,
				'currency_id':self.env.company.currency_id.id,
				'amount':float(amnt)
				}
			self.env['student.onetime.fees'].create(vals)
		self.write({'state':'confirmed'})
		return True

	
	def confirm_generate_onetime_invoice(self):
		return {
            'name': _('Warning'),
            'res_model': 'validate.one.time.fees',
            'view_mode': 'form',
            'context': {
                'active_model': 'one.time.fees',
                'active_ids': self.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

	def generate_onetime_invoice(self):
		student_fees_ids = self.env['student.onetime.fees'].search([('onetimefees_id','=',self.id),('invoice_created','=',False)])
		for obj in student_fees_ids:
			move_obj = self.env['account.move']
			partner_id = self.env['res.partner'].search([('aadhar_no','=',obj.student_id.aadhar_no)],limit=1)
			if not partner_id:
				raise UserError(_("Unable to find Partner for the Student %s" % (obj.student_id.role_no)))
			journal = self.env['account.journal'].search([('company_id', '=', self.env.company.id),('type', '=', 'sale')],limit=1)
			inv_lines = []
			fee_lines = []
			for line in self.fees_ids:
				fee_val = {
					'product_id': line.product_id.id,
					'payment_type': '',
					'priority': 0,
					'terms': 0,
					'amount': line.amount,
					'unpaid': line.amount
				}
				fee_lines.append((0, 0,fee_val))
				inv_val = {
					'student_id': obj.student_id.id,
					'product_id': line.product_id.id,
					'course_id':obj.student_id.courses_id.id,
					'semester_id':self.semester_id.id if self.semester_id else False,
					'fees_for_id': self.term_id.id if self.term_id else False,
					'start_date': self.academice_year_from,
					'end_date': self.academice_year_to,
					'due_date': self.due_date,
					'price_unit': line.amount,
					'course_year': self.course_year,
					'tax_ids': [(6, 0, line.product_id.taxes_id.ids)],
				}
				if line.product_id.id:
					inv_lines.append((0, 0,inv_val))

			inv_vals = {
					'details_id':obj.student_id.id,
					'partner_id':partner_id.id,
					'is_true':True,
					'journal_id': journal.id,
					'invoice_date': datetime.now().date(),
					'date': datetime.now().date(),
					# 'payment_type': '',
					'fees_for_id': self.term_id.id if self.term_id else False,
					'term': 0,
					'last_payment':self.last_payment,
					'semester_id':self.semester_id.id if self.semester_id else False,
					'batch_id': self.batch_id.id,
					'move_type':'out_invoice',
					'course_year':self.course_year,
					'one_time_fee_id':self.id,
					'fee_manage_id':'',
					'degree_level_id':obj.student_id.degree_level_id.id,
					'course_id':obj.student_id.courses_id.id,
					'payment_state':'not_paid',
					'state':'draft',
					'fee_line_ids': fee_lines,
					'invoice_line_ids': inv_lines,
				}
			move_obj += self.env['account.move'].sudo().create(inv_vals)
			obj.invoice_created = True
		self.write({'state':'invoiced'})
		return {
			'warning':{
				'title':'Fees Generated Successfully!',
				'message': "Fees was generated Successfully!"
				}
			}

class FeesDetails(models.Model):
	_name = 'one.time.fees.line'


	name = fields.Char(related="product_id.name",string="Name")
	fees_id = fields.Many2one('one.time.fees', string="One Fees Details")
	product_id = fields.Many2one('product.product',string="Description",required=True)
	amount = fields.Monetary(string="Amount", currency_field='currency_id')
	currency_id = fields.Many2one('res.currency', string='Currency')



class ValidateONeTimeFees(models.TransientModel):
	_name = "validate.one.time.fees"

	def confim_one_time_fees(self):
		one_obj = self.env['one.time.fees'].search([('id','in',self._context.get('active_ids', []))])
		if one_obj:
			for rec in one_obj:
				rec.generate_onetime_invoice()
		return True