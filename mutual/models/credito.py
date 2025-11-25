from odoo import models, fields, api

class Credito(models.Model):
    _name = 'mutual.credito'
    _description = 'Credito Importado'

    fecha = fields.Date(string='Fecha')
    tipo_credito = fields.Char(string='Tipo de Credito')
    dni = fields.Char(string='DNI')
    nro_credito = fields.Char(string='Nro Credito')
    cuota_actual = fields.Integer(string='Cuota Actual')
    cant_cuotas = fields.Integer(string='Cantidad de Cuotas')
    monto = fields.Float(string='Monto')
    monto_solicitado = fields.Float(string='Monto Solicitado')
    nro_fijo = fields.Boolean(string='Numero Fijo')
    comercio = fields.Char(string='Comercio')

    afiliado_id = fields.Many2one('mutual.afiliado', string='Afiliado')
    nombre_afiliado = fields.Char(related='afiliado_id.nombre', store=True)
    #empleador_afiliado = fields.Char(related='afiliado_id.empleador', store=True)
    empleador_afiliado = fields.Many2one('res.partner',string='Empleador',related='afiliado_id.empleador',store=True)

    _sql_constraints = [
        ('credito_unico', 'unique(dni, nro_credito, cuota_actual)', 'Este credito ya fue importado.')
    ]
    empleador_nombre = fields.Char(string='Nombre del Empleador',compute='_compute_empleador_nombre',store=True)
    
    @api.depends('afiliado_id.empleador')
    def _compute_empleador_nombre(self):
        for record in self:
            record.empleador_nombre = record.afiliado_id.empleador.name if record.afiliado_id.empleador else ''