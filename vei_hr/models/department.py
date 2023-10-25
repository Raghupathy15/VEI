from odoo import fields, models, api

class HrDepartment(models.Model):
    _inherit = 'hr.department'

    courses_id = fields.Many2one('degree.master', string="Course")
    courses_ids = fields.Many2many('degree.master', string="Course")

    def allocate_section_students(self):
        students = self.env['student.details'].sudo().search([('section_id','=',False)])
        if students:
            degree_list = []
            for student in students:
                if student.courses_id and student.courses_id.degree_id :
                    degree_list.append(student.courses_id.degree_id.id)
            if degree_list:
                departments = self.env['hr.department'].sudo().search([('courses_ids', 'in', degree_list)])
                if departments:
                    for department in departments:
                        student_datas = []
                        sr_no = 1
                        for student in students:
                            # if student.courses_id and student.courses_id.degree_id and student.courses_id.degree_id.id == department.courses_id.id:
                            if student.courses_id and student.courses_id.degree_id and student.courses_id.degree_id.id in department.courses_ids.ids:
                                student_dic = {
                                    'sr_no': sr_no,
                                    'role_no': student.role_no,
                                    'name': student.name,
                                }
                                student_datas.append(student_dic)
                                sr_no += 1
                        if student_datas:
                            ctx = {}
                            db = self.env.cr.dbname
                            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                            action_id = self.env.ref('vg_colg.regular_students_list_act_window').id
                            menu_id = self.env.ref('vg_colg.regular_student_menu').id
                            ctx[
                                'action_url'] = "{}/web?db={}#action={}&model=student.details&view_type=list&menu_id={}".format(
                                base_url, db, action_id, menu_id)
                            ctx['student_datas'] = student_datas
                            mail_template = self.env.ref(
                                'vei_hr.mail_remainder_allocate_section_template')
                            mail_template.with_context(ctx).sudo().send_mail(department.id, force_send=True, email_values={
                                'email_to': department.manager_id.work_email})
