import pytz
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, exceptions, _
from odoo.tools import float_round
from datetime import date, datetime, time, timedelta


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def _attendance_action_change(self):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        self.ensure_one()
        action_date = fields.Datetime.now()
        current_date = datetime.now().date()
        calendar_obj = self.env["resource.calendar.attendance"].search([('calendar_id','=',self.resource_calendar_id.id),('dayofweek','=',date.today().weekday() + 1),('day_period','=','morning')])
        time_now_ist = pytz.utc.localize(datetime.now())
        time_now_ist = time_now_ist.astimezone(pytz.timezone(self.env.context.get('tz'))).replace(microsecond=0, tzinfo=None)

        if self.attendance_state != 'checked_in':
            # in_record = self.env['hr.attendance'].search([
            #     ('check_in', '<=', datetime.combine(current_date, time(23, 59, 59))),
            #     ('check_in', '>=', datetime.combine(current_date, datetime.min.time()))
            # ])
            # if in_record:
            #     raise exceptions.UserError(_('Already Checked In today'))
            recent_check_ins = self.env['hr.attendance'].search([], order='check_in desc')
            vals ={}     
            vals = {
                'employee_id': self.id,
                'check_in': action_date,
                'status':'working'
            }
            if calendar_obj:
                hours = int(calendar_obj.hour_from)
                decimal_minutes = (calendar_obj.hour_from - hours) * 60
                minutes, seconds = divmod(decimal_minutes * 60, 60)
            
                abscent_time = datetime.combine(current_date, time(int(hours), int(minutes), 00))+timedelta(hours=1)

                if time_now_ist > abscent_time:
                    abst_time = (time_now_ist-abscent_time)
                    formatted_time_difference = str(abst_time).split(".")[0]
                    vals.update({'late':True,'status':'leave','late_time':formatted_time_difference})
                    attendance = self.env['hr.attendance'].create(vals)
                    starting_hour = datetime.combine(datetime.now().date(), time(2, 30, 0))
                    ending_hour = datetime.combine(datetime.now().date(), time(11, 30, 0))
                    full_day = {'holiday_status_id':4,
                                'holiday_type': 'employee', 
                                'employee_id': self.id,
                                'request_date_from':datetime.now().date(),
                                'request_date_to':datetime.now().date(),
                                'date_from': starting_hour, 
                                'date_to': ending_hour,
                                'attendance_id':attendance.id,
                                }
                    env = self.env['hr.leave'].create(full_day)
                    return attendance
                late_time = datetime.combine(current_date, time(int(hours), int(minutes), 00))+timedelta(minutes=30)

                if time_now_ist > late_time:
                    l_time = (time_now_ist-late_time)
                    formatted_time_difference = str(l_time).split(".")[0]
                    vals.update({'late':True,'late_time':formatted_time_difference,'status':'working',})
                    attendance = self.env['hr.attendance'].create(vals)
                    starting_hour = datetime.combine(datetime.now().date(), time(2, 30, 0))
                    ending_hour = datetime.combine(datetime.now().date(), time(6, 30, 0))
                    half_day = {'holiday_status_id':4,
                                'holiday_type': 'employee', 
                                'employee_id': self.id,
                                'request_unit_half':True,
                                'request_date_from':datetime.now().date(),
                                'request_date_to':datetime.now().date(),
                                'date_from': starting_hour, 
                                'date_to': ending_hour,
                                'attendance_id':attendance.id,
                                }
                    self.env['hr.leave'].create(half_day)
                    return attendance
            return self.env['hr.attendance'].create(vals)
        attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
        if attendance:


            # out_record = self.env['hr.attendance'].search([
            #     ('check_out', '<=', datetime.combine(current_date, time(23, 59, 59))),
            #     ('check_out', '>=', datetime.combine(current_date, datetime.min.time()))
            # ])
            # if out_record:
            #     raise exceptions.UserError(_('Already Checked out today'))
            # current_date = datetime.now().date()
            # extra_hour = datetime.combine(current_date, time(18, 30, 0))
            # print(" datetime.now() = ",datetime.now())
            # print(" extra_hour = ",extra_hour)
            # if time_now_ist > extra_hour:
            #     e_hour = (time_now_ist-extra_hour)
            #     formatted_time_difference = str(e_hour).split(".")[0]
            #     attendance.extra_hour = formatted_time_difference

            # delta = (action_date - attendance.check_in).total_seconds()
            # float_time = attendance.employee_id.resource_calendar_id.hours_per_day
            # total_seconds = (int(float_time) * 3600) + (int((float_time * 60) % 60) * 60) + int((float_time * 3600) % 60)

            # if int(delta)>int(total_seconds):
            #     xtr_time = float(int(delta)-int(total_seconds))/3600.0
            #     attendance.extra_hour = xtr_time
                # if xtr_time> 3.0:

            attendance.check_out = action_date
        else:
            raise exceptions.UserError(_('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                'Your attendances have probably been modified manually by human resources.') % {'empl_name': self.sudo().name, })
        return attendance





