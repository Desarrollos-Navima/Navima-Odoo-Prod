# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MaterialPorcentaje(models.Model):
    _name = 'materialporcentaje'
    _description = 'Es la indexación entre cualquier modelo y los materiales añadiendo un porcentaje de presencia en la formación del elemento que relacione cualquier modelo'

    material = fields.Many2one('materiales.materiales', 'Material', required=True)
    porcentaje_presencia = fields.Char('Porcentaje de presencia')
    int_ext = fields.Selection([('int', 'Interior'), ('ext', 'Exterior')], '¿Interior o exterior?')

    @api.onchange('material')
    def _onchange_material(self):
        self.display_name = self.material.display_name
    