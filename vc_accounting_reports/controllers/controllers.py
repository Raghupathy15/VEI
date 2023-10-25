# -*- coding: utf-8 -*-
# from odoo import http


# class CrmAccess(http.Controller):
#     @http.route('/crm_access/crm_access/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_access/crm_access/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_access.listing', {
#             'root': '/crm_access/crm_access',
#             'objects': http.request.env['crm_access.crm_access'].search([]),
#         })

#     @http.route('/crm_access/crm_access/objects/<model("crm_access.crm_access"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_access.object', {
#             'object': obj
#         })
