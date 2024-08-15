# -*- coding: utf-8 -*-
{
    'name': "POS Margin Sale",

    'summary': "Ensure products are sold above their minimum price with margin checks in POS and sale orders.",

    'description': """
        The POS Margin Sale module calculates and enforces the minimum sale price and profit margin for each product. 
        When a user attempts to sell a product below its minimum price in either a sale order or a POS order, 
        the system triggers a warning, helping businesses maintain profitability and prevent underpricing.
    """,

    'author': "Doodex",
    'website': "https://www.doodex.net",

    'category': 'Point of Sale',
    'version': '16.0.1.0',

    'depends': ['base', 'point_of_sale', 'product', 'sale', 'stock_account'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_confirmation.xml',
        'wizard/wizard_margin_product.xml',
        'views/res_config_settings.xml',
        'views/products.xml',
        'views/sale_order.xml',
    ],

    'assets': {
        'point_of_sale.assets': [
            'pos_margin_sale/static/src/**/*.js',
            'pos_margin_sale/static/src/**/*.xml',
            'pos_margin_sale/static/src/**/*.scss',
        ]
    },

    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}
