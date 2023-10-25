from odoo import models,fields,api,_ 


class InheritProductProduct(models.Model):
    _inherit = "product.product"


    token_ok = fields.Boolean(string="can be token?", default=False,track_visibility="always",)


class InheritProductTemplate(models.Model):
    _inherit = "product.template"


    token_ok = fields.Boolean(string="can be token?", default=False,track_visibility="always")


    @api.model
    def create(self,values):
        res = super(InheritProductTemplate,self).create(values)
        for itm in res.product_variant_ids:
            itm.token_ok = res.token_ok
        return res

    def write(self,values):
        res = super(InheritProductTemplate,self).write(values)
        for itm in self.product_variant_ids:
            itm.token_ok = self.token_ok
        return res