from odoo import fields, models, api,_
from datetime import datetime
from odoo.exceptions import ValidationError

class CoursesMaster(models.Model):
    _name = 'courses.master'
    _description = 'Courses Master'
    _rec_name = 'name'

    name = fields.Char('Course Name',copy=False)
    stream_id = fields.Many2one('stream.master',string='Stream',index=True)
    grade_id = fields.Many2one('grade.master', string='Grade',index=True)
    degree_level_id = fields.Many2one('degree.level.master', string="Degree",index=True)
    degree_id = fields.Many2one('degree.master', string='Course',index=True)
    duration = fields.Char(string='Duration')
    token_num = fields.Char(string="Token Code")
    sequence = fields.Integer(string="Sequence")
    batch_id = fields.Many2one("batch.courses.master", string="Batch",index=True,copy=False)
    company_id = fields.Many2one('res.company',string="College",default=lambda self:self.env.company.id,index=True)

    _sql_constraints =  [
        ('unique_fees_record', 'UNIQUE(stream_id,company_id,grade_id,degree_level_id,degree_id,batch_id,duration)', 'Combination of Stream,College,Grade,Degree,Batch,Duration and Course is already exist!'),
    ]


    @api.model
    def create(self,vals):
        res = super(CoursesMaster,self).create(vals)
        res.get_compute_name()
        return res
    
    def write(self,vals):
        res = super(CoursesMaster,self).write(vals)
        if 'batch_id' in vals.keys() or 'degree_id' in vals.keys():
            self.get_compute_name()
        return res

    def get_compute_name(self):
        for config in self:
            course = config.degree_id.name if config.degree_id.name else ''
            batch = config.batch_id.name if config.batch_id.name else ''
            config.name = course + ' - [' + batch + ']'
    
    @api.onchange('stream_id')
    def onchange_stream_id(self):
        self.company_id = False
        
    
    @api.onchange('company_id')
    def onchange_company_id(self):
        self.grade_id = False

    
    @api.onchange('grade_id')
    def onchange_grade_id(self):
        self.degree_level_id = False
        
    
    @api.onchange('degree_level_id','grade_id','company_id','stream_id')
    def domain_for_degree_course(self):
        self.degree_id = False
        domain = []
        if self.stream_id:
            domain.append(('stream_id','=',self.stream_id.id))
        if self.grade_id:
            domain.append(('grade_id','=',self.grade_id.id))
        if self.company_id:
            courses_college_objs = self.env['courses.college.master'].search([('company_id','=',self.company_id.id)])
            course_ids = []
            for itm in courses_college_objs:
                course_ids.append(itm.courses_ids.ids)

            domain.append(('id','in',(course_ids[0] if course_ids else [])))
    
        if domain:
            return {'domain':{
                        'degree_id':domain
                        }
            }
    
        
class BatchCoursesMaster(models.Model):
    _name = 'batch.courses.master'
    _description = 'Batch Courses Master'

    name = fields.Char(string='Batch')
    start_month = fields.Char(string="Start Month",required=True)
    start_year = fields.Char(string='Start Year',required=True)
    end_month = fields.Char(string='End Month',required=True)
    end_year = fields.Char(string='End Year',readonly=True)
    duration = fields.Integer(string='Duration',required=True)
    active = fields.Boolean(string="Active",default=True)


    _sql_constraints = [
        ('unique_batch_details','UNIQUE(name,start_year,end_year,duration)','Combination of Batch Name, Start Year, End Year and Duration must be unique!'),
    ]


    @api.onchange('start_month','end_month')
    def onchange_of_month(self):
        if self.start_month or self.end_month:
            try:
                start_month = int(self.start_month) if self.start_month else ''
                end_month = int(self.end_month) if self.end_month else ''

                if start_month:
                    if start_month >= 0 and start_month <= 12:
                        pass
                    else:
                        raise ValidationError(_("Start Month and End Month should be inbetween 1 - 12"))
                
                if end_month:
                    if end_month >= 0 and end_month <= 12:
                        pass
                    else:
                        raise ValidationError(_("Start Month and End Month should be inbetween 1 - 12"))
            except Exception as e:
               raise ValidationError(_('Please Enter Valid Start Year! (' + str(e) + ')'))
            
    
    @api.onchange('start_year','duration')
    def get_calculate_batch(self):
        if self.duration and self.duration <= 0:
            raise ValidationError(_("Course Duration Should be atleast 1 or more than of it!"))
        if self.start_year and self.duration:
            try:
                start_year = int(self.start_year)
            except Exception as e:
                raise ValidationError(_('Please Enter Valid Start Year! (' + str(e) + ')'))
            self.end_year = start_year + self.duration
            self.name = 'Batch ' + str(self.start_year)[-2:] + ' - ' + str(self.end_year)[-2:]


    @api.model
    def create(self,vals):
        res = super(BatchCoursesMaster,self).create(vals)
        if not res.start_year and not res.duration:
            raise ValidationError(_("Start year and End Year is shouldn't be empty!"))
        return res
