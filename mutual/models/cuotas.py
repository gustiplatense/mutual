# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MutualCuota(models.Model):
    _name = 'mutual.cuota'
    _description = 'Cuota de Operacion'

    operacion_id = fields.Many2one('mutual.operacion', string='Operacion')
    credito_id = fields.Many2one('mutual.credito', string='Credito', ondelete='set null')
    registro = fields.Integer(string='Registro', readonly=True, index=True)

    # Campos mapeados desde la "ficha" (SQL)
    comercio = fields.Integer(string='Comercio')
    documento = fields.Integer(string='Documento')
    fecha = fields.Date(string='Fecha')
    fecha_original = fields.Date(string='Fecha Original')
    fecha_venc = fields.Date(string='Fecha Vencimiento')
    solicitud = fields.Integer(string='Solicitud')                # nro de credito/solicitud en la fuente
    detalle = fields.Char(string='Detalle', size=30)

    debe = fields.Float(string='Debe', digits=(18, 2))
    haber = fields.Float(string='Haber', digits=(18, 2))
    saldo = fields.Float(string='Saldo', digits=(18, 2))

    afiliado_num = fields.Integer(string='Nro Afiliado')
    afiliado_id = fields.Many2one('mutual.afiliado', string='Afiliado')
    empleador_num = fields.Char(string='Nro Empleador')
    empleador_id = fields.Many2one('res.partner', string='Empleador')

    cpura = fields.Float(string='Cpura', digits=(18, 2))
    interes = fields.Float(string='Interes', digits=(18, 2))
    creditos = fields.Float(string='Creditos', digits=(18, 2))
    gastos = fields.Float(string='Gastos', digits=(18, 2))
    turismo = fields.Float(string='Turismo', digits=(18, 2))
    salud = fields.Float(string='Salud', digits=(18, 2))

    cancelada = fields.Char(string='Cancelada', size=1)
    cancelada_bool = fields.Boolean(string='Cancelada (bool)', compute='_compute_cancelada_bool', store=True)

    cuota = fields.Integer(string='Numero de Cuota')
    autorizada = fields.Boolean(string='Autorizada')

    estado = fields.Selection(
        [('PENDIENTE', 'Pendiente'),
         ('LIQUIDADO', 'Liquidado'),
         ('CANCELADO', 'Cancelado')],
        string='Estado',
        default='PENDIENTE'
    )

    _sql_constraints = [
        ('registro_uniq', 'unique(registro)', 'El campo registro debe ser unico.'),
    ]

    @api.depends('cancelada')
    def _compute_cancelada_bool(self):
        for rec in self:
            rec.cancelada_bool = bool(rec.cancelada and rec.cancelada.strip() and rec.cancelada.upper() not in ('0', 'N', 'F', 'FALSE'))

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

    @api.onchange('solicitud', 'documento')
    def _onchange_solicitud_documento(self):
        """Intentar vincular la cuota al credito importado por solicitud+documento."""
        if self.solicitud and self.documento:
            credito = self.env['mutual.credito'].search([
                ('solicitud', '=', int(self.solicitud)),
                ('documento', '=', int(self.documento))
            ], limit=1)
            if credito:
                self.credito_id = credito.id

    def name_get(self):
        res = []
        for rec in self:
            name = f"{rec.registro or ''} - {rec.afiliado_num or ''} - {rec.solicitud or ''} - Cuota {rec.cuota or ''}"
            res.append((rec.id, name))
        return res