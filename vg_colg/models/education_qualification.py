from odoo import fields, models, api


class EducationQualification(models.Model):
	_name = 'education.qualification'
	_description = 'Education Qualification'

	admission_confirmation_id = fields.Many2one('admission.confirmation', string="Admission Confirmation")
	admission_list_id = fields.Many2one('admission.list', string="Admission List")
	student_details_id = fields.Many2one('student.details', string="Student Details")
	name = fields.Char('Description')
	marks = fields.Float('Marks')
	per = fields.Float('%')

	ug_id = fields.Many2one('ug.master', string="Std/UG/PG")
	stream_id = fields.Many2one('stream.master', string="Stream")
	school = fields.Char('School/College')
	place_id = fields.Many2one('place.city.master', string="City")
	state_id = fields.Many2one("res.country.state", string="State")
	board_id = fields.Many2one('board.master', string="Board")

	display_type = fields.Selection(
		selection=[
			('line_section', "Section"),
		],
		default=False)


class UgMaster(models.Model):
	_name = 'ug.master'
	_description = 'UG Master'

	name = fields.Char('Name')


class BoardMaster(models.Model):
	_name = 'board.master'
	_description = 'Board Master'

	name = fields.Char('Name')


class FeeDetails(models.Model):
	_name = 'fee.details'
	_description = 'Fee Details'

	admission_confirmation_id = fields.Many2one('admission.confirmation', string="Fee Admission Confirmation")
	student_details_id = fields.Many2one('student.details', string="Student Details")
	term_fee = fields.Char('Term Fee')
	receipt_no = fields.Char('Receipt No.')
	signature = fields.Char('Signature')
	other_fee = fields.Char('Other Fee')
	date = fields.Date('Date')

	receipt_no_i = fields.Char()
	signature_i = fields.Char()
	date_i = fields.Date()
	name = fields.Char('Description')
	amount = fields.Float('Amount')

class InspectionImage(models.Model):
	_name = 'inspection.image'
	_description = 'Inspection Image'

	admission_confirmation_id = fields.Many2one('admission.confirmation')
	admission_list_id = fields.Many2one('admission.list')
	student_details_id = fields.Many2one('student.details', string="Student Details")
	image = fields.Binary(string='Image')
	file_name = fields.Char('File Name', store=True)
	name = fields.Text('Description')
	verified = fields.Boolean('Verified')
	is_mandatory = fields.Boolean('Is Mandatory')
	is_collected = fields.Boolean('Is Collected')

	@api.onchange('document_templates_id')
	def set_is_mandatory_document_templates_id(self):
		for inspection in self:
			inspection.is_mandatory = inspection.document_templates_id.is_mandatory
