# -*- coding: utf-8 -*-

from odoo import api, fields, tools, models, _

class ResPartnerDetailed(models.Model):

    _inherit = 'res.partner'

    agente_nvm = fields.Many2one('agentes.navima', string='Agente')
