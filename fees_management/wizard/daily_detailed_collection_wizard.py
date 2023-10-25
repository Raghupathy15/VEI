from odoo import models,fields,api,_
from odoo.exceptions import MissingError


class DailyDetailedCollectionReportWizard(models.TransientModel):
    _name = "daily.detailed.collection.report.wizard"

    
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    batch_id = fields.Many2one('batch.courses.master',string="Batch")
    course_id = fields.Many2one('courses.master',string="Course")
    semester_id = fields.Many2one('semester.master',string="Semester")
    term_id = fields.Many2one('fees.for',string="Term")
    status = fields.Selection([('true','Active'),('false','In Active')],default='true',string="Status")
    cashier_ids = fields.Many2many('res.users',default=lambda self:[(4,self.env.user.id)])
    company_id = fields.Many2one('res.company',default=lambda self:self.env.company.id)


    @api.onchange('batch_id')
    def onchange_batch_id(self):
        domain = [('company_id','=',self.env.company.id)]
        if self.batch_id:
            domain.append(('batch_id','=',self.batch_id.id))
        
        return {
            'domain':{'course_id':domain}
        }

    @api.onchange('semester_id')
    def onchange_semester_id(self):
        return {
            'domain':{'term_id':[('id','in',self.semester_id.term_ids.ids)]}
        }


    # Redirect Payments Consolidated Report
    def load_daily_detailed_collection_report(self):
        report_dict = {}
        report_dict = self.env.ref('fees_management.action_daily_detailed_collection_report').report_action(self)
        return report_dict
    

    # Print PDF
    def print_pdf(self):
        print("Control arrived in print PDF!")
        return self.load_daily_detailed_collection_report()