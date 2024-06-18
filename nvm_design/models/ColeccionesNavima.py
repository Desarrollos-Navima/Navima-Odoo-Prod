# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ColeccionesNavima(models.Model):
    _name = 'colecciones.colecciones'
    _description = 'Modelo de las colecciones de navima'

    name = fields.Char('Colección')
    temporada = fields.Char('Temporada')
    logo_marca = fields.Binary('Logo')
    marca_nvm = fields.Many2one('marcasnavima', 'Marca')
    agentes_autorizados_nvm = fields.Many2many('res.partner', string="Agentes autorizados")

    # PRECIOS

    cash_conversion = fields.Many2one('cash.conversion', 'Conversion moneda')

    multiplicador_aranceles = fields.Float('Multiplicador aranceles', default=1.15)

    multiplicador = fields.Float('Multiplicador Precio', default=2.5)
    multiplicador_it = fields.Float('Multiplicador IT', default=2.6)
    multiplicador_usa = fields.Float('Multiplicador USA', default=2.7)

    multiplicador_pvr = fields.Float('Multiplicador PVR', default=2.5)
    multiplicador_usa_pvr = fields.Float('Multiplicador PVR USA', default=2.7)
    multiplicador_fob = fields.Float('Multiplicador F.O.B', default=1.8)

    # FIN PRECIOS

    # TARIFAS

    tarifa = fields.Many2one('product.pricelist', 'Tarifa EUR')
    tarifa_usd = fields.Many2one('product.pricelist', 'Tarifa USD')

    tarifa_fob = fields.Many2one('product.pricelist', 'Tarifa F.O.B')

    tarifa_wholesalers = fields.Many2one('product.pricelist', 'Tarifa EUR')
    tarifa_wholesalers_usd = fields.Many2one('product.pricelist', 'Tarifa USD')



    # FIN TARIFAS

    @api.onchange('temporada', 'marca_nvm')
    def _onchange_temporada_marca(self):
        marca = self.env['marcasnavima'].browse(self.marca_nvm.id)
        self.name = str(self.temporada) + '-' + str(marca.name)
        self.display_name = self.name
