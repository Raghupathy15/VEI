

from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time
from odoo.exceptions import UserError, ValidationError

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def compute_sheet(self):

        for payslip in self:
            number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
            # delete old payslip lines
            payslip.line_ids.unlink()
            # set the list of contract for which the rules have to be applied
            # if we don't give the contract, then the rules to apply should be for all current contracts of the employee
            contract_ids = payslip.contract_id.ids or \
                           self.get_contract(payslip.employee_id, payslip.date_from, payslip.date_to)
            lines = [(0, 0, line) for line in self._get_payslip_lines(contract_ids, payslip.id)]
            if not payslip.employee_id.tds:
                lines = [item for item in lines if item[2]['name'] != 'TDS']
            if self.employee_id.ded_allow_lines:
                for index, (zero, zero, dictionary) in enumerate(lines):
                    if int(dictionary.get('salary_rule_id')) in self.employee_id.ded_allow_lines.rule_id.ids:
                        obj = self.env['employee.dedcution'].search([('rule_id','=',int(dictionary.get('salary_rule_id'))),('emp_id','=',self.employee_id.id)],limit=1)
                        dictionary['amount'] = obj.fixed_amount
            payslip.write({'line_ids': lines, 'number': number})
        return True
    

    @api.model
    def create(self, vals):
        if 'employee_id' in vals:
            c_obj = self.env['certificate.withdrawn'].search(['|',('employee_id','=',int(vals.get('employee_id'))),('res_emp_id','=',int(vals.get('employee_id'))),('lastdate_date','<',datetime.now().date()),('state','=','withdrawn')])
            if c_obj:
                empl = self.env['hr.employee'].browse(int(vals.get('employee_id')))
                raise ValidationError(_('Cannot create payslip for "%s" due to failing to return the document on time.', empl.name))
        return super(HrPayslip, self).create(vals)