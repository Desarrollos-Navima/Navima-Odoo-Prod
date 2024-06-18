# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HSMaster(models.Model):
    _name = 'hs.master'
    _description = 'Codigos aduaneros'

    display_name = fields.Char('HS Code')
    name = fields.Char('HS Code')

    descripcion = fields.Char('Descripción')

    @api.onchange('display_name')
    def _onchange_display_name(self):
        self.name = self.display_name