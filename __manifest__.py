# Copyright 2020 Pafnow
{
    'name': 'BOM Component Consumption Type',
    'version': '13.0.1.0.0',
    'depends': ['mrp', 'product'],
    'author': 'Pafnow',
    'category': 'MRP',
    'description': 'Add consumption type in BOM lines to define component consumption type (fixed, variable, formula)',
    'data': [
        'views/mrp_bom_views.xml',
    ],
    'installable': True,
    'application': False,
}
