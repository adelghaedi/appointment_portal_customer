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
        'security/ir.model.access.csv',
        'views/portal_template.xml',
    ],
    'installable': True,
    'application': False,
}