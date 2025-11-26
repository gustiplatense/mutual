# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Credito(models.Model):
    _name = 'mutual.credito'
    _description = 'Credito / Operacion (operaciones)'

    # Identificadores y trazas
    registro = fields.Integer(string='Registro', readonly=True, index=True)
    comercio = fields.Integer(string='Comercio')
    columna = fields.Integer(string='Columna')
    timestamp_column = fields.Char(string='Timestamp')  # SQL timestamp/rowversion guardado como string

    # Fechas
    ingreso = fields.Date(string='Fecha Ingreso')
    aceptado = fields.Date(string='Fecha Aceptado')
    primera = fields.Date(string='Primera Cuota')
    ultima = fields.Date(string='Ultima Cuota')
    ult_pago = fields.Date(string='Ultimo Pago')
    fec_baja = fields.Date(string='Fecha Baja')

    # Identificación / referencia
    solicitud = fields.Integer(string='Solicitud')
    nro_credito = fields.Char(string='Nro Credito', compute='_compute_nro_credito', store=True)
    documento = fields.Integer(string='Documento')
    legajo = fields.Char(string='Legajo', size=10)
    nombre = fields.Char(string='Nombre', size=50)

    # Montos y condiciones
    solicitado = fields.Float(string='Solicitado', digits=(18, 2))
    otorgado = fields.Float(string='Otorgado', digits=(18, 2))
    cuota = fields.Float(string='Importe Cuota', digits=(18, 2))
    cantidad = fields.Integer(string='Cantidad de Cuotas')
    pedida = fields.Integer(string='Pedida')
    pagada = fields.Integer(string='Pagada')
    comision = fields.Float(string='Comision', digits=(18, 2))

    # Estados / flags / observaciones
    cancelado = fields.Char(string='Cancelado', size=1)
    arreglado = fields.Char(string='Arreglado', size=1)
    obs = fields.Char(string='Observaciones', size=100)
    detalle = fields.Text(string='Detalle')

    # Integracion con afiliado / empleador
    afiliado_num = fields.Integer(string='Nro Afiliado')
    afiliado_id = fields.Many2one('mutual.afiliado', string='Afiliado')
    nombre_afiliado = fields.Char(related='afiliado_id.nombre', string='Nombre Afiliado', store=True)

    empleador_id = fields.Many2one('res.partner', string='Empleador')
    empleador_num = fields.Char(string='Nro Empleador')
    empleador_nombre = fields.Char(string='Nombre Empleador', compute='_compute_empleador_nombre', store=True)

    # Relacion con cuotas
    cuota_ids = fields.One2many('mutual.cuota', 'credito_id', string='Cuotas')

    estado = fields.Selection(
        [('ACTIVO', 'Activo'),
         ('CANCELADO', 'Cancelado'),
         ('SUSPENDIDO', 'Suspendido')],
        string='Estado',
        default='ACTIVO'
    )

    _sql_constraints = [
        ('registro_uniq', 'unique(registro)', 'El campo registro debe ser unico.'),
    ]

    @api.depends('solicitud')
    def _compute_nro_credito(self):
        for rec in self:
            rec.nro_credito = str(rec.solicitud) if rec.solicitud else ''

    @api.depends('afiliado_id')
    def _compute_empleador_nombre(self):
        for rec in self:
            if rec.afiliado_id and rec.afiliado_id.empleador:
                rec.empleador_nombre = rec.afiliado_id.empleador.name
                if not rec.empleador_id:
                    rec.empleador_id = rec.afiliado_id.empleador.id
                    rec.empleador_num = rec.afiliado_id.empleador.id_empleador or ''
            else:
                rec.empleador_nombre = rec.empleador_id.name if rec.empleador_id else ''

    @api.onchange('afiliado_num')
    def _onchange_afiliado_num(self):
        if self.afiliado_num:
            af = self.env['mutual.afiliado'].search([('afiliado', '=', int(self.afiliado_num))], limit=1)
            if af:
                self.afiliado_id = af.id
                if af.empleador:
                    self.empleador_id = af.empleador.id
                    self.empleador_num = af.empleador.id_empleador or ''

    @api.onchange('afiliado_id')
    def _onchange_afiliado_id(self):
        if self.afiliado_id:
            self.afiliado_num = self.afiliado_id.afiliado or 0
            if self.afiliado_id.empleador:
                self.empleador_id = self.afiliado_id.empleador.id
                self.empleador_num = self.afiliado_id.empleador.id_empleador or ''

    def name_get(self):
        res = []
        for r in self:
            label = f"{r.solicitud or r.nro_credito or ''} - {r.nombre or r.nombre_afiliado or ''}"
            res.append((r.id, label))
        return res