# -*- coding: utf-8 -*-
from odoo import models, fields, api

try:
	import qrcode
except ImportError:
	qrcode = None
try:
	import base64
except ImportError:
	base64 = None
from io import BytesIO


class ResCompany(models.Model):
	_inherit = 'res.company'

	qr_url = fields.Char(string="QR URL", readonly=False)
	qr = fields.Binary(string="QR Code")

	def qr_generate(self):
		if qrcode and base64 and self.qr_url:
			qr = qrcode.QRCode(
				version=1,
				error_correction=qrcode.constants.ERROR_CORRECT_L,
				box_size=10,
				border=4,
			)
			qr.add_data(self.qr_url)
			qr.make(fit=True)

			img = qr.make_image()
			temp = BytesIO()
			img.save(temp, format="PNG")
			qr_image = base64.b64encode(temp.getvalue())
			self.write({'qr': qr_image})
			return self.env.ref(
				'customer_qr.print_qr').report_action(self, data={
				'data': self.id, 'type': 'cust'})