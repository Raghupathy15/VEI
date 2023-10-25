from odoo import fields, models, api


class PlaceCityMaster(models.Model):
    _name = 'place.city.master'
    _description = 'Place City Master'

    name = fields.Char()
