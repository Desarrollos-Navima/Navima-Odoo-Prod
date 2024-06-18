# -*- coding: utf-8 -*-
# Desarrollado por franco@upperstechnologies.com

{
    'name': 'Ventas Navima',
    'version': '1.0',
    'shortdesc': 'Ventas Navima',
    'author': 'Franco De Paulis Camacho',
    'license': 'LGPL-3',
    'sequence': 130,
    'category': 'Operations/Sales',
    'description': """Añade las fehcas de entrea en el presupuesto""",
    'depends': ['sale_management', 'risks', 'purchase_product_matrix', 'web'],
    'summary': 'Añade las fehcas de entrea en el presupuesto',
    'website': '',
    'data': [
        'views/templates.xml',
    ],
    'css': [
        'static/scss/colores.scss',
    ],
    'js': [
        'static/js/color_set.js',
    ],
    'assets': {
        'web.assets_backend': [
            'nvm_sales/static/js/color_set.js',
        ],
    },
    'installable': True,
    'application': True,
}
