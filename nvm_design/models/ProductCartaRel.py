# -*- coding: utf-8 -*-
from odoo import models, fields, api
import json

class ColoresNavima(models.Model):
    _inherit = "product.template"

    @api.onchange('carta_color_navima', 'medidas_navima', 'marca_modelo_navima') # TODO ADD 'marca_modelo_navima'
    def _onchange_carta_medidas(self):
        self.modelo_navima = str(self.medidas_navima) + str(self.carta_color_navima.material.cod_material)
        self.coleccion_navima = str(self.carta_color_navima.coleccion.temporada) + "-" + str(self.marca_modelo_navima.display_name)
        if self.purchase_ok and self.carta_color_navima.proveedor.id:
            id_supplier_info = self.env['product.supplierinfo'].create({'name': self.carta_color_navima.proveedor.id, 'delay': 1, 'min_qty': 0.0, 'price': 0.0})
            self.seller_ids = [id_supplier_info.id]

    # PRECIO

    precio_pvr = fields.Float('PVR EUR')
    precio_usa_pvr = fields.Float('PVR USD')

    precio_pvp = fields.Float('PVP EUR')
    precio_usa_pvp = fields.Float('PVP USD')

    extra_cost = fields.Float('Coste Extra', default=0)

    coste_propuesto = fields.Float('Coste Propuesto')
    coste = fields.Float('Coste Deseado')
    coste_final = fields.Float('Coste con aranceles (Deseado)')
    coste_final_propuesto = fields.Float('Coste con aranceles (Propuesto)')

    precio_propuesto = fields.Float('Precio Recomendado (Propuesto)')
    precio = fields.Float('Precio Recomendado (Deseado)')
    precio_it = fields.Float('Precio Recomendado F.O.B')
    precio_usa = fields.Float('Precio Recomendado USA')
    precio_final = fields.Float('Precio Final')
    precio_final_it = fields.Float('Precio F.O.B')
    precio_final_usa = fields.Float('Precio USA')

    moneda_del_proveedor = fields.Many2one('res.currency', string='Moneda del proveedor')

    @api.onchange('carta_color_navima')
    def _valor_moneda_proveedor(self):

        moneda = self.carta_color_navima.proveedor.property_purchase_currency_id
        self.moneda_del_proveedor = moneda


    @api.onchange('coste_propuesto', 'extra_cost', 'carta_color_navima')
    def _onchange_coste_propuesto(self):

        coleccion_calcular_precio = self.carta_color_navima.coleccion
        multiplo_a_convertir = coleccion_calcular_precio.cash_conversion.multiplo_a_convertir
        multiplo_conversion = coleccion_calcular_precio.cash_conversion.multiplo_conversion

        _carta_color = self.env['cartacoloresnavima.cartacoloresnavima'].browse(self.carta_color_navima.id)

        tp_multiplicador = _carta_color.material.tipo_de_producto.multiplo_precio

        final = self.coste_propuesto * tp_multiplicador

        if self.extra_cost > 0:

            final = final + self.extra_cost

        self.coste_final_propuesto = final

        self.precio_propuesto = final * coleccion_calcular_precio.multiplicador

        
    @api.onchange('precio')
    def _onchange_precio(self):

        coleccion_calcular_precio = self.carta_color_navima.coleccion
        multiplo_a_convertir = coleccion_calcular_precio.cash_conversion.multiplo_a_convertir
        multiplo_conversion = coleccion_calcular_precio.cash_conversion.multiplo_conversion
        _carta_color = self.env['cartacoloresnavima.cartacoloresnavima'].browse(self.carta_color_navima.id)

        tp_multiplicador = _carta_color.material.tipo_de_producto.multiplo_precio

        if not coleccion_calcular_precio.multiplicador == 0:
            _coste_base = self.precio / coleccion_calcular_precio.multiplicador

            self.coste_final = _coste_base

            self.precio_usa = _coste_base * coleccion_calcular_precio.multiplicador_usa
            self.precio_it = _coste_base * coleccion_calcular_precio.multiplicador_fob #F.O.B

        self.precio_pvr = self.precio * coleccion_calcular_precio.multiplicador_pvr
        self.precio_usa_pvr = self.precio_usa * coleccion_calcular_precio.multiplicador_usa_pvr

        if self.extra_cost > 0 and not tp_multiplicador == 0:

            _coste_base = _coste_base - self.extra_cost

            self.coste = _coste_base / tp_multiplicador
        

    def set_cost_as_final_cost(self):

        if self.coste_final:

            moneda_del_proveedor = self.carta_color_navima.proveedor.property_purchase_currency_id.id  # en sp se llama currency_id, es un m20 para currency.
            tiempo_inicial_de_entrega = 5                                                           # en sp se llama delay, es un entero.
            cantidad_minima = 1.0                                                                   # en sp se llama min_qty, es float.
            proveedor = self.carta_color_navima.proveedor.id                                        # en sp se llama name, es m2o para el contacto.
            precio = self.coste_final * self.multiplicador                                                         # en sp se llama price, es un float.
            product_tmpl_id = self.id                                                               # en sp se llama product_tmpl_id, es m2o para la plantilla del producto.
            product_uom = self.uom_po_id.id                                                            # en sp se llama product_uom, es un m2o para las unidades de medida.
            
            id_supplierinfo = self.env['product.supplierinfo'].create({
                'currency_id': moneda_del_proveedor,
                'delay': tiempo_inicial_de_entrega,
                'min_qty': cantidad_minima,
                'name': proveedor,
                'price': precio,
                'product_tmpl_id': product_tmpl_id,
                'product_uom': product_uom
                })

    # FIN PRECIO

    def make_variants(self):
        
        id_color_producto_comun = 0
        id_attribute_talla = 0
        tallas = ["35", "36", "37", "37,5", "38", "38,5", "39", "40", "41"]
        #f = open('/var/log/odoo15/odoo-log-navima.txt', 'w')
        #f.write('Empiezo la función\n')  # COMMENT

        atts = 0

        for at in self.attribute_line_ids:
            atts = atts + 1

        if atts == 0:
            #f.write('No hay atributos\n')  # COMMENT

            tallas = ["35", "36", "37", "37,5", "38", "38,5", "39", "40", "41"]

            ids_valores_attributo_tallas = []
            attribute_talla = self.env['product.attribute'].create({'create_variant': 'always', 'display_type': 'color', 'name': 'talla'})
            id_attribute_talla = attribute_talla.id

            for talla in tallas:
                valor_atributo_talla = self.env['product.attribute.value'].create({'attribute_id': attribute_talla.id, 'name': str(talla)})
                ids_valores_attributo_tallas.append(valor_atributo_talla.id)

            self.env['product.template.attribute.line'].create({'attribute_id': attribute_talla.id, 'product_tmpl_id': self.id, 'value_ids': ids_valores_attributo_tallas})


            ids_valores_attributo = []
            attribute = self.env['product.attribute'].create({'create_variant': 'always', 'display_type': 'color', 'name': 'color'})
            id_color_producto_comun = attribute.id
            carta_color = self.env['cartacoloresnavima.cartacoloresnavima'].browse(self.carta_color_navima.id)

            for color in carta_color.color:
                valor_attributo = self.env['product.attribute.value'].create({'attribute_id': attribute.id, 'name': str(color.name)})
                ids_valores_attributo.append(valor_attributo.id)

            valorres = []
            
            for valor in ids_valores_attributo:
                if not valor in valorres:
                    valorres.append(valor)

            ids_valores_attributo = valorres

            self.env['product.template.attribute.line'].create({'attribute_id': attribute.id, 'product_tmpl_id': self.id, 'value_ids': ids_valores_attributo})


        else:

            colores = []
            att_color = False
            att = ""

            for att_f in self.attribute_line_ids:
                #f.write('att.display_name = ' + str(att_f.display_name + '\n'))  # COMMENT
                if att_f.display_name == 'color':
                    att_color = True
                    att = att_f

            if att_color:
                #f.write('Hay atributo color\n')  # COMMENT

                self.attribute_line_ids = [[2, att.id]]
                ids_valores_attributo = []
                attribute = self.env['product.attribute'].create({'create_variant': 'always', 'display_type': 'color', 'name': 'color'})
                id_color_producto_comun = attribute.id
                carta_color = self.env['cartacoloresnavima.cartacoloresnavima'].browse(self.carta_color_navima.id)
                for color in carta_color.color:
                    
                    #f.write('color.name = ' + str(color.name) + '\n')  # COMMENT
                    valor_attributo = self.env['product.attribute.value'].create({'attribute_id': attribute.id, 'name': str(color.name)})
                    #f.write('valor_attributo = ' + str(valor_attributo) + '\n')  # COMMENT
                    ids_valores_attributo.append(valor_attributo.id)

                #f.write('ids_valores_attributo = ' + str(ids_valores_attributo) + '\n')  # COMMENT
                self.env['product.template.attribute.line'].create({'attribute_id': attribute.id, 'product_tmpl_id': self.id, 'value_ids': ids_valores_attributo})

                tallas = ["35", "36", "37", "37,5", "38", "38,5", "39", "40", "41"]
        
                ids_valores_attributo_tallas = []
                attribute_talla = self.env['product.attribute'].create({'create_variant': 'always', 'display_type': 'color', 'name': 'talla'})
                id_attribute_talla = attribute_talla.id

                for talla in tallas:
                    valor_atributo_talla = self.env['product.attribute.value'].create({'attribute_id': attribute_talla.id, 'name': str(talla)})
                    ids_valores_attributo_tallas.append(valor_atributo_talla.id)

                self.env['product.template.attribute.line'].create({'attribute_id': attribute_talla.id, 'product_tmpl_id': self.id, 'value_ids': ids_valores_attributo_tallas})

            else:
                #f.write('No hay atributo color\n')  # COMMENT
                ids_valores_attributo = []
                attribute = self.env['product.attribute'].create({'create_variant': 'always', 'display_type': 'color', 'name': 'color'})
                id_color_producto_comun = attribute.id
                carta_color = self.env['cartacoloresnavima.cartacoloresnavima'].browse(self.carta_color_navima.id)
                for color in carta_color.color:
                    
                    #f.write('color.name = ' + str(color.name) + '\n')  # COMMENT
                    valor_attributo = self.env['product.attribute.value'].create({'attribute_id': attribute.id, 'name': str(color.name)})
                    #f.write('valor_attributo = ' + str(valor_attributo) + '\n')  # COMMENT
                    ids_valores_attributo.append(valor_attributo.id)

                #f.write('ids_valores_attributo = ' + str(ids_valores_attributo) + '\n')  # COMMENT
                self.env['product.template.attribute.line'].create({'attribute_id': attribute.id, 'product_tmpl_id': self.id, 'value_ids': ids_valores_attributo})

                tallas = ["35", "36", "37", "37,5", "38", "38,5", "39", "40", "41"]
        
                ids_valores_attributo_tallas = []
                attribute_talla = self.env['product.attribute'].create({'create_variant': 'always', 'display_type': 'color', 'name': 'talla'})
                id_attribute_talla = attribute_talla.id

                for talla in tallas:
                    valor_atributo_talla = self.env['product.attribute.value'].create({'attribute_id': attribute_talla.id, 'name': str(talla)})
                    ids_valores_attributo_tallas.append(valor_atributo_talla.id)

                self.env['product.template.attribute.line'].create({'attribute_id': attribute_talla.id, 'product_tmpl_id': self.id, 'value_ids': ids_valores_attributo_tallas})
        
        carta_color = self.env['cartacoloresnavima.cartacoloresnavima'].browse(self.carta_color_navima.id)

        temporada_producto = carta_color.coleccion.temporada
        nombre_nuevo_producto = self.modelo_navima + " - " + temporada_producto

        uom = self.env['uom.uom'].search([('name', '=', 'Unidades')])

        nuevo_producto = self.env['product.template'].create({'name': nombre_nuevo_producto, 
                                                    'marca_modelo_navima': self.marca_modelo_navima.id, 
                                                    'carta_color_navima': self.carta_color_navima.id,
                                                    'modelo_navima': self.modelo_navima,
                                                    'horma_nvm': self.horma_nvm.id,
                                                    'medidas_navima': self.medidas_navima,
                                                    'coleccion_nvm': self.coleccion_nvm.id,
                                                    'uom_id': uom.id,
                                                    'uom_po_id': uom.id,
                                                    'image_1920': self.image_1920,
                                                    'route_ids': [(6, 0, [1, 5])],
                                                    'detailed_type': 'product',
                                                    'foto_marca': self.foto_marca,
                                                    'tracking': 'lot',
                                                    'categ_id': self.categ_id.id,
                                                    'sale_ok': True,
                                                    'product_add_mode': 'matrix',
                                                    'can_be_expensed': True,
                                                    'purchase_ok': True
                                                    })
        

        tiempo_inicial_de_entrega = 5                                                           # en sp se llama delay, es un entero.
        cantidad_minima = 1.0                                                                   # en sp se llama min_qty, es float.
        proveedor = self.carta_color_navima.proveedor.id                                         # en sp se llama name, es m2o para el contacto.
        precio = self.coste_final
        precio_final = self.precio_final                                                      # en sp se llama price, es un float.
        product_tmpl_id = nuevo_producto.id                                                               # en sp se llama product_tmpl_id, es m2o para la plantilla del producto.
        product_uom = uom.id                                                          # en sp se llama product_uom, es un m2o para las unidades de medida.
        

        id_supplierinfo = self.env['product.supplierinfo'].create({
                        'currency_id': 1, #MOD LATER
                        'delay': tiempo_inicial_de_entrega,
                        'min_qty': cantidad_minima,
                        'partner_id': proveedor,
                        'price': precio,
                        'product_tmpl_id': product_tmpl_id,
                        'product_uom': uom.id
                        })
        
        packs = ["A", "B", "C", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Y"]

        attribute_p = self.env['product.attribute'].create({'create_variant': 'always', 'display_type': 'color', 'name': 'COLOR'})
        ids_valores_attributo = []
        colores_general = []
        
        for color in carta_color.color:

            color_buscado = self.env['coloresnnavima'].browse(color.id)
            colores_general.append(str(color_buscado.name))

            valor_attributo = self.env['product.attribute.value'].create({'attribute_id': attribute_p.id, 'name': str(color.name)})
            ids_valores_attributo.append(valor_attributo.id)
        
        self.env['product.template.attribute.line'].create({'attribute_id': attribute_p.id, 'product_tmpl_id': nuevo_producto.id, 'value_ids': ids_valores_attributo})

        attribute_packs = self.env['product.attribute'].create({'create_variant': 'always', 'display_type': 'color', 'name': 'PACK'})
        ids_valores_attributo_packs = []

        for pack in packs:
            valor_attributo_pack = self.env['product.attribute.value'].create({'attribute_id': attribute_packs.id, 'name': str(pack)})
            ids_valores_attributo_packs.append(valor_attributo_pack.id)

        self.env['product.template.attribute.line'].create({'attribute_id': attribute_packs.id, 'product_tmpl_id': nuevo_producto.id, 'value_ids': ids_valores_attributo_packs})

        productos_packs = self.env['product.product'].search([('product_tmpl_id', '=', nuevo_producto.id)])

        matriz_packs = """{"A": { "35": 0, "36": 1, "37": 2, "37,5": 0, "38": 2, "38,5": 0, "39": 2, "40": 1, "41": 0, "total": 8},"B": { "35": 0, "36": 1, "37": 2, "37,5": 0, "38": 3, "38,5": 0, "39": 2, "40": 1, "41": 1, "total": 10},"C": { "35": 0, "36": 1, "37": 2, "37,5": 0, "38": 3, "38,5": 0, "39": 3, "40": 2, "41": 1, "total": 12},"E": { "35": 1, "36": 1, "37": 2, "37,5": 0, "38": 3, "38,5": 0, "39": 2, "40": 1, "41": 0, "total": 10},"F": { "35": 0, "36": 1, "37": 1, "37,5": 0, "38": 2, "38,5": 0, "39": 3, "40": 2, "41": 1, "total": 10},"G": { "35": 0, "36": 1, "37": 1, "37,5": 0, "38": 2, "38,5": 0, "39": 1, "40": 1, "41": 0, "total": 6},"H": { "35": 1, "36": 1, "37": 2, "37,5": 0, "38": 2, "38,5": 0, "39": 1, "40": 1, "41": 0, "total": 8},"I": { "35": 1, "36": 2, "37": 2, "37,5": 0, "38": 2, "38,5": 0, "39": 1, "40": 0, "41": 0, "total": 8},"J": { "35": 1, "36": 1, "37": 2, "37,5": 0, "38": 3, "38,5": 0, "39": 2, "40": 1, "41": 0, "total": 10},"K": { "35": 0, "36": 1, "37": 1, "37,5": 0, "38": 2, "38,5": 0, "39": 2, "40": 1, "41": 1, "total": 8},"L": { "35": 0, "36": 0, "37": 1, "37,5": 0, "38": 3, "38,5": 0, "39": 3, "40": 1, "41": 0, "total": 8},"M": { "35": 0, "36": 0, "37": 1, "37,5": 0, "38": 3, "38,5": 0, "39": 3, "40": 2, "41": 1, "total": 10},"N": { "35": 0, "36": 1, "37": 2, "37,5": 0, "38": 2, "38,5": 0, "39": 2, "40": 2, "41": 1, "total": 10},"Y": { "35": 0, "36": 0, "37": 1, "37,5": 0, "38": 2, "38,5": 0, "39": 2, "40": 2, "41": 1, "total": 8}}"""

        uom = self.env['uom.uom'].search([('name', '=', 'Unidades')])

        matriz_de_packs = json.loads(str(matriz_packs), strict=False)
        
        for producto_pack in productos_packs:
            color = ""
            pack = ""
            producto = self.env['product.product'].browse(producto_pack.id)

            bom_id = self.env['mrp.bom'].create({
                'product_qty': 1,
                'product_id': producto_pack.id,
                'product_tmpl_id': nuevo_producto.id,
                'product_uom_id': uom.id,
                'ready_to_produce': 'all_available',
                'type': 'normal'
            })

            for attribute_val in producto.product_template_attribute_value_ids:
                atributo = self.env['product.template.attribute.value'].browse(attribute_val.id)

                if atributo.name in packs:
                    pack = str(atributo.name)

                if str(atributo.name) in colores_general:
                    color = str(atributo.name)

            producto_pack.standard_price = precio * float(matriz_de_packs[pack]["total"])
            producto_pack.lst_price = precio_final * float(matriz_de_packs[pack]["total"])

            productos_tallas = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
 
            uom = self.env['uom.uom'].search([('name', '=', 'Pares')])

            for talla in matriz_de_packs[pack]:
                if matriz_de_packs[pack][talla] > 0:
                    for producto_talla in productos_tallas:
                        p_talla = self.env['product.product'].browse(producto_talla.id)

                        talla_base = ""
                        color_base = ""

                        for attribute_val in p_talla.product_template_attribute_value_ids:
                            atributo = self.env['product.template.attribute.value'].browse(attribute_val.id)
                            if str(atributo.name) == str(talla):
                                talla_base = True

                            if str(atributo.name) == color:
                                color_base = True

                        if talla_base and color_base:
                            line_nueva = self.env['mrp.bom.line'].create({
                                'bom_id': bom_id.id,
                                'product_id': p_talla.id,
                                'product_qty': float(matriz_de_packs[pack][talla]),
                                'product_uom_id': uom.id
                            })

                        p_talla.standard_price = precio
                        p_talla.lst_price = precio_final
                       
        tallas = ["35", "36", "37", "37,5", "38", "38,5", "39", "40", "41", "A", "B", "C", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Y"]

        #variantes_de_productos = self.env['product.product'].search([('is_product_variant', '=', 'True')])

        """for variantes in variantes_de_productos:

            variante = self.env['product.product'].browse(variantes)

            try:

                for attribute in variante.product_template_attribute_value_ids:

                    if str(attribute.name) in tallas:

                        variante.talla_pack = str(attribute.name)

                    else:

                        variante.color = str(attribute.name)
                    # TODO USAR en division de lotes

            except:

                pass"""

    carta_color_navima = fields.Many2one('cartacoloresnavima.cartacoloresnavima', 'Carta de color')
    medidas_navima = fields.Char('Medidas caja')
    sku_navima = fields.Char('ID Modelo')
    marca_navima = fields.Selection([('BIBI LOU','BIBI LOU'), ('LOLA CRUZ','LOLA CRUZ')],'Marca')
    marca_modelo_navima = fields.Many2one('marcasnavima', 'Marca')
    cod_aduanero = fields.Many2one('hs.master', 'Código aduanero')
    foto_marca = fields.Binary('Foto Marca')

    modelo_navima = fields.Char('Modelo')
    referencia_diseno_navima = fields.Char('Referencia de diseño')
    referencia_de_proveedor = fields.Char('Referencia de proveedor')

    coleccion_navima = fields.Char('Coleccion')
    coleccion_nvm = fields.Many2one('colecciones.colecciones')
    horma_nvm = fields.Many2one('horma.horma')
    referencia_video_navima = fields.Char('Referencia de video')
    tipo_de_producto_navima = fields.Selection([('IP','IP'), ('IS','IS'), ('IT','IT'), ('CP','CP'), ('CS','CS'), ('VP','VP'), ('VS','VS'), ('VT','VT'), ('CT','CT'), ('Comunitario','Comunitario')], 'Tipo de producto')
    plataforma_navima = fields.Selection([('0','0 cm'), ('0,5','0,5 cm'), ('1','1 cm'), ('1,5','1,5 cm'), ('2','2 cm'), ('2,5','2,5 cm'), ('3','3 cm'), ('3,5','3,5 cm')],'Plataforma')
    alto_tacon_navima = fields.Selection([('0','0 cm'), ('0,5','0,5 cm'), ('1','1 cm'), ('1,5','1,5 cm'), ('2','2 cm'), ('2,5','2,5 cm'), ('3','3 cm'), ('3,5','3,5 cm'), ('4','4 cm'), ('4,5','4,5 cm'), ('5','5 cm')],'Plataforma')
    tipo_de_calzado_navima = fields.Selection([('Tacon','Tacon'), ('Loafers','Loafers'), ('Bota','Bota')],'Plataforma')
    descripcion_web_es = fields.Char('Descripción ES')
    descripcion_web_en = fields.Char('Descripción EN')
    timbrado = fields.Many2one('timbrado', 'Timbrado')
