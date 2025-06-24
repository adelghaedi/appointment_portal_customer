{
    'name': 'Appointment Portal Customer',
    'version': '17.0.1.0.0',
    'category': 'Portal',
    'summary': 'Customer portal',
    'depends': [
        'base',
        'appointment_module',
        'portal',
        'website',
    ],
    'data': [
        'views/portal_template.xml',
        'views/appointment_template.xml',
        'views/employee_template.xml',
        'views/service_template.xml',
    ],
    'installable': True,
    'application': False,
}