{
    'name': 'Appointment Portal Customer',
    'version': '17.0.1.0.0',
    'category': 'Website',
    'summary': 'Adds a customer portal for managing appointments, services, and employee details.',
    'author': 'Adel Ghaedi',
    'website': 'https://github.com/adelghaedi/appointment_portal_customer/',
    'license': 'MIT',
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
    'auto_install': False,
}
