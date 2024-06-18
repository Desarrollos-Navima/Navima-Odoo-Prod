# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AlturasNavima(models.Model):
    _name = 'alturas'
    _description = 'Las diferetes alturas que se usan en navima para bocetos y productos en centímetros'

    name = fields.Char('Altura (cm)')
    display_name = fields.Char('Altura (cm)')

    @api.depends('name')
    def _depends_display_name(self):
        self.display_name = self.name
