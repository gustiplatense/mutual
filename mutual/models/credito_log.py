from odoo import models, fields

class CreditoLog(models.Model):
    _name = 'mutual.credito.log'
    _description = 'Log de Creditos Omitidos'

    linea_original = fields.Text(string='Linea TXT')
    motivo = fields.Char(string='Motivo del rechazo')
    fecha_log = fields.Datetime(string='Fecha', default=fields.Datetime.now)
    archivo_origen = fields.Char(string='Archivo TXT')