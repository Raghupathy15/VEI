from odoo import fields, models, api, _


class TokenFees(models.Model):
	_name = 'token.fees'
	_description = 'Token Fees'
	_inherit = ['mail.thread']
	_rec_name = "course_id"


	stream_id = fields.Many2one('stream.master',string="Stream", required=True)
	company_id = fields.Many2one('res.company',string="College", required=True)
	grade_id = fields.Many2one('grade.master',string="Grade", required=True)
	degree_level_id = fields.Many2one('degree.level.master', string="Degree", required=True)
	course_id = fields.Many2one('courses.master', string="Course Name", required=True)
	batch_id = fields.Many2one('batch.courses.master',string="Batch")
	# fees = fields.Integer(string="Fees")
	notes = fields.Text(string="Internal Notes")
	quota_id = fields.Many2one("quota.master",string="Quota", track_visibility='always',required=True)
	academice_year_from = fields.Date(string="Academic year",required=True, track_visibility='always')
	academice_year_to = fields.Date(string="Academic year",required=True, track_visibility='always')
	fees_lines = fields.One2many("token.fees.lines","token_fee_id",string="Fees Lines")
	payment_ids = fields.One2many("account.payment","token_fee_id",string="Advance Payments")

	_sql_constraints = [
		('unique_token_fees_constraints','UNIQUE(stream_id,company_id,grade_id,degree_level_id,course_id,batch_id,quota_id)','Combination of Stream, College, Grade, Degree, Course, Batch and Quota already exist!')
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

	@api.onchange("degree_level_id","batch_id")
	def onchange_degree_level_id(self):
		self.course_id = False

	def action_open_advance_payments(self):
		action = {
			'name': (_("One Time Fees")),
			'view_mode': 'tree,form',
			'type': 'ir.actions.act_window',
			'res_model': 'account.payment',
			'context':{'readonly':True},
			'domain': [('id','in',self.payment_ids.ids)]
		}
		return action


class TokenFeesLines(models.Model):
	_name = "token.fees.lines"
	_description = "Token Fees Line Items"


	token_fee_id = fields.Many2one("token.fees",string="Fees")
	product_id = fields.Many2one("product.product",string="Fees Heads")
	amount = fields.Float(string="Amount")
