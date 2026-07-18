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

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from logging import getLogger
_logger = getLogger(__name__)



class InsysUserType(models.Model):
    _name = 'insys.user.type'
    _description = "Insys User Type"
    _rec_name = 'name'


    name= fields.Char(string="Name")
    description = fields.Text(string="Description")
    company_id = fields.Many2one('res.company',string='Company',default=lambda self: self.env.company.id)




class InsysUserAccess(models.Model):
    _name = 'insys.user.access'
    _description = 'Insys User Access'
    _rec_name = 'user_access_type'

    def _exlude_category_user_type_domain(self):
        user_types_category = self.env.ref('base.module_category_user_type', raise_if_not_found=False)
        return [('category_id','!=',user_types_category.id)]



    user_access_type = fields.Many2one(comodel_name="insys.user.type",string="User Access Type")
    # module_category = fields.Many2one('ir.module.category',string="Module Category")
    user_groups = fields.Many2many('res.groups',string="Groups",domain=_exlude_category_user_type_domain)
    company_id = fields.Many2one('res.company',string='Company',default=lambda self: self.env.company.id)

    
    def name_get(self):
        result = [(rec.id,rec.user_access_type.name) for rec in self]
        return result

    @api.constrains('user_access_type')
    def user_group_change(self):
        user_access_type_id = self.user_access_type.id
        insys_user_access_recs = self.env['insys.user.access'].search([('id','!=',self.id),('user_access_type','=',user_access_type_id)])
        if insys_user_access_recs:
            raise ValidationError('User Access type should be unique!')
                

    def write(self,vals):
        """Override the write function for the add or remove the user from the groups"""
        groups_id = vals.get('user_groups')
        if groups_id:
            groups_dict = {'added_groups':[],'removed_groups':[]}
            for group in groups_id:
                if group[0]==4:
                    groups_dict['added_groups'].append(group[1])
                elif group[0]==3:
                    groups_dict['removed_groups'].append(group[1])
            users = self.env['res.users'].search([('res_user_access','=',self.id)])
            if users:
                if added_groups:=groups_dict.get('added_groups'):
                    added_groups_id = self.env['res.groups'].browse(added_groups)
                    added_groups_id.write({'users':[(4,user.id) for user in users]})

                if removed_groups:=groups_dict.get('removed_groups'):
                    removed_group_ids =  self.env['res.groups'].browse(removed_groups)
                    removed_group_ids.write({'users':[(3,user.id) for user in users]})
        return super().write(vals)



class InheritResUsers(models.Model):
    _inherit = "res.users"

    def _get_company_domain(self):
        return [('company_id','=',self.company_id.id)]

    res_user_access = fields.Many2one('insys.user.access',string="User Role")

    
    def _get_exclude_groups(self):
        user_types_category = self.env.ref('base.module_category_user_type').id
        user_hidden_category = self.env.ref('base.module_category_hidden').id
        return (user_types_category,user_hidden_category)

    def group_user_add_remove(self,user_access):
        insys_user_access = self.env['insys.user.access']
        exclude_groups = self._get_exclude_groups()
        old_group_ids = self.env['res.groups'].search([('category_id','not in', exclude_groups)]).filtered(lambda group: self.id in group.users.ids)
        new_user_access = insys_user_access.search([('id','=',user_access)],limit=1)
        if not new_user_access.user_groups:
            raise ValidationError('Please define groups inside the user role.')
        new_group_ids = new_user_access.user_groups
        old_group_ids.write({'users':[(3,self.id)]})
        new_group_ids.write({'users': [(4,self.id)]})
        return True
           
    @api.model
    def create(self,vals):
        """ Override the Create function for the add the user in the group on the basis of the Insys User Type access"""
        res = super().create(vals)
        insys_user_access = vals.get('res_user_access')
        if insys_user_access:
            access_type = self.env['insys.user.access'].search([('id','=',insys_user_access)],limit=1)
            group_ids = access_type.user_groups
            group_ids.write({'users':[(4,res.id)]})
        return res
    
    def write(self,vals):
        """ Override the Write function to update current insys user access"""
        user_access = vals.get('res_user_access')
        if user_access:
            self.group_user_add_remove(user_access)
        return super().write(vals)
    
    @api.model
    def check_user_group(self):
        admin_group = self.user_has_groups('base.group_system')
        return admin_group
            