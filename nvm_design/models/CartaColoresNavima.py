# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CartaColoresNavima(models.Model):
    _name = 'cartacoloresnavima.cartacoloresnavima'
    _description = 'Modelo para las cartas de colores'

    name = fields.Char('Código carta de color')

    proveedor = fields.Many2one('res.partner', 'Proveedor', required=True)

    color = fields.Many2many(
        'coloresnnavima',
        string='Colores'
    )

    codigo_material_interno = fields.Char('Código material')

    material = fields.Many2one('materiales.materiales', 'Material', required=True) 
    coleccion = fields.Many2one('colecciones.colecciones', 'Colección', required=True)
    descripcion_material = fields.Char('Descripcion material', required=True)
    codigo_material = fields.Char('Código Material')
    temporada = fields.Char('Temporada')
    tipo_de_material = fields.Selection([('ALGODON', 'ALGODON'), ('ANTE', 'ANTE'), ('ECOPIEL', 'ECOPIEL'), ('NAPA', 'NAPA'), ('NOBUCK', 'NOBUCK'), ('OTROS MATERIALES', 'OTROS MATERIALES'), ('PIEL', 'PIEL'), ('PIEL VEGANA', 'PIEL VEGANA'), ('SERRAJE', 'SERRAJE'), ('SINTETICO', 'SINTETICO'), ('TEXTIL', 'TEXTIL')],'Categoria de material')

    @api.onchange('coleccion', 'codigo_material_interno')
    def _onchange_material(self):

        nombre_coleccion = str(self.coleccion.name)[0:3]
        self.name = str(nombre_coleccion) + '-' + str(self.codigo_material_interno)
        self.marca = self.coleccion.marca_nvm

    """@api.onchange('name')
    def _onchange_name(self):
        if len(str(self.name)) >= 5 and "-" in str(self.name):
            nombre_carta_color = str(self.name).split("-")

            self.update({'temporada': str(nombre_carta_color[0]), 'codigo_material': str(nombre_carta_color[1])})"""

    #codigo_proveedor = fields.Char('Codigo Proveedor')
    colors_image = fields.Binary("Imagen", help="Seleccionar imagen")
    colors_fields = fields.Binary("Documento carta color", help="Seleccionar documento")

    marca = fields.Many2one('marcasnavima', 'Marca', required=True)

    #@api.onchange('proveedor')
    #def _onchange_proveedor(self):
    #    self.codigo_proveedor = self.env['res.partner'].search([('id', '=', self.proveedor.id)]).codigo_proveedor
