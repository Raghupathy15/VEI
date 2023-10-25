from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from odoo.tools.misc import get_lang
import pytz
from datetime import datetime
from num2words import num2words


class AccountMove(models.Model):
	_inherit = 'account.move'

	@api.depends('posted_before', 'state', 'journal_id', 'date')
	def _compute_name(self):
		self = self.sorted(lambda m: (m.date, m.ref or '', m.id))
		for move in self:
			seq_match = move._sequence_matches_date()
			last_seq = move._get_last_sequence(lock=False)
			move_has_name = move.name and move.name != '/'
			if move_has_name or move.state != 'posted':
				if not move.posted_before and not seq_match:
					if last_seq:
						# The name does not match the date and the move is not the first in the period:
						# Reset to draft
						move.name = False
						continue
				else:
					if move_has_name and move.posted_before or not move_has_name and last_seq:
						# The move either
						# - has a name and was posted before, or
						# - doesn't have a name, but is not the first in the period
						# so we don't recompute the name
						continue
			if move.date and (not move_has_name or not seq_match):
				if move.journal_id.payment_sequence and move.payment_id:
					seq = "%s/%s/" % (self.env.company.college_code,str(datetime.now().year))
					seq += str(self.env['ir.sequence'].next_by_code('account.payment.seq'))
					move.name = seq
				else:
					move._set_next_sequence()

		self.filtered(lambda m: not m.name and not move.quick_edit_mode).name = '/'
		self._inverse_name()
