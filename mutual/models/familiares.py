# -*- coding: utf-8 -*-
from odoo import models, fields

class MutualFamiliar(models.Model):
    _name = 'mutual.familiar'
    _description = 'Familiar de Afiliado'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Esto activa el chatter

    id_externo = fields.Char(string='ID Externo') # se utiliza para integracion con otros sistemas
    afiliado_id = fields.Many2one('mutual.afiliado',string='Afiliado',required=True,ondelete='cascade', tracking=True)
    nombre = fields.Char(string='Nombre', required=True, tracking=True)
    nacioel = fields.Date(string='Fecha de Nacimiento', tracking=True)
    nacional = fields.Many2one('res.country', string='Nacionalidad', tracking=True)
    tipo = fields.Char(string='Tipo')
    dni = fields.Integer(string='DNI', tracking=True)
    parentesco = fields.Selection(
        [('HIJO','Hijo'),
         ('HIJASTRO','Hijastro'),
         ('ESPOSO','Esposo'),
         ('ESPOSA','Esposa'),
         ('Flia.Cargo','Familiar a Cargo'),
         ('HIJA','Hija'),
         ('MADRE','Madre'),
         ('PADRE','Padre'),
         ('NIETO','Nieto'),
         ('CONCUBINA','Concubina')],
        string='Parentesco'
    )
    obs = fields.Text(string='Observaciones', tracking=True)
    foto = fields.Binary(string='Foto')
