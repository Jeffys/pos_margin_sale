# -*- coding: utf-8 -*-
{
    'name': "POS Margin Threshold",

    'summary': "Ensure products are sold above their minimum price with margin checks in POS orders.",

    'description': """
        The POS Margin Sale module calculates and enforces the minimum sale price and profit margin for each product. 
        When a user attempts to sell a product below its minimum price in either a sale order or a POS order, 
        the system triggers a warning, helping businesses maintain profitability and prevent underpricing.
    """,

    'author': "Doodex",
    'website': "https://www.doodex.net",
    'license': "AGPL-3",
    'category': 'Point of Sale',
    'version': '18.0.1.0',

    'depends': [
        'base', 
        'point_of_sale', 
        'product', 
        'stock_account'
    ],

    'data': [
        'security/ir.model.access.csv',          
        'views/res_config_settings.xml',         
        'views/products.xml',                           
        'wizard/wizard_margin_product.xml',      
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            'pos_margin_threshold/static/src/**/*',
        ],
        'web.assets_tests': [
            'pos_margin_threshold/static/tests/tours/**/*',
        ],
    },

    'demo': [
        'demo/demo.xml',                    
    ],
    'application': True,
    'installable': True,
    'images': [
       'static/description/banner.gif',
       'static/description/icon.png',
    ],
}
