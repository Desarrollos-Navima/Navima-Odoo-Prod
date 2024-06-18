# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MaterialesNavima(models.Model):
    _name = 'materiales.materiales'
    _description = 'Materiales que se utilizan en las colecciones'

    material = fields.Char('Material')
    name = fields.Char('Material')
    display_name = fields.Char('Material')
    cod_material = fields.Char('Cod. Material')

    tipo_de_producto = fields.Many2one('tipo.producto', string='Tipo de producto')

    @api.onchange('name')
    def _onchange_material(self):
        self.material = self.name
        self.display_name = self.name