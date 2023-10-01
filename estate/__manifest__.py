{

    'name': "Real-Estate Management",

    'version': '1.0',

    'depends': ['base'],

    'author': "Waleed",

    'category': 'Category',

    'description': """

  This is a module of Real-Estate Management!

  """,

    # data files always loaded at installation

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menu.xml',
        'views/estate_type_menu.xml'
    ],

    'installable': True,

    'auto_install': False,

    'application': True,

}
