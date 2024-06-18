# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MuestrasNavima(models.Model):
    _name = 'muestras.navima'
    _description = 'Muestras que se piden para los agentes'

    name = fields.Char('Muestra')
    agente_de_venta = fields.Many2one('agentes.navima')
    colores_muestra_nvm = fields.Many2many('coloresnnavima', 'colores_muestras', string="Colores")
    diseno_id = fields.Many2one('nvm_design.request')


class MuestrasNavimaColor(models.Model):
    _name = 'muestras.navima.color'
    _description = 'Muestras unitarias'

    name = fields.Char('Muestra')
    colores_muestra_nvm = fields.Many2one('coloresnnavima', string="Color")
    agente_de_venta = fields.Many2many('agentes.navima', 'agentes_muestras', string="Agentes")
    diseno_id = fields.Many2one('nvm_design.request')
    imagen = fields.Binary("Imagen")

    def set_vip_agents(self):

        boceto = self.env['nvm_design.request'].browse(self.diseno_id.id)

        if "Lola".upper() in str(boceto.carta_color_nvm.marca.name).upper():

            agentes_bibi = self.env['agentes.navima'].search([('vip_lola', '=', True)])

            id_agentes = []

            for agente in agentes_bibi:

                id_agentes.append(agente.id)

            self.agente_de_venta =  [(6, 0, id_agentes)]

        elif "Bibi".upper() in str(boceto.carta_color_nvm.marca.name).upper():
            
            agentes_bibi = self.env['agentes.navima'].search([('vip_bibi', '=', True)])

            id_agentes = []

            for agente in agentes_bibi:

                id_agentes.append(agente.id)

            self.agente_de_venta =  [(6, 0, id_agentes)]

        boceto._depends_muestras()

    
    def set_all_agents(self):

        boceto = self.env['nvm_design.request'].browse(self.diseno_id.id)

        if "Lola".upper() in str(boceto.carta_color_nvm.marca.name).upper():

            agentes_bibi = self.env['agentes.navima'].search([('all_lola', '=', True)])

            id_agentes = []

            for agente in agentes_bibi:

                id_agentes.append(agente.id)

            self.agente_de_venta =  [(6, 0, id_agentes)]

        elif "Bibi".upper() in str(boceto.carta_color_nvm.marca.name).upper():
            
            agentes_bibi = self.env['agentes.navima'].search([('all_bibi', '=', True)])

            id_agentes = []

            for agente in agentes_bibi:

                id_agentes.append(agente.id)

            self.agente_de_venta =  [(6, 0, id_agentes)]

        boceto._depends_muestras()


    @api.depends('agente_de_venta')
    def _depends_agente_de_venta(self):

        boceto = self.env['nvm_design.request'].browse(self.diseno_id.id)
        boceto.actualizar_muestras()