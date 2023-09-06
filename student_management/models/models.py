# -*- coding: utf-8 -*-
from odoo import api, fields, models , _
from odoo.exceptions import ValidationError


class resPartner(models.Model):
    _inherit = 'res.partner'

    is_student  = fields.Boolean(string='Is Student')
    birth_date = fields.Date(string='Birthdate')
    

class resPartner(models.Model):
    _inherit = 'account.move'

    registration_id  = fields.Many2one(comodel_name='student.registration',string='Registration' )
