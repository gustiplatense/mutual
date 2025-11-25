from odoo import models, fields
import base64
import io
import datetime

class CreditoImportador(models.TransientModel):
    _name = 'mutual.credito.importador'
    _description = 'Importador de Creditos desde TXT'

    archivo_txt = fields.Binary(string='Archivo TXT', required=True)
    nombre_archivo = fields.Char(string='Nombre del archivo')

    def importar_creditos(self):
        contenido = base64.b64decode(self.archivo_txt or b'')
        archivo = io.StringIO(contenido.decode('utf-8', errors='ignore'))

        contador = 0
        omitidos = 0
        errores = 0

        for linea in archivo:
            partes = linea.strip().split(';')
            if len(partes) != 12:
                errores += 1
                self.env['mutual.credito.log'].create({
                    'linea_original': linea.strip(),
                    'motivo': 'Formato invalido',
                    'archivo_origen': self.nombre_archivo,
                })
                continue

            try:
                fecha = datetime.datetime.strptime(partes[0], '%d/%m/%Y').date()
                tipo_credito = partes[1]
                dni = partes[2]
                nro_credito = partes[3]
                cant_cuotas = int(partes[4])
                cuota_actual = int(partes[5])
                monto = float(f"{partes[6]}.{partes[7]}")
                monto_solicitado = float(f"{partes[8]}.{partes[9]}")
                nro_fijo = partes[10].strip().lower() in ['si', 'true', '1']
                comercio = partes[11]

                afiliado = self.env['mutual.afiliado'].search([('dni', '=', dni)], limit=1)
                if not afiliado:
                    errores += 1
                    self.env['mutual.credito.log'].create({
                        'linea_original': linea.strip(),
                        'motivo': 'DNI no Existe',
                        'archivo_origen': self.nombre_archivo,
                    })
                    continue

                existe = self.env['mutual.credito'].search([
                    ('dni', '=', dni),
                    ('nro_credito', '=', nro_credito),
                    ('cuota_actual', '=', cuota_actual)
                ], limit=1)

                if existe:
                    omitidos += 1
                    self.env['mutual.credito.log'].create({
                        'linea_original': linea.strip(),
                        'motivo': 'Duplicado',
                        'archivo_origen': self.nombre_archivo,
                    })
                    continue

                self.env['mutual.credito'].create({
                    'fecha': fecha,
                    'tipo_credito': tipo_credito,
                    'dni': dni,
                    'nro_credito': nro_credito,
                    'cant_cuotas': cant_cuotas,
                    'cuota_actual': cuota_actual,
                    'monto': monto,
                    'monto_solicitado': monto_solicitado,
                    'nro_fijo': nro_fijo,
                    'comercio': comercio,
                    'afiliado_id': afiliado.id,
                })
                contador += 1

            except Exception as e:
                errores += 1
                self.env['mutual.credito.log'].create({
                    'linea_original': linea.strip(),
                    'motivo': f'Error: {str(e)}',
                    'archivo_origen': self.nombre_archivo,
                })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Importacion finalizada',
                'message': f'{contador} creditos importados. {omitidos} duplicados. {errores} rechazados.',
                'type': 'success',
                'sticky': False,
            }
        }