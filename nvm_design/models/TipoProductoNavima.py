# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TipoProductoNavima(models.Model):
    _name = 'tipo.producto'
    _description = 'Tipos de producto que se usa en los materiales'

    name = fields.Char('Nombre')
    display_name = fields.Char('Nombre')
    descripcion = fields.Char('Descripción', required=True)
    multiplo_precio = fields.Float('Multiplo Precio', required=True)

    @api.onchange('name')
    def _onchange_name(self):
        self.display_name = self.name