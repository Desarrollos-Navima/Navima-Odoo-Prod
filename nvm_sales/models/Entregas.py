# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Entregas(models.Model):

    _inherit = 'sale.order'

    entregar_desde = fields.Date('Entregar desde', help="Fecha desde la que se puede entregar el pedido al cliente.")
    entregar_hasta = fields.Date('Entregar hasta', help="Fecha hasta la que se puede entregar el pedido al cliente.")

    asumo_riesgo = fields.Boolean('Asumo el riesgo')

    agente_nvm = fields.Many2one('agentes.navima', string='Agente')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        
        self.agente_nvm = self.partner_id.agente_nvm.id