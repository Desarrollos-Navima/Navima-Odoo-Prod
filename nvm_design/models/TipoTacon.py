# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TipoTacon(models.Model):
    _name = 'tipotacon'
    _description = 'Tipos de tacón utilizados en Navima'

    name = fields.Char('Nombre')
    display_name = fields.Char('Nombre')

    @api.onchange('name')
    def _onchange_display_name(self):
        self.display_name = self.name
