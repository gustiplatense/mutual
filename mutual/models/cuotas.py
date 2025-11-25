# -*- coding: utf-8 -*-
from odoo import models, fields

class MutualCuota(models.Model):
    _name = 'mutual.cuota'
    _description = 'Cuota de Operacion'

    operacion_id = fields.Many2one('mutual.operacion', string='Operacion', required=True)
    cuota = fields.Integer(string='Numero de Cuota')
    detalle = fields.Char(string='Detalle')
    fecha = fields.Date(string='Fecha')
    estado = fields.Selection(
        [('PENDIENTE','Pendiente'),
         ('LIQUIDADO','Liquidado'),
         ('CANCELADO','Cancelado')],
        string='Estado'
    )