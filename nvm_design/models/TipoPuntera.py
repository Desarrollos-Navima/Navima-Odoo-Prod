# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TipoPuntera(models.Model):
    _name = 'tipopuntera'
    _description = 'Tipos de punteras utilizados en Navima'

    name = fields.Char('Nombre')
    display_name = fields.Char('Nombre')

    @api.onchange('name')
    def _onchange_name(self):
        self.display_name = self.name