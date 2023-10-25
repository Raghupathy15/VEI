# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from datetime import datetime,timedelta
import json


class StdForm(http.Controller):


    @http.route(['/student-admission'], type='http', auth='public', website=True)
    def student_admission_form(self, **post):
        community_master = request.env['community.master'].sudo().search([])
        places = request.env['place.city.master'].sudo().search([])
        taluks = request.env['taluk.master'].sudo().search([])
        districts = request.env['district.master'].sudo().search([])
        institution_groups = request.env['institution.group.master'].sudo().search([])
        last_studied_institutions = request.env['last.studied.institutions'].sudo().search([])
        courses = request.env['courses.master'].sudo().search([])
        grade_ids = request.env['grade.master'].sudo().search([])
        degree_id = request.env['degree.level.master'].sudo().search([])
        references = request.env['reference.master'].sudo().search([])
        company_id = request.env['res.company'].sudo().search([], limit=1)
        values = {
            'community_master': community_master,
            'places': places,
            'taluks': taluks,
            'districts': districts,
            'institution_groups': institution_groups,
            'last_studied_institutions': last_studied_institutions,
            'courses': courses,
            'grade_ids': grade_ids,
            'degree_id': degree_id,
            'references': references,
            'company_id': company_id,
            'location': post.get('location') if post.get('location') else None,
            'batch': "%s-%s"% (datetime.now().strftime("%Y"),int(datetime.now().strftime("%Y"))+1),
        }
        return request.render('vg_colg.create_website_student_admission', values)

    @http.route(['/student-admission-created'], type='http', auth="public", methods=['POST'], website=True)
    def std_admission_created(self, **post):
        pending_std = request.env['student.admission'].sudo().search([('aadhaar_code','=',post.get('aadhar_code')),('state','=','inquiry')],limit=1)
        if not pending_std:
            dict_vals = {
                'location': post.get('location'),
                'name_initial': post.get('initial'),
                'name': post.get('name'),
                'email': post.get('email'),
                'birth_date': post.get('birth_date') or False,
                'parent_guardian_name': post.get('parent_guardian_name'),
                'parent_guardian_occupation': post.get('parent_guardian_occupation'),
                'aadhaar_code': post.get('aadhar_code'),
                'mobile_number': post.get('mobile_number'),
                'whatsapp_number': post.get('whatsapp_number'),
                'caste': post.get('caste'),
                'community_id': int(post.get('community_id')) if post.get('community_id') else False,
                'gender': post.get('gender'),
                'place_id': int(post.get('place_id')) if post.get('place_id') else False,
                'taluk_id': int(post.get('taluk_id')) if post.get('taluk_id') else False,
                'district_id': int(post.get('district_id')) if post.get('district_id') else False,
                'pin_code': post.get('pin_code'),
                'batch': post.get('batch'),
                'ug_regn_number': post.get('ug_regn_number'),
                'group_ug_number': post.get('group_ug_branch'),
                'total_marks_ug': post.get('total_marks_ug'),
                'institution_group_id': int(post.get('institution_group_id')) if post.get('institution_group_id') else False,
                'last_studied_institution_id': int(post.get('last_studied_institution_id')) if post.get('last_studied_institution_id') else False,
                'stream_id': int(post.get('stream_by_id')) if post.get('stream_by_id') else False,
                'company_id': int(post.get('company_by_id')) if post.get('company_by_id') else False,
                'grade_id': int(post.get('grade_id')) if post.get('grade_id') else False,
                'degree_level_id': int(post.get('degree_id')) if post.get('degree_id') else False,
                'courses_id': int(post.get('courses_id')) if post.get('courses_id') else False,
                'referred_by_id': int(post.get('referred_by_id')) if post.get('referred_by_id') else False,
            }
            quota_id = request.env['quota.master'].sudo().search([('is_default','=',True)],limit=1).id
            dict_vals.update(quota_id=quota_id)
            std = request.env['student.admission'].sudo().create(dict_vals)
            std.batch_id = std.courses_id.batch_id.id
            std.onchange_batch_id()
            # template_id = request.env.ref('vg_colg.mail_template_demo_student_admission_template').sudo()
            template_id = request.env.ref('vg_colg.mail_student_admission_template').sudo()
            if template_id:
                template_id.send_mail(std.id, force_send=True, email_values={"email_to": std.email})
            return request.render('vg_colg.std_thanks', {'student': std})
        else:
            return request.render('vg_colg.std_panding', {'student': pending_std})
    

    def get_first_last_date(self,year, month):
        first_date = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d")
        last_date = (first_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        return first_date, last_date

    def is_current_date_within_range(self,start_year, start_month, end_year, end_month):
        current_date = datetime.now()
        start_date, end_date = self.get_first_last_date(start_year, start_month)[0], self.get_first_last_date(end_year, end_month)[1]
        return start_date <= current_date <= end_date
    
    def compare_batch(self,batch_id):
        if batch_id:
            if batch_id.start_year and batch_id.end_year and batch_id.start_month and batch_id.end_month:
                return self.is_current_date_within_range(batch_id.start_year, batch_id.start_month, batch_id.end_year, batch_id.end_month)
            else:
                return False
        else:
            return False


    @http.route(['/aadhaarcard'], type='json', auth="public", website=True)
    def remove_line(self, addhar=None, **post):
        if addhar:
            students = request.env['student.admission'].sudo().search([('aadhaar_code', '=', addhar)])
            for student in students:
                if student.aadhaar_code == addhar and self.compare_batch(student.batch_id):
                    return True
        else:
            return False
        
    # on change of stream
    @http.route(['/stream'], type='json', auth="public", website=True)
    def college_by_stream(self, stream=None, **post):
        if stream:
            colleges = request.env['res.company'].sudo().search([('stream_ids', 'in', [int(stream)])])
            colleges_list = []
            for college in colleges:
                colleges_list.append((college.name,college.id))
            return colleges_list
        else:
            return False
        
    # on change of company
    @http.route(['/company'], type='json', auth="public", website=True)
    def grade_by_college(self, **post):
        data = post
        if data:
            grade_ids = request.env['grade.master'].sudo().search([('stream_ids', 'in', [int(data.get('company').get('stream'))])])
            grade_list = []
            for grade in grade_ids:
                grade_list.append((grade.name,grade.id))
            return grade_list
        else:
            return False

    # on change of grade
    @http.route(['/grade'], type='json', auth="public", website=True)
    def degree_by_grade(self, **post):
        data = post
        if data:
            degree_ids = request.env['degree.level.master'].sudo().search([('grade_id', 'in', [int(data.get('company').get('grade'))]),('stream_id', 'in', [int(data.get('company').get('stream'))])])
            degree_list = []
            for degree in degree_ids:
                degree_list.append((degree.name,degree.id))
            return degree_list
        else:
            return False

    # on change of degree
    @http.route(['/degree'], type='json', auth="public", website=True)
    def course_by_grade(self, **post):
        data = post
        if data:
            course_ids = request.env['courses.master'].sudo().search([('stream_id','in',[int(data.get('company').get('stream'))]),('company_id','in',[int(data.get('company').get('company'))]),('grade_id', 'in', [int(data.get('company').get('grade'))])])
            course_list = []
            for course in course_ids:
                course_list.append((course.degree_id.name,course.id))
            return course_list
        else:
            return False