# -*- coding: utf-8 -*-
{
    'name': "User Roles Management",
    'version': '17.0.0.0',
    'author': "Salman Malik",
    'website': "https://ntww.com",
    'category': 'Human Resources',
    'summary': """User Roles Management""",
    'description': """
        Assign roles to users on one click
    """,

    'depends': ['base','contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'views/inherit_user_view.xml',
        # 'views/assets.xml',
        'data/data.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,

}
