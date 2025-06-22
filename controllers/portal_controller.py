import json
import pytz
from datetime import datetime
from odoo import fields
from odoo.http import Controller,route,request
from odoo.exceptions import ValidationError


class AppointmentPortalController(Controller):

    @route('/my/appointments', type='http', auth='user', website=True)
    def portal_my_appointments(self):
        user_partner = request.env.user.partner_id
        appointments = request.env['appointment.appointment'].sudo().search([
            ('customer_id', '=', user_partner.id)
        ])
        return request.render("appointment_portal_customer.portal_my_appointments", {
            'appointments': appointments,
            'page_name':'appointment_list',
        })

    @route('/my/appointments/<int:appointment_id>',type='http', auth='user', website=True)
    def portal_my_appointment_detail(self,appointment_id):
        appointment=request.env['appointment.appointment'].sudo().browse(appointment_id)

        if not appointment.exists():
            return request.not_found()
        else:
            return request.render('appointment_portal_customer.portal_my_appointment_detail',{
                'appointment':appointment,
                'now':fields.Datetime.now(),
                'page_name':'appointment_form',
            })

    @route(['/my/appointments/<int:appointment_id>/cancel'],type='http', auth='user',methods=['POST'],csrf=False)
    def portal_my_appointment_cancel(self,appointment_id):
        appointment=request.env['appointment.appointment'].sudo().browse(appointment_id)

        if appointment.state=="draft" and appointment.start_datetime>fields.Datetime.now():
            appointment.write({'state':'cancelled'})
        
        return request.redirect('/my/appointments')

    @route(['/my/appointments/new'],type='http', auth='user',website=True)
    def portal_create_appointment(self):
        services = request.env['appointment.service'].sudo().search([])

        return request.render('appointment_portal_customer.portal_create_appointment',{
              'services': services,
              'page_name': 'appointment_new',   
            })

    @route('/my/appointments/new/employees_by_service',type='json', auth='user',methods=['POST'])
    def employees_by_service(self):
        data = json.loads(request.httprequest.get_data().decode('utf-8'))
        service_id = data.get('service_id')
        employees = request.env['hr.employee'].sudo().search([
            ("service_ids","in",[service_id])
        ])

        return [
            {'id': employee.id, 'name': employee.name}
            for employee in employees
        ]
    
    def user_tz_to_utc(self, env, dt_local):
        if dt_local is None:
            return None
        user_tz = pytz.timezone(env.user.tz or 'UTC')
        local_dt = user_tz.localize(dt_local, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.UTC)
        return utc_dt
    
    def _check_quantity_selected_service(self,service_id):
        service = request.env["appointment.service"].sudo().browse(service_id)
        if not service.exists() or service.quantity <= 0:
            raise ValidationError("No available quantity for the selected service.")
        
    def _check_start_datetime_by_now(self,start_datetime):
        now_utc = datetime.now(pytz.utc)
        print(f"datetime_now: {now_utc}")
        if start_datetime < now_utc:
            raise ValidationError("The start datetime cannot be set in the past")


    @route(['/my/appointments/submit'], type='http', auth='user', website=True, csrf=True)
    def portal_submit_appointment(self, **post):
        customer = request.env.user.partner_id
        error_message = None

        try:
            start_datetime_str = post.get('start_datetime')
            duration_str = post.get('duration') 
            employee_id_str = post.get('employee_id')
            service_id_str = post.get('service_id')

            self._check_quantity_selected_service(int(service_id_str))

            naive_dt = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")
            start_datetime_utc = self.user_tz_to_utc(request.env, naive_dt)
            start_datetime_str_utc = fields.Datetime.to_string(start_datetime_utc)

            if start_datetime_utc.tzinfo is None:
                start_datetime_utc = pytz.utc.localize(start_datetime_utc)
            print(f"datetime_now: {start_datetime_utc}")


            self._check_start_datetime_by_now(start_datetime_utc)
           
            request.env['appointment.appointment'].sudo().create({
                'customer_id': customer.id,
                'service_id': int(service_id_str),
                'employee_id': int(employee_id_str),
                'start_datetime': start_datetime_str_utc,
                'duration': float(duration_str),
                'state': 'draft',
            })

        except ValidationError as ve:
            error_message = str(ve)
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"

        if error_message:     
            return request.render('appointment_portal_customer.portal_create_appointment', {
                'services': request.env['appointment.service'].sudo().search([]),
                'error': error_message,
                'default_vals': post,
                'page_name': 'appointment_new',
            })

        return request.redirect('/my/appointments')


    @route('/my/employees', type='http', auth='user', website=True)
    def portal_my_employees(self):
        employees = request.env['hr.employee'].sudo().search([
            ('service_ids','!=',False)
        ])

        return request.render("appointment_portal_customer.portal_my_employees", {
            'employees': employees,
            'page_name':'employee_list',
        })
    
    @route('/my/workfields',type='http', auth='user', website=True)
    def portal_my_workfields(self):
        workfields = request.env['appointment.workfield'].sudo().search([])

        return request.render('appointment_portal_customer.portal_my_workfields',{
            'workfields': workfields,
            'page_name': 'workfield_list',
        })

    @route('/my/workfields/<int:workfield_id>/services',type='http', auth='user', website=True)
    def portal_my_services_of_workfield(self,workfield_id):
        services = request.env['appointment.service'].sudo().search([
            ('workfield_id','=',workfield_id)
        ])

        return request.render('appointment_portal_customer.portal_my_services_of_workfield',{
            'services': services,
            'page_name': 'service_list',
        })




