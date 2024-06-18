# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class PartnerRisks(models.Model):

    _inherit = 'res.partner'

    cod_proveedor_nvm = fields.Char('Codigo Proveedor')

    asegurado = fields.Boolean('Asegurado?')
    moroso = fields.Boolean('Moroso?')
    
    cantidad_concesion = fields.Float('Cantidad concesión', help="Cantidad concedida para la cobertura.")
    cantidad_propuesta = fields.Float('Cantidad propuesta', help="Cantidad propuesta para la cobertura.")
    cantidad_validacion = fields.Float('Cantidad validación', help="Cantidad validada para la cobertura.")

    fecha_cancelacion = fields.Date('Fecha de cancelación', help="Fecha en la que se cancela la cobertura del riesgo.")
    fecha_concesion = fields.Date('Fecha de concesión', help="Fecha en la que se concede la cobertura del riesgo.")
    fecha_propuesta = fields.Date('Fecha propuesta', help="Fecha en la que se hace la propuesta para la cobertura del riesgo.")
    fecha_validacion = fields.Date('Fecha de validación', help="Fecha en la que se valida la cobertura del riesgo.")

    poliza = fields.Char("Nº de póliza")
    referencia_proveedor = fields.Char("Referencia proveedor", help="Referencia que asigna el proveedor de la póliza.")
    antiguo_codigo_cliente = fields.Char("Antiguo código de cliente")

    empresa_riesgo = fields.Many2one('res.partner', 'Empresa de riesgo')
    metodo_de_pago = fields.Many2one('account.payment.method', 'Método de pago')

    comentario_riego = fields.Text('Comentario')