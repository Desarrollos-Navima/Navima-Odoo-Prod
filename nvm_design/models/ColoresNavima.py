# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ColoresNavima(models.Model):
    _name = 'coloresnnavima'
    _description = 'Colores utilizados en las colecciones'

    display_name = fields.Char('Color')
    name = fields.Char('Color')

    @api.onchange('display_name')
    def _onchange_display_name(self):
        self.name = self.display_name

    proveedor = fields.Many2one('gruposcolores', 'Grupos Colores')
    codigo_color_old = fields.Char('Codigo Color')
    cod_rgb = fields.Char('Cod. RGB')