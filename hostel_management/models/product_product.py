from odoo import models,fields,api,_ 


class InheritProductProduct(models.Model):
    _inherit = "product.product"


    hostel_ok = fields.Boolean(string="can be hostel?", default=False,track_visibility="always",)
    courses_ids = fields.Many2many("courses.master", string="Courses",track_visibility="always")


    @api.onchange('hostel_ok')
    def onchange_hotel_ok(self):
        if self.hostel_ok:
            self.detailed_type = 'service'

    
    # @api.onchange('hostel_ok', 'courses_ids')
    # def _onchange_product_fields(self):
    #     for product in self:
    #         template_vals = {}
    #         if product.hostel_ok != product.product_tmpl_id.hostel_ok:
    #             template_vals['hostel_ok'] = product.hostel_ok
    #         if product.courses_ids != product.product_tmpl_id.courses_ids:
    #             template_vals['courses_ids'] = [(6, 0, product.courses_ids.ids)]

    #         if template_vals:
    #             self.env['product.template'].sudo()._update_template_fields(product, template_vals)


class InheritProductTemplate(models.Model):
    _inherit = "product.template"


    hostel_ok = fields.Boolean(string="can be hostel?", default=False,track_visibility="always")
    courses_ids = fields.Many2many("courses.master", string="Courses",track_visibility="always")


    @api.model
    def create(self,values):
        res = super(InheritProductTemplate,self).create(values)
        for itm in res.product_variant_ids:
            itm.hostel_ok = res.hostel_ok
            itm.courses_ids = res.courses_ids
        return res

    def write(self,values):
        res = super(InheritProductTemplate,self).write(values)
        for itm in self.product_variant_ids:
            itm.hostel_ok = self.hostel_ok
            itm.courses_ids = self.courses_ids
        return res