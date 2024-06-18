# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CashConversion(models.Model):
    _name = 'cash.conversion'
    _description = 'Modelo que se utiliza para la conversion de monedas'

    name = fields.Char('Nombre de Conversión')

    moneda_a_convertir_id = fields.Many2one('res.currency', string='Moneda a convertir')
    multiplo_a_convertir = fields.Float('Valor de moneda a converir')

    moneda_de_conversion_id = fields.Many2one('res.currency', string='Moneda de conversión')
    multiplo_conversion = fields.Float('Multiplo de la mondeda de conversión')

    temporada = fields.Char('Temporada')
    marca = fields.Many2one('marcasnavima', 'Marca', required=True)

    @api.onchange('moneda_a_convertir_id', 'moneda_de_conversion_id', 'temporada', 'marca')
    def _onchange_name(self):

        if self.moneda_a_convertir_id and self.moneda_de_conversion_id:

            nombre = str(self.temporada) + "-" + str(self.marca.name) + " " + str(self.moneda_a_convertir_id.name) + " - " + str(self.moneda_de_conversion_id.name)
            self.name = nombre