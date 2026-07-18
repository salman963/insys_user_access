# -*- coding: utf-8 -*-
################################################################################
#
#    Copyright (C) 2026-TODAY Salman Malik
#
#    Author: Salman Malik
#    Email: salmanmalik9475@gmail.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License (LGPL-3)
#    as published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/>.
#
################################################################################

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
