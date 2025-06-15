from datetime import datetime, timedelta
from odoo import fields
from odoo.http import Controller,route,request

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
    def employees_by_service(self,service_id):
        employees = request.env['appointment.employee'].sudo().search([
            ('service_ids','in',int(service_id))
        ])
        

        return [
            {'id': employee.id, 'name': employee.name}
            for employee in employees
        ]


    @route(['/my/appointments/submit'], type='http', auth='user', website=True, csrf=True)
    def portal_submit_appointment(self, **post):
        partner = request.env.user.partner_id
        try:
            date_str = post.get('date') 
            time_str = post.get('time')
            start_datetime_str = f"{date_str} {time_str}"
            start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")

            service = request.env['appointment.service'].sudo().browse(int(post.get('service_id')))
            duration_minutes = service.duration or 30  

            end_datetime = start_datetime + timedelta(minutes=duration_minutes)

            request.env['appointment.appointment'].sudo().create({
                'partner_id': partner.id,
                'service_id': service.id,
                'employee_id': int(post.get('employee_id')),
                'start_datetime': start_datetime,
                'end_datetime': end_datetime,
                'duration': duration_minutes,
                'state': 'draft',
            })
        except Exception as e:
            return request.render('appointment_portal_customer.portal_create_appointment', {
                'services': request.env['appointment.service'].sudo().search([]),
                'error': str(e),
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




