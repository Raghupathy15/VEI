from odoo import fields, models, api


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
    fees_ids = fields.One2many('fees.detail.master', 'fees_id', string="Fees")

    @api.onchange('room_type', 'course_id')
    def _onchange_set_name(self):
        self.name = self.course_id.name
        if self.hotsel_fees:
            self.name = dict(self._fields['room_type'].selection).get(self.room_type)


class FeesDetailsMaster(models.Model):
    _name = 'fees.detail.master'
    _description = 'Fees Details Master'

    fees_id = fields.Many2one('fees.master')
    name = fields.Char('Description')
    amount = fields.Float('Amount')