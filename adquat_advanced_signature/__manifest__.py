# -*- coding: utf-8 -*-
############################################################################################
#
#    ADQUAT - AJOUTE UN CHAMP DATE POUR CHOISIR LA DATE A LAQUELLE A ETE REALISE L'INVENTAIRE
#
############################################################################################


{
    'name': 'Adquat Advanced Signature',
    'version': '0.1',
    'category': 'Tools',
    'description': """
    Ajouts divers
""",
    'author': 'Adquat-solutions',
    'website': 'http://www.adquat.com',
    'depends': ['base','product','stock','sale','sale_project'],
    'data': [],
    'demo': [],
    'update_xml': [
        #'security/ir.model.access.csv',
        'models_view.xml',
        #'wizard/stock_change_product_price_view.xml',
        #'wizard/stock_change_product_qty_view.xml',
    ],
    'test':[],
    'installable': True,
    'images': [],
}