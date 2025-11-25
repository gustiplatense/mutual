# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MutualAfiliado(models.Model):
    _name = 'mutual.afiliado'
    _description = 'Afiliado'
    _rec_name = 'afiliado'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Esto activa el chatter


    afiliado = fields.Integer(string='Nro de Afiliado',required=True,copy=False,readonly=True,index=True,default=0)

    legajo = fields.Char(string='Legajo', required=True, tracking=True)
    nombre = fields.Char(string='Nombre', required=True, tracking=True)
    nacioel = fields.Date(string='Fecha de Nacimiento', tracking=True)
    nacional = fields.Many2one('res.country', string='Nacionalidad', tracking=True)
    tipo = fields.Char(string='Tipo')
    dni = fields.Integer(string='DNI', tracking=True)
    domicilio = fields.Char(string='Domicilio', tracking=True)
    localidad = fields.Char(string='Localidad', tracking=True)
    telefono = fields.Char(string='Telefono', tracking=True)
    movil = fields.Char(string='Movil')
    email = fields.Char(string='Email', tracking=True)
    cuil = fields.Char(string='CUIL', tracking=True)
    postal = fields.Char(string='Codigo Postal')
    civil = fields.Selection(
        [('SOLTERO','Soltero'),
         ('CASADO','Casado'),
         ('DIVORCIADO','Divorciado'),
         ('VIUDO','Viudo'),
         ('CONCUBINO','Concubino')],
        string='Estado Civil'
    )
    ingreso = fields.Date(string='Fecha de Ingreso')
    empleador = fields.Many2one('res.partner', string='Empleador', tracking=True)
    fecha_alta = fields.Date(string='Fecha de Alta', tracking=True)
    fecha_baja = fields.Date(string='Fecha de Baja', tracking=True)
    obs = fields.Text(string='Observaciones', tracking=True)
    foto = fields.Binary(string='Foto')
    familiar_ids = fields.One2many(
        'mutual.familiar',   # modelo hijo
        'afiliado_id',       # campo Many2one en el hijo
        string='Familiares'
    )
    operacion_ids = fields.One2many(
        'mutual.operacion',   # modelo destino
        'afiliado_id',        # campo Many2one en mutual.operacion
        string='Creditos'
    )

    def action_add_operacion(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Agregar Operacion',
            'res_model': 'mutual.operacion',
            'view_mode': 'form',
            'context': {'default_afiliado_id': self.id},
            'target': 'current',
            }

    def action_add_familiar(self):
        """Abre el formulario de alta de Familiar con el afiliado ya preseleccionado"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Agregar Familiar',
            'res_model': 'mutual.familiar',
            'view_mode': 'form',
            'context': {'default_afiliado_id': self.id},
            'target': 'current',
            }
    def name_get(self):
        result = []
        for record in self:
            # Mostramos: N°Afiliado - Nombre
            name = f"{record.afiliado} - {record.nombre or ''}"
            result.append((record.id, name))
        return result

   # @api.model_create_multi
   # def create(self, vals_list):
   #     for vals in vals_list:
   #         if not vals.get('afiliado'):
   #             seq = self.env['ir.sequence'].next_by_code('afiliado.afiliado')
   #             vals['afiliado'] = int(seq) if seq and seq.isdigit() else 0
   #     return super().create(vals_list)

    @api.model
    def create(self, vals):
        if not vals.get('afiliado'):
            seq = self.env['ir.sequence'].next_by_code('afiliado.afiliado')
            vals['afiliado'] = int(seq) if seq and seq.isdigit() else 0
        return super().create(vals)





