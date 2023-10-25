from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import format_time


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    communication_street = fields.Char(string='Street')
    communication_street2 = fields.Char(string='Street 1')
    communication_city = fields.Char(string='City')
    communication_zip = fields.Char(string='Zip')
    communication_state_id = fields.Many2one('res.country.state',string='State')
    communication_country_id = fields.Many2one('res.country',string='Country') 
    communication_phone = fields.Char(string='Phone')
    communication_mobile = fields.Char(string='Mobile')
    empl_type = fields.Many2one('employee.type',string='Employee category')
    empl_category = fields.Selection([('teaching', 'Teaching'), ('non_teaching', 'Non Teaching')], string="Employee Type", default='non_teaching',required=True)
    education_lines = fields.One2many('employee.education.line','emp_id',string='Education')
    work_lines = fields.One2many('employee.work.line','emp_id',string='Work Experience')
    extra_lines = fields.One2many('employee.activity.line','emp_id',string='Work Experience')
    proof_lines = fields.One2many('id.proof.line','emp_id',string='Employee Proof')
    tds = fields.Boolean(string='TDS Deduction?',default=False)
    tds_amount = fields.Float(string='TDS Amount',store=True)
    empl_referral_lines = fields.One2many('empl.referral','emp_id',string='Employee Referral')
    ded_allow_lines = fields.One2many('employee.dedcution','emp_id',string='Deduction/Allowance')
    employee_state = fields.Selection([('draft', 'Draft'), ('working','Working'), ('resigned','Resigned')], string="Employee Type", default='working')
    probation_days = fields.Integer('Probation Period (Days)')


    @api.model_create_multi
    def create(self, vals_list):
        if 'empl_id' in tuple(vals_list[0].keys()) or vals_list[0].get('empl_id') == '':
            # obj = self.env['employee.type'].browse(int(vals_list[0].get('empl_type')))
            # if obj.tech_or_non == 'teaching':
            #     str_name = "T"+str(self.env.company.college_code)+str(self.env['ir.sequence'].next_by_code('employee.id'))
            #     vals_list[0].update({'empl_id':str_name})
            # if obj.tech_or_non == 'non_teaching':
            #     str_name = "N"+str(self.env.company.college_code)+str(self.env['ir.sequence'].next_by_code('employee.id'))
            #     vals_list[0].update({'empl_id':str_name})
            # obj = self.env['employee.type'].browse(int(vals_list[0].get('empl_type')))
            if vals_list[0].get('empl_category') == 'teaching':
                str_name = "T"+str(self.env.company.college_code)+str(self.env['ir.sequence'].next_by_code('employee.id'))
                vals_list[0].update({'empl_id':str_name})
            if vals_list[0].get('empl_category') == 'non_teaching':
                str_name = "N"+str(self.env.company.college_code)+str(self.env['ir.sequence'].next_by_code('employee.id'))
                vals_list[0].update({'empl_id':str_name})
        return super(HrEmployeePrivate, self).create(vals_list)
