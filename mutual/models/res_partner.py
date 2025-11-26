# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    id_empresa = fields.Char(string='ID Empresa')
    es_empleador = fields.Boolean(
        string='Empresa empleadora asociada',
        default=False,
        help='Marcar si es una empresa empleadora asociada a la mutual para recibir liquidaciones.'
    )
    id_empleador = fields.Char(
        string='ID Empleador',
        help='Numero identificador del empleador utilizado por la mutual.'
    )