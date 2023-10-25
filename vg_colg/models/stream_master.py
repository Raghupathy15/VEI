from odoo import fields, models, api


class StreamMaster(models.Model):
	_name = 'stream.master'
	_description = 'Stream Master'

	name = fields.Char('Name')

	_sql_constraints = {
		('unique_stream_master_constraints','UNIQUE(name)','Stream is alreay exist!')
	}


class ResCompany(models.Model):
	_inherit = 'res.company'
		
	custom_sequence = fields.Integer(string="Custom Sequence", default=1)
	stream_ids = fields.Many2many('stream.master',string="Stream")
	grade_ids = fields.Many2many('grade.master',string="Grade")
	principle_id = fields.Many2one('res.users',string="Principle")


	@api.onchange('stream_ids')
	def onchange_stream_ids(self):
		domain = []
		if self.stream_ids:
			self.grade_ids = False
			domain.append(('stream_ids','in',self.stream_ids.ids))
		return {'domain':{ 'grade_ids':domain}}