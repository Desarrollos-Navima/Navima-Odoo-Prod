# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AgentesNavima(models.Model):
    _name = 'agentes.navima'
    _description = 'Agentes de Navima'

    name = fields.Char('Nombre Agente')
    display_name = fields.Char('Nombre Agente Label')
    shortdesc = fields.Char('Apodo')
    vip_lola = fields.Boolean('VIP Lola Cruz?')
    vip_bibi = fields.Boolean('VIP Bibi Lou?')
    all_lola = fields.Boolean('ALL Lola Cruz?')
    all_bibi = fields.Boolean('ALL Bibi Lou?')

    @api.onchange('display_name')
    def _onchange_display_name(self):
        self.name = self.display_name