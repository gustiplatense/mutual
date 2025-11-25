# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    id_empresa = fields.Char(string='ID Empresa')
    #activa = fields.Boolean(string='Activa', default=False)