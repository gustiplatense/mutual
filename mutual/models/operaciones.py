# -*- coding: utf-8 -*-
from odoo import models, fields

class MutualOperacion(models.Model):
    _name = 'mutual.operacion'
    _description = 'Operacion de Afiliado'

    afiliado_id = fields.Many2one('mutual.afiliado', string='Afiliado', required=True)
    comercio = fields.Many2one('res.partner', string='Comercio')
    ingreso = fields.Date(string='Fecha de Ingreso')
    aceptado = fields.Date(string='Fecha Aceptado')
    solicitud = fields.Integer(string='Numero de Solicitud')
    otorgado = fields.Monetary(string='Monto Otorgado')
    currency_id = fields.Many2one(
        'res.currency', string='Moneda',
        default=lambda self: self.env.company.currency_id
    )
    cantidad = fields.Integer(string='Cantidad')
    primera = fields.Date(string='Primera Cuota')
    ultima = fields.Date(string='Ultima Cuota')
    estado = fields.Selection(
        [('PENDIENTE','Pendiente'),
         ('APROBADO','Aprobado'),
         ('OTORGADO','Otorgado'),
         ('CANCELADO','Cancelado')],
        string='Estado'
    )
    comision = fields.Monetary(string='Comision', currency_field='currency_id')
    afiliado_id = fields.Many2one(
        'mutual.afiliado',
        string='Afiliado',
        required=True,
        ondelete='cascade'
    )