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
            })

    @route(['/my/appointments/<int:appointment_id>/cancel'],type='http', auth='user',methods=['POST'],csrf=False)
    def portal_my_appointment_cancel(self,appointment_id):
        appointment=request.env['appointment.appointment'].sudo().browse(appointment_id)

        if appointment.state=="draft" and appointment.start_datetime>fields.Datetime.now():
            appointment.write({'state':'cancelled'})
        
        return request.redirect('/my/appointments')

    @route('/my/employees', type='http', auth='user', website=True)
    def portal_my_employees(self):
        services=request.env['appointment.service'].sudo().search([])
        employees = request.env['hr.employee'].sudo().search([
            ('service_ids','!=',False)
        ])

        return request.render("appointment_portal_customer.portal_my_employees", {
            'employees': employees,
        })




