from odoo import models,fields,api,_


class ConcessionRejectionWizard(models.TransientModel):
    _name = "concession.rejection.wizard"
    _desc = "Inorder get the reason from the user for Concession Rejection"

    name = fields.Char(string="Reason for Rejection")


    def action_concession_reject(self):
        concession_obj = self.env['student.concession'].sudo().browse(self.env.context.get('concession_id'))
        for obj in concession_obj:
            obj.remarks = self.name
        concession_obj.action_to_reject()
        

        