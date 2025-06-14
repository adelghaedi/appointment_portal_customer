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




