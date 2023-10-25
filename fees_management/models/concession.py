from odoo import models,fields,api,_
from odoo.exceptions import ValidationError


class InheritConcession(models.Model):
    _inherit = "student.concession"


    invoices_map_ids = fields.One2many('map.move.concession','concession_id',string="Invoices Map")
    invoices_ids = fields.Many2many('account.move',string="Invoices",compute="get_invoices_ids")
    concession_used_amount = fields.Float(string="Used Concession Amount",compute="get_compute_concession_amount")
    concession_balance_amount = fields.Float(string="Balance Concession Amount",compute="get_compute_concession_amount")


    def action_open_invoices(self):
        action = {
			'name': _("Collections"),
			'view_mode': 'tree,form',
			'type': 'ir.actions.act_window',
			'res_model': 'account.move',
			'domain': [('id','in',self.invoices_ids.ids)]
		}
        return action

    def get_invoices_ids(self):
        for concession in self:
            map_invoices_ids = self.env['account.move'].sudo()
            for map in concession.invoices_map_ids:
                map_invoices_ids += map.invoice_id
            concession.invoices_ids = map_invoices_ids

    def get_compute_concession_amount(self):
        for concession in self:
            concession.concession_used_amount = sum(concession.invoices_map_ids.mapped('allocated_amount')) or 0.00
            concession.concession_balance_amount = concession.amount - concession.concession_used_amount

    def unlink(self):
        if self.invoices_ids:
            raise ValidationError(_("Before deleting the Concession please revoke the concession in the applied collections!"))
        res = super(InheritConcession,self).unlink()

        return res

class MapMoveConcession(models.Model):
    _name = "map.move.concession"


    invoice_id = fields.Many2one('account.move',string="Collection")
    details_id = fields.Many2one(related="invoice_id.details_id")
    concession_id = fields.Many2one('student.concession',string="Concession",index=True)
    available_amount = fields.Float(string="Available Amount")
    allocated_amount = fields.Float(string="Allocated Amount")

    _sql_constraints = [
        ('unique_move_and_concession','UNIQUE(invoice_id,concession_id)','Repeated concessions not allowed against one collection!')
    ]


    @api.onchange('concession_id')
    @api.depends('concession_id')
    def onchange_concession_id(self):
        self.available_amount = self.concession_id.concession_balance_amount or 0.0

    @api.onchange('allocated_amount')
    @api.onchange('allocated_amount')
    def onchange_allocated_amount(self):
        if self.allocated_amount and self.allocated_amount > self.available_amount:
            raise ValidationError(_("Concession Allocated Amount Should be less than or equal to available Amount!"))

    @api.model
    def create(self,vals):
        res = super(MapMoveConcession,self).create(vals)
        return res
    
    def write(self,vals):
        res = super(MapMoveConcession,self).write(vals)
        return res