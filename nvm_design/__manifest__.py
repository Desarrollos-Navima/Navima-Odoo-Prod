# -*- coding: utf-8 -*-
################################################################################
#
#    Franco De Paulis (franco@upperstechnologies.com).
#
################################################################################
{
    'name': 'Diseño',
    'version': '17.0',
    'summary': 'Aplicación desarrollada para gestionar el departamento de diseño de una empresa de calzados.',
    'description': 'Gestión del departamento de diseño.',
    'category': 'Operations/Design',
    'sequence': 10,
    'author': 'Franco De Paulis Camacho',
    'company': 'Franco De Paulis Camacho',
    'maintainer': 'Franco De Paulis Camacho',
    'website': 'https://www.upperstechnologies.com',
    'depends': ['base', 'mail', 'product', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/design_views.xml',
        'views/carta_colores_form_view.xml',
        'views/mail_activity_views.xml',
        'views/templates.xml',
        'data/design_data.xml'
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
