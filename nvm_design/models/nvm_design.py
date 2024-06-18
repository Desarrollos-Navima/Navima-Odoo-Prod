# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID
import base64


class Design(models.Model):

    "Modelo base"

    _name = 'nvm_design'
    _description = 'Modelo base'

    name = fields.Char('Nombre')


class DesignStage(models.Model):

    "Modelo para las etapas de diseño que contendran los bocetos en la vista kanban"

    _name = 'nvm_design.stage'
    _description = 'Estapas de diseño'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Secuence', default=20)
    fold = fields.Boolean('Doblada en diseño')
    done = fields.Boolean('Hecho')
    color = fields.Integer('Color Index')


class DesignRequest(models.Model):
    
    "Modelo para los Bocetos de diseño"

    _name = 'nvm_design.request'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin'] #MAILNVM
    _description = 'Bocetos de diseño'
    _order = 'id desc'
    _check_company_auto = True

    # DE TEXTO

    name = fields.Char('Name', required=True)
    modelo_base_nvm = fields.Char('Modelo Base')
    product_name_nvm = fields.Char('Nombre Web')
    referencia_design_nvm = fields.Char('Referencia de diseño')
    variante_de_horma_nvm = fields.Char('Variante de Horma')
    carta_color_modelo_base = fields.Char('Carta Color mas Modelo Base')
    atributo_con = fields.Char('Con...')
    coleccion = fields.Many2one('colecciones.colecciones', 'Colección', required=True)

    descripcion_web = fields.Text('Descripción')

    mensaje_muestras = fields.Html('Mensaje para la petición de muestras')
    fiting = fields.Html('Fiting')

    primer_porcentaje_ext = fields.Char('Primer porc ext')
    segundo_porcentaje_ext = fields.Char('Segundo porc ext')
    tercero_porcentaje_ext = fields.Char('Tercero porc ext')

    primer_porcentaje_int = fields.Char('Primer porc int')
    segundo_porcentaje_int = fields.Char('Segundo porc int')
    tercero_porcentaje_int = fields.Char('Tercero porc int')

    # EMOJI

    EMOJI_SELECTION = [
        ('✅', 'Confirmado'),
        ('❓', 'Stand By'),
        ('❌', 'Cancelado'),
        ('👢', 'Esperando 2ª Muestra'),
    ]

    emoji = fields.Selection(selection=EMOJI_SELECTION, string='Emoji')


    @api.returns('self')
    def _default_stage(self):
        return self.env['nvm_design.stage'].search([], limit=1)

    
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'stage_id' in init_values:
            return self.env.ref('maintenance.mt_req_status')
        return super(DesignRequest, self)._track_subtype(init_values)

    
    @api.returns('self')
    def _get_default_team_id(self):
        MT = self.env['design.team']
        team = MT.search([('company_id', '=', self.env.company.id)], limit=1)
        if not team:
            team = MT.search([], limit=1)
        return team.id


    # Campos NUMERICOS

    multiplicador = fields.Float('Multiplicador Precio', default=2.5)
    multiplicador_it = fields.Float('Multiplicador IT', default=2.6)
    multiplicador_usa = fields.Float('Multiplicador USA', default=2.7)

    multiplicador_pvr = fields.Float('Multiplicador PVR', default=2.5)
    multiplicador_usa_pvr = fields.Float('Multiplicador PVR USA', default=2.7)

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

    # SELECCIONABLES

    primero_int = fields.Selection([('Piel', 'Piel'), ('Ante', 'Ante'), ('Acero', 'Acero'), ('Acero brillo', 'Acero brillo'), ('Acero y Piedras', 'Acero y Piedras'), ('Acetato', 'Acetato'), ('Acrílico', 'Acrílico'), ('Afelpado', 'Afelpado'), ('Algodón', 'Algodón'), ('Algodón canvas', 'Algodón canvas'), ('Algodón egipcio', 'Algodón egipcio'), ('Algodón encerado', 'Algodón encerado'), ('Algodón felpa francesa', 'Algodón felpa francesa'), ('Algodón jersey', 'Algodón jersey'), ('Algodón modal', 'Algodón modal'), ('Algodón orgánico', 'Algodón orgánico'), ('Algodón peinado', 'Algodón peinado'), ('Algodón pima', 'Algodón pima'), ('Algodón Voile', 'Algodón Voile'), ('Alpaca', 'Alpaca'), ('Aluminio', 'Aluminio'), ('Angora', 'Angora'), ('Arcilla', 'Arcilla'), ('Armys', 'Armys'), ('Bamboo', 'Bamboo'), ('Bambú', 'Bambú'), ('Box', 'Box'), ('Cachemire', 'Cachemire'), ('Cañamo', 'Cañamo'), ('Cáñamo', 'Cáñamo'), ('Carey', 'Carey'), ('Cashemire', 'Cashemire'), ('Cashmere', 'Cashmere'), ('Caucho', 'Caucho'), ('Caucho vulcanizado', 'Caucho vulcanizado'), ('Celulosa', 'Celulosa'), ('Cerámica', 'Cerámica'), ('Chapado', 'Chapado'), ('Charol', 'Charol'), ('Conejo', 'Conejo'), ('Coolmax', 'Coolmax'), ('Crystal Mesh', 'Crystal Mesh'), ('Cuero', 'Cuero'), ('Cuero sintético', 'Cuero sintético'), ('Cuero sintético ecológico', 'Cuero sintético ecológico'), ('Cuero vegetal', 'Cuero vegetal'), ('Cupro', 'Cupro'), ('Dralón', 'Dralón'), ('Ecopiel', 'Ecopiel'), ('Elastán', 'Elastán'), ('Elastano', 'Elastano'), ('Elastano double-weave twill', 'Elastano double-weave twill'), ('Elastodieno', 'Elastodieno'), ('Elastomero', 'Elastomero'), ('Elastomultiester', 'Elastomultiester'), ('Esparto', 'Esparto'), ('Etil-Vinil-Acetato (EVA)', 'Etil-Vinil-Acetato (EVA)'), ('EVA', 'EVA'), ('EVA celular', 'EVA celular'), ('EVA Foam', 'EVA Foam'), ('EVA moldeada', 'EVA moldeada'), ('Felpa', 'Felpa'), ('Latex', 'Latex'), ('Linen', 'Linen'), ('Lino', 'Lino'), ('Liocel', 'Liocel'), ('Lona', 'Lona'), ('Lurex', 'Lurex'), ('Lurex metálico', 'Lurex metálico'), ('Lycra', 'Lycra'), ('Lyocell', 'Lyocell'), ('Madera', 'Madera'), ('Madera natural', 'Madera natural'), ('Merino', 'Merino'), ('Meryl', 'Meryl'), ('Mesh', 'Mesh'), ('Metal', 'Metal'), ('Metalizado', 'Metalizado'), ('Mezcla de fibras', 'Mezcla de fibras'), ('Microfibra', 'Microfibra'), ('Microfribra', 'Microfribra'), ('Micromodal', 'Micromodal'), ('Micropoliéster', 'Micropoliéster'), ('Mimbre', 'Mimbre'), ('Mineral', 'Mineral'), ('Mineral abovedado', 'Mineral abovedado'), ('Modacrilico', 'Modacrilico'), ('Modal', 'Modal'), ('Mohair', 'Mohair'), ('Mouton vuelto', 'Mouton vuelto'), ('Nailon', 'Nailon'), ('Napa', 'Napa'), ('Napa flor', 'Napa flor'), ('Napa sintética', 'Napa sintética'), ('Neopreno', 'Neopreno'), ('Nobuck', 'Nobuck'), ('Nylon', 'Nylon'), ('Nylon angora', 'Nylon angora'), ('Nylon mohair', 'Nylon mohair'), ('Nylon reciclado', 'Nylon reciclado'), ('Nylon taffeta', 'Nylon taffeta'), ('Nylour', 'Nylour'), ('Organza', 'Organza'), ('Oro', 'Oro'), ('Otros materiales', 'Otros materiales'), ('Paja', 'Paja'), ('Pana', 'Pana'), ('Papel', 'Papel'), ('Pelo', 'Pelo'), ('Piel becerro', 'Piel becerro'), ('Piel bovina', 'Piel bovina'), ('Piel Caprina', 'Piel Caprina'), ('Piel cordero', 'Piel cordero'), ('Piel de búfalo', 'Piel de búfalo'), ('Piel de potro', 'Piel de potro'), ('Piel equina', 'Piel equina'), ('Piel metalizada', 'Piel metalizada'), ('Piel napa', 'Piel napa'), ('Piel nobuck', 'Piel nobuck'), ('Piel ovina', 'Piel ovina'), ('Piel porcina', 'Piel porcina'), ('Piel serpiente', 'Piel serpiente'), ('Piel serraje', 'Piel serraje'), ('Piel vacuna', 'Piel vacuna'), ('Piel vegana', 'Piel vegana'), ('Piqué', 'Piqué'), ('Plástico', 'Plástico'), ('Plata', 'Plata'), ('Plata de ley', 'Plata de ley'), ('Pluma', 'Pluma'), ('Pluma natural', 'Pluma natural'), ('Plumas', 'Plumas'), ('Plumeti', 'Plumeti'), ('Plumón', 'Plumón'), ('Poliacrílico', 'Poliacrílico'), ('Poliamida', 'Poliamida'), ('Poliamida Chiffon', 'Poliamida Chiffon'), ('Policarbonato', 'Policarbonato'), ('Poliéster', 'Poliéster'), ('Poliéster eduction', 'Poliéster eduction'), ('Poliéster micro', 'Poliéster micro'), ('Poliéster reciclado', 'Poliéster reciclado'), ('Poliéster tricot', 'Poliéster tricot'), ('Poliéster, plain weave', 'Poliéster, plain weave'), ('Polietileno', 'Polietileno'), ('Polipropileno', 'Polipropileno'), ('Poliuretano', 'Poliuretano'), ('Polivinilcloruro', 'Polivinilcloruro'), ('Polivinilo', 'Polivinilo'), ('Poly memory', 'Poly memory'), ('Propileno', 'Propileno'), ('PU', 'PU'), ('Pulsera', 'Pulsera'), ('Pura lana virgen', 'Pura lana virgen'), ('PVC', 'PVC'), ('Rafia', 'Rafia'), ('Ramil', 'Ramil'), ('Ramio', 'Ramio'), ('Raso', 'Raso'), ('Ratio', 'Ratio'), ('Rayón', 'Rayón'), ('Resina', 'Resina'), ('Resina acrílica', 'Resina acrílica'), ('Resina de plástico', 'Resina de plástico'), ('Resina poliuretano', 'Resina poliuretano'), ('Rex', 'Rex'), ('Rodio', 'Rodio'), ('Satén', 'Satén'), ('Seda', 'Seda'), ('Seda natural', 'Seda natural'), ('Serraje', 'Serraje'), ('Silicona', 'Silicona'), ('Sinamay', 'Sinamay'), ('Sintético', 'Sintético'), ('Softshell', 'Softshell'), ('Spandex', 'Spandex'), ('T400', 'T400'), ('Tactel', 'Tactel'), ('Tecno-policarbonato', 'Tecno-policarbonato'), ('Tela', 'Tela'), ('Tencel', 'Tencel'), ('Terciopelo', 'Terciopelo'), ('Textil', 'Textil'), ('Thermocool Poliéster', 'Thermocool Poliéster'), ('Titanio', 'Titanio'), ('TPU Compacto', 'TPU Compacto'), ('Trevira', 'Trevira'), ('Tul', 'Tul'), ('Varias', 'Varias'), ('Velour', 'Velour'), ('Vinilo', 'Vinilo'), ('Viscosa', 'Viscosa'), ('Viscosa Modal', 'Viscosa Modal'), ('Visón', 'Visón'), ('XLA', 'XLA'), ('Yak', 'Yak'), ('Yute', 'Yute'), ('Zafiro', 'Zafiro'), ('Zamak', 'Zamak'), ('Zorro', 'Zorro')], 'Primer material interior.')
    segundo_int = fields.Selection([('Piel', 'Piel'), ('Ante', 'Ante'), ('Acero', 'Acero'), ('Acero brillo', 'Acero brillo'), ('Acero y Piedras', 'Acero y Piedras'), ('Acetato', 'Acetato'), ('Acrílico', 'Acrílico'), ('Afelpado', 'Afelpado'), ('Algodón', 'Algodón'), ('Algodón canvas', 'Algodón canvas'), ('Algodón egipcio', 'Algodón egipcio'), ('Algodón encerado', 'Algodón encerado'), ('Algodón felpa francesa', 'Algodón felpa francesa'), ('Algodón jersey', 'Algodón jersey'), ('Algodón modal', 'Algodón modal'), ('Algodón orgánico', 'Algodón orgánico'), ('Algodón peinado', 'Algodón peinado'), ('Algodón pima', 'Algodón pima'), ('Algodón Voile', 'Algodón Voile'), ('Alpaca', 'Alpaca'), ('Aluminio', 'Aluminio'), ('Angora', 'Angora'), ('Arcilla', 'Arcilla'), ('Armys', 'Armys'), ('Bamboo', 'Bamboo'), ('Bambú', 'Bambú'), ('Box', 'Box'), ('Cachemire', 'Cachemire'), ('Cañamo', 'Cañamo'), ('Cáñamo', 'Cáñamo'), ('Carey', 'Carey'), ('Cashemire', 'Cashemire'), ('Cashmere', 'Cashmere'), ('Caucho', 'Caucho'), ('Caucho vulcanizado', 'Caucho vulcanizado'), ('Celulosa', 'Celulosa'), ('Cerámica', 'Cerámica'), ('Chapado', 'Chapado'), ('Charol', 'Charol'), ('Conejo', 'Conejo'), ('Coolmax', 'Coolmax'), ('Crystal Mesh', 'Crystal Mesh'), ('Cuero', 'Cuero'), ('Cuero sintético', 'Cuero sintético'), ('Cuero sintético ecológico', 'Cuero sintético ecológico'), ('Cuero vegetal', 'Cuero vegetal'), ('Cupro', 'Cupro'), ('Dralón', 'Dralón'), ('Ecopiel', 'Ecopiel'), ('Elastán', 'Elastán'), ('Elastano', 'Elastano'), ('Elastano double-weave twill', 'Elastano double-weave twill'), ('Elastodieno', 'Elastodieno'), ('Elastomero', 'Elastomero'), ('Elastomultiester', 'Elastomultiester'), ('Esparto', 'Esparto'), ('Etil-Vinil-Acetato (EVA)', 'Etil-Vinil-Acetato (EVA)'), ('EVA', 'EVA'), ('EVA celular', 'EVA celular'), ('EVA Foam', 'EVA Foam'), ('EVA moldeada', 'EVA moldeada'), ('Felpa', 'Felpa'), ('Latex', 'Latex'), ('Linen', 'Linen'), ('Lino', 'Lino'), ('Liocel', 'Liocel'), ('Lona', 'Lona'), ('Lurex', 'Lurex'), ('Lurex metálico', 'Lurex metálico'), ('Lycra', 'Lycra'), ('Lyocell', 'Lyocell'), ('Madera', 'Madera'), ('Madera natural', 'Madera natural'), ('Merino', 'Merino'), ('Meryl', 'Meryl'), ('Mesh', 'Mesh'), ('Metal', 'Metal'), ('Metalizado', 'Metalizado'), ('Mezcla de fibras', 'Mezcla de fibras'), ('Microfibra', 'Microfibra'), ('Microfribra', 'Microfribra'), ('Micromodal', 'Micromodal'), ('Micropoliéster', 'Micropoliéster'), ('Mimbre', 'Mimbre'), ('Mineral', 'Mineral'), ('Mineral abovedado', 'Mineral abovedado'), ('Modacrilico', 'Modacrilico'), ('Modal', 'Modal'), ('Mohair', 'Mohair'), ('Mouton vuelto', 'Mouton vuelto'), ('Nailon', 'Nailon'), ('Napa', 'Napa'), ('Napa flor', 'Napa flor'), ('Napa sintética', 'Napa sintética'), ('Neopreno', 'Neopreno'), ('Nobuck', 'Nobuck'), ('Nylon', 'Nylon'), ('Nylon angora', 'Nylon angora'), ('Nylon mohair', 'Nylon mohair'), ('Nylon reciclado', 'Nylon reciclado'), ('Nylon taffeta', 'Nylon taffeta'), ('Nylour', 'Nylour'), ('Organza', 'Organza'), ('Oro', 'Oro'), ('Otros materiales', 'Otros materiales'), ('Paja', 'Paja'), ('Pana', 'Pana'), ('Papel', 'Papel'), ('Pelo', 'Pelo'), ('Piel becerro', 'Piel becerro'), ('Piel bovina', 'Piel bovina'), ('Piel Caprina', 'Piel Caprina'), ('Piel cordero', 'Piel cordero'), ('Piel de búfalo', 'Piel de búfalo'), ('Piel de potro', 'Piel de potro'), ('Piel equina', 'Piel equina'), ('Piel metalizada', 'Piel metalizada'), ('Piel napa', 'Piel napa'), ('Piel nobuck', 'Piel nobuck'), ('Piel ovina', 'Piel ovina'), ('Piel porcina', 'Piel porcina'), ('Piel serpiente', 'Piel serpiente'), ('Piel serraje', 'Piel serraje'), ('Piel vacuna', 'Piel vacuna'), ('Piel vegana', 'Piel vegana'), ('Piqué', 'Piqué'), ('Plástico', 'Plástico'), ('Plata', 'Plata'), ('Plata de ley', 'Plata de ley'), ('Pluma', 'Pluma'), ('Pluma natural', 'Pluma natural'), ('Plumas', 'Plumas'), ('Plumeti', 'Plumeti'), ('Plumón', 'Plumón'), ('Poliacrílico', 'Poliacrílico'), ('Poliamida', 'Poliamida'), ('Poliamida Chiffon', 'Poliamida Chiffon'), ('Policarbonato', 'Policarbonato'), ('Poliéster', 'Poliéster'), ('Poliéster eduction', 'Poliéster eduction'), ('Poliéster micro', 'Poliéster micro'), ('Poliéster reciclado', 'Poliéster reciclado'), ('Poliéster tricot', 'Poliéster tricot'), ('Poliéster, plain weave', 'Poliéster, plain weave'), ('Polietileno', 'Polietileno'), ('Polipropileno', 'Polipropileno'), ('Poliuretano', 'Poliuretano'), ('Polivinilcloruro', 'Polivinilcloruro'), ('Polivinilo', 'Polivinilo'), ('Poly memory', 'Poly memory'), ('Propileno', 'Propileno'), ('PU', 'PU'), ('Pulsera', 'Pulsera'), ('Pura lana virgen', 'Pura lana virgen'), ('PVC', 'PVC'), ('Rafia', 'Rafia'), ('Ramil', 'Ramil'), ('Ramio', 'Ramio'), ('Raso', 'Raso'), ('Ratio', 'Ratio'), ('Rayón', 'Rayón'), ('Resina', 'Resina'), ('Resina acrílica', 'Resina acrílica'), ('Resina de plástico', 'Resina de plástico'), ('Resina poliuretano', 'Resina poliuretano'), ('Rex', 'Rex'), ('Rodio', 'Rodio'), ('Satén', 'Satén'), ('Seda', 'Seda'), ('Seda natural', 'Seda natural'), ('Serraje', 'Serraje'), ('Silicona', 'Silicona'), ('Sinamay', 'Sinamay'), ('Sintético', 'Sintético'), ('Softshell', 'Softshell'), ('Spandex', 'Spandex'), ('T400', 'T400'), ('Tactel', 'Tactel'), ('Tecno-policarbonato', 'Tecno-policarbonato'), ('Tela', 'Tela'), ('Tencel', 'Tencel'), ('Terciopelo', 'Terciopelo'), ('Textil', 'Textil'), ('Thermocool Poliéster', 'Thermocool Poliéster'), ('Titanio', 'Titanio'), ('TPU Compacto', 'TPU Compacto'), ('Trevira', 'Trevira'), ('Tul', 'Tul'), ('Varias', 'Varias'), ('Velour', 'Velour'), ('Vinilo', 'Vinilo'), ('Viscosa', 'Viscosa'), ('Viscosa Modal', 'Viscosa Modal'), ('Visón', 'Visón'), ('XLA', 'XLA'), ('Yak', 'Yak'), ('Yute', 'Yute'), ('Zafiro', 'Zafiro'), ('Zamak', 'Zamak'), ('Zorro', 'Zorro')], 'Segundo material interior.')
    tercero_int = fields.Selection([('Piel', 'Piel'), ('Ante', 'Ante'), ('Acero', 'Acero'), ('Acero brillo', 'Acero brillo'), ('Acero y Piedras', 'Acero y Piedras'), ('Acetato', 'Acetato'), ('Acrílico', 'Acrílico'), ('Afelpado', 'Afelpado'), ('Algodón', 'Algodón'), ('Algodón canvas', 'Algodón canvas'), ('Algodón egipcio', 'Algodón egipcio'), ('Algodón encerado', 'Algodón encerado'), ('Algodón felpa francesa', 'Algodón felpa francesa'), ('Algodón jersey', 'Algodón jersey'), ('Algodón modal', 'Algodón modal'), ('Algodón orgánico', 'Algodón orgánico'), ('Algodón peinado', 'Algodón peinado'), ('Algodón pima', 'Algodón pima'), ('Algodón Voile', 'Algodón Voile'), ('Alpaca', 'Alpaca'), ('Aluminio', 'Aluminio'), ('Angora', 'Angora'), ('Arcilla', 'Arcilla'), ('Armys', 'Armys'), ('Bamboo', 'Bamboo'), ('Bambú', 'Bambú'), ('Box', 'Box'), ('Cachemire', 'Cachemire'), ('Cañamo', 'Cañamo'), ('Cáñamo', 'Cáñamo'), ('Carey', 'Carey'), ('Cashemire', 'Cashemire'), ('Cashmere', 'Cashmere'), ('Caucho', 'Caucho'), ('Caucho vulcanizado', 'Caucho vulcanizado'), ('Celulosa', 'Celulosa'), ('Cerámica', 'Cerámica'), ('Chapado', 'Chapado'), ('Charol', 'Charol'), ('Conejo', 'Conejo'), ('Coolmax', 'Coolmax'), ('Crystal Mesh', 'Crystal Mesh'), ('Cuero', 'Cuero'), ('Cuero sintético', 'Cuero sintético'), ('Cuero sintético ecológico', 'Cuero sintético ecológico'), ('Cuero vegetal', 'Cuero vegetal'), ('Cupro', 'Cupro'), ('Dralón', 'Dralón'), ('Ecopiel', 'Ecopiel'), ('Elastán', 'Elastán'), ('Elastano', 'Elastano'), ('Elastano double-weave twill', 'Elastano double-weave twill'), ('Elastodieno', 'Elastodieno'), ('Elastomero', 'Elastomero'), ('Elastomultiester', 'Elastomultiester'), ('Esparto', 'Esparto'), ('Etil-Vinil-Acetato (EVA)', 'Etil-Vinil-Acetato (EVA)'), ('EVA', 'EVA'), ('EVA celular', 'EVA celular'), ('EVA Foam', 'EVA Foam'), ('EVA moldeada', 'EVA moldeada'), ('Felpa', 'Felpa'), ('Latex', 'Latex'), ('Linen', 'Linen'), ('Lino', 'Lino'), ('Liocel', 'Liocel'), ('Lona', 'Lona'), ('Lurex', 'Lurex'), ('Lurex metálico', 'Lurex metálico'), ('Lycra', 'Lycra'), ('Lyocell', 'Lyocell'), ('Madera', 'Madera'), ('Madera natural', 'Madera natural'), ('Merino', 'Merino'), ('Meryl', 'Meryl'), ('Mesh', 'Mesh'), ('Metal', 'Metal'), ('Metalizado', 'Metalizado'), ('Mezcla de fibras', 'Mezcla de fibras'), ('Microfibra', 'Microfibra'), ('Microfribra', 'Microfribra'), ('Micromodal', 'Micromodal'), ('Micropoliéster', 'Micropoliéster'), ('Mimbre', 'Mimbre'), ('Mineral', 'Mineral'), ('Mineral abovedado', 'Mineral abovedado'), ('Modacrilico', 'Modacrilico'), ('Modal', 'Modal'), ('Mohair', 'Mohair'), ('Mouton vuelto', 'Mouton vuelto'), ('Nailon', 'Nailon'), ('Napa', 'Napa'), ('Napa flor', 'Napa flor'), ('Napa sintética', 'Napa sintética'), ('Neopreno', 'Neopreno'), ('Nobuck', 'Nobuck'), ('Nylon', 'Nylon'), ('Nylon angora', 'Nylon angora'), ('Nylon mohair', 'Nylon mohair'), ('Nylon reciclado', 'Nylon reciclado'), ('Nylon taffeta', 'Nylon taffeta'), ('Nylour', 'Nylour'), ('Organza', 'Organza'), ('Oro', 'Oro'), ('Otros materiales', 'Otros materiales'), ('Paja', 'Paja'), ('Pana', 'Pana'), ('Papel', 'Papel'), ('Pelo', 'Pelo'), ('Piel becerro', 'Piel becerro'), ('Piel bovina', 'Piel bovina'), ('Piel Caprina', 'Piel Caprina'), ('Piel cordero', 'Piel cordero'), ('Piel de búfalo', 'Piel de búfalo'), ('Piel de potro', 'Piel de potro'), ('Piel equina', 'Piel equina'), ('Piel metalizada', 'Piel metalizada'), ('Piel napa', 'Piel napa'), ('Piel nobuck', 'Piel nobuck'), ('Piel ovina', 'Piel ovina'), ('Piel porcina', 'Piel porcina'), ('Piel serpiente', 'Piel serpiente'), ('Piel serraje', 'Piel serraje'), ('Piel vacuna', 'Piel vacuna'), ('Piel vegana', 'Piel vegana'), ('Piqué', 'Piqué'), ('Plástico', 'Plástico'), ('Plata', 'Plata'), ('Plata de ley', 'Plata de ley'), ('Pluma', 'Pluma'), ('Pluma natural', 'Pluma natural'), ('Plumas', 'Plumas'), ('Plumeti', 'Plumeti'), ('Plumón', 'Plumón'), ('Poliacrílico', 'Poliacrílico'), ('Poliamida', 'Poliamida'), ('Poliamida Chiffon', 'Poliamida Chiffon'), ('Policarbonato', 'Policarbonato'), ('Poliéster', 'Poliéster'), ('Poliéster eduction', 'Poliéster eduction'), ('Poliéster micro', 'Poliéster micro'), ('Poliéster reciclado', 'Poliéster reciclado'), ('Poliéster tricot', 'Poliéster tricot'), ('Poliéster, plain weave', 'Poliéster, plain weave'), ('Polietileno', 'Polietileno'), ('Polipropileno', 'Polipropileno'), ('Poliuretano', 'Poliuretano'), ('Polivinilcloruro', 'Polivinilcloruro'), ('Polivinilo', 'Polivinilo'), ('Poly memory', 'Poly memory'), ('Propileno', 'Propileno'), ('PU', 'PU'), ('Pulsera', 'Pulsera'), ('Pura lana virgen', 'Pura lana virgen'), ('PVC', 'PVC'), ('Rafia', 'Rafia'), ('Ramil', 'Ramil'), ('Ramio', 'Ramio'), ('Raso', 'Raso'), ('Ratio', 'Ratio'), ('Rayón', 'Rayón'), ('Resina', 'Resina'), ('Resina acrílica', 'Resina acrílica'), ('Resina de plástico', 'Resina de plástico'), ('Resina poliuretano', 'Resina poliuretano'), ('Rex', 'Rex'), ('Rodio', 'Rodio'), ('Satén', 'Satén'), ('Seda', 'Seda'), ('Seda natural', 'Seda natural'), ('Serraje', 'Serraje'), ('Silicona', 'Silicona'), ('Sinamay', 'Sinamay'), ('Sintético', 'Sintético'), ('Softshell', 'Softshell'), ('Spandex', 'Spandex'), ('T400', 'T400'), ('Tactel', 'Tactel'), ('Tecno-policarbonato', 'Tecno-policarbonato'), ('Tela', 'Tela'), ('Tencel', 'Tencel'), ('Terciopelo', 'Terciopelo'), ('Textil', 'Textil'), ('Thermocool Poliéster', 'Thermocool Poliéster'), ('Titanio', 'Titanio'), ('TPU Compacto', 'TPU Compacto'), ('Trevira', 'Trevira'), ('Tul', 'Tul'), ('Varias', 'Varias'), ('Velour', 'Velour'), ('Vinilo', 'Vinilo'), ('Viscosa', 'Viscosa'), ('Viscosa Modal', 'Viscosa Modal'), ('Visón', 'Visón'), ('XLA', 'XLA'), ('Yak', 'Yak'), ('Yute', 'Yute'), ('Zafiro', 'Zafiro'), ('Zamak', 'Zamak'), ('Zorro', 'Zorro')], 'Tercero material interior.')
    
    primero_ext = fields.Selection([('Piel', 'Piel'), ('Ante', 'Ante'), ('Acero', 'Acero'), ('Acero brillo', 'Acero brillo'), ('Acero y Piedras', 'Acero y Piedras'), ('Acetato', 'Acetato'), ('Acrílico', 'Acrílico'), ('Afelpado', 'Afelpado'), ('Algodón', 'Algodón'), ('Algodón canvas', 'Algodón canvas'), ('Algodón egipcio', 'Algodón egipcio'), ('Algodón encerado', 'Algodón encerado'), ('Algodón felpa francesa', 'Algodón felpa francesa'), ('Algodón jersey', 'Algodón jersey'), ('Algodón modal', 'Algodón modal'), ('Algodón orgánico', 'Algodón orgánico'), ('Algodón peinado', 'Algodón peinado'), ('Algodón pima', 'Algodón pima'), ('Algodón Voile', 'Algodón Voile'), ('Alpaca', 'Alpaca'), ('Aluminio', 'Aluminio'), ('Angora', 'Angora'), ('Arcilla', 'Arcilla'), ('Armys', 'Armys'), ('Bamboo', 'Bamboo'), ('Bambú', 'Bambú'), ('Box', 'Box'), ('Cachemire', 'Cachemire'), ('Cañamo', 'Cañamo'), ('Cáñamo', 'Cáñamo'), ('Carey', 'Carey'), ('Cashemire', 'Cashemire'), ('Cashmere', 'Cashmere'), ('Caucho', 'Caucho'), ('Caucho vulcanizado', 'Caucho vulcanizado'), ('Celulosa', 'Celulosa'), ('Cerámica', 'Cerámica'), ('Chapado', 'Chapado'), ('Charol', 'Charol'), ('Conejo', 'Conejo'), ('Coolmax', 'Coolmax'), ('Crystal Mesh', 'Crystal Mesh'), ('Cuero', 'Cuero'), ('Cuero sintético', 'Cuero sintético'), ('Cuero sintético ecológico', 'Cuero sintético ecológico'), ('Cuero vegetal', 'Cuero vegetal'), ('Cupro', 'Cupro'), ('Dralón', 'Dralón'), ('Ecopiel', 'Ecopiel'), ('Elastán', 'Elastán'), ('Elastano', 'Elastano'), ('Elastano double-weave twill', 'Elastano double-weave twill'), ('Elastodieno', 'Elastodieno'), ('Elastomero', 'Elastomero'), ('Elastomultiester', 'Elastomultiester'), ('Esparto', 'Esparto'), ('Etil-Vinil-Acetato (EVA)', 'Etil-Vinil-Acetato (EVA)'), ('EVA', 'EVA'), ('EVA celular', 'EVA celular'), ('EVA Foam', 'EVA Foam'), ('EVA moldeada', 'EVA moldeada'), ('Felpa', 'Felpa'), ('Latex', 'Latex'), ('Linen', 'Linen'), ('Lino', 'Lino'), ('Liocel', 'Liocel'), ('Lona', 'Lona'), ('Lurex', 'Lurex'), ('Lurex metálico', 'Lurex metálico'), ('Lycra', 'Lycra'), ('Lyocell', 'Lyocell'), ('Madera', 'Madera'), ('Madera natural', 'Madera natural'), ('Merino', 'Merino'), ('Meryl', 'Meryl'), ('Mesh', 'Mesh'), ('Metal', 'Metal'), ('Metalizado', 'Metalizado'), ('Mezcla de fibras', 'Mezcla de fibras'), ('Microfibra', 'Microfibra'), ('Microfribra', 'Microfribra'), ('Micromodal', 'Micromodal'), ('Micropoliéster', 'Micropoliéster'), ('Mimbre', 'Mimbre'), ('Mineral', 'Mineral'), ('Mineral abovedado', 'Mineral abovedado'), ('Modacrilico', 'Modacrilico'), ('Modal', 'Modal'), ('Mohair', 'Mohair'), ('Mouton vuelto', 'Mouton vuelto'), ('Nailon', 'Nailon'), ('Napa', 'Napa'), ('Napa flor', 'Napa flor'), ('Napa sintética', 'Napa sintética'), ('Neopreno', 'Neopreno'), ('Nobuck', 'Nobuck'), ('Nylon', 'Nylon'), ('Nylon angora', 'Nylon angora'), ('Nylon mohair', 'Nylon mohair'), ('Nylon reciclado', 'Nylon reciclado'), ('Nylon taffeta', 'Nylon taffeta'), ('Nylour', 'Nylour'), ('Organza', 'Organza'), ('Oro', 'Oro'), ('Otros materiales', 'Otros materiales'), ('Paja', 'Paja'), ('Pana', 'Pana'), ('Papel', 'Papel'), ('Pelo', 'Pelo'), ('Piel becerro', 'Piel becerro'), ('Piel bovina', 'Piel bovina'), ('Piel Caprina', 'Piel Caprina'), ('Piel cordero', 'Piel cordero'), ('Piel de búfalo', 'Piel de búfalo'), ('Piel de potro', 'Piel de potro'), ('Piel equina', 'Piel equina'), ('Piel metalizada', 'Piel metalizada'), ('Piel napa', 'Piel napa'), ('Piel nobuck', 'Piel nobuck'), ('Piel ovina', 'Piel ovina'), ('Piel porcina', 'Piel porcina'), ('Piel serpiente', 'Piel serpiente'), ('Piel serraje', 'Piel serraje'), ('Piel vacuna', 'Piel vacuna'), ('Piel vegana', 'Piel vegana'), ('Piqué', 'Piqué'), ('Plástico', 'Plástico'), ('Plata', 'Plata'), ('Plata de ley', 'Plata de ley'), ('Pluma', 'Pluma'), ('Pluma natural', 'Pluma natural'), ('Plumas', 'Plumas'), ('Plumeti', 'Plumeti'), ('Plumón', 'Plumón'), ('Poliacrílico', 'Poliacrílico'), ('Poliamida', 'Poliamida'), ('Poliamida Chiffon', 'Poliamida Chiffon'), ('Policarbonato', 'Policarbonato'), ('Poliéster', 'Poliéster'), ('Poliéster eduction', 'Poliéster eduction'), ('Poliéster micro', 'Poliéster micro'), ('Poliéster reciclado', 'Poliéster reciclado'), ('Poliéster tricot', 'Poliéster tricot'), ('Poliéster, plain weave', 'Poliéster, plain weave'), ('Polietileno', 'Polietileno'), ('Polipropileno', 'Polipropileno'), ('Poliuretano', 'Poliuretano'), ('Polivinilcloruro', 'Polivinilcloruro'), ('Polivinilo', 'Polivinilo'), ('Poly memory', 'Poly memory'), ('Propileno', 'Propileno'), ('PU', 'PU'), ('Pulsera', 'Pulsera'), ('Pura lana virgen', 'Pura lana virgen'), ('PVC', 'PVC'), ('Rafia', 'Rafia'), ('Ramil', 'Ramil'), ('Ramio', 'Ramio'), ('Raso', 'Raso'), ('Ratio', 'Ratio'), ('Rayón', 'Rayón'), ('Resina', 'Resina'), ('Resina acrílica', 'Resina acrílica'), ('Resina de plástico', 'Resina de plástico'), ('Resina poliuretano', 'Resina poliuretano'), ('Rex', 'Rex'), ('Rodio', 'Rodio'), ('Satén', 'Satén'), ('Seda', 'Seda'), ('Seda natural', 'Seda natural'), ('Serraje', 'Serraje'), ('Silicona', 'Silicona'), ('Sinamay', 'Sinamay'), ('Sintético', 'Sintético'), ('Softshell', 'Softshell'), ('Spandex', 'Spandex'), ('T400', 'T400'), ('Tactel', 'Tactel'), ('Tecno-policarbonato', 'Tecno-policarbonato'), ('Tela', 'Tela'), ('Tencel', 'Tencel'), ('Terciopelo', 'Terciopelo'), ('Textil', 'Textil'), ('Thermocool Poliéster', 'Thermocool Poliéster'), ('Titanio', 'Titanio'), ('TPU Compacto', 'TPU Compacto'), ('Trevira', 'Trevira'), ('Tul', 'Tul'), ('Varias', 'Varias'), ('Velour', 'Velour'), ('Vinilo', 'Vinilo'), ('Viscosa', 'Viscosa'), ('Viscosa Modal', 'Viscosa Modal'), ('Visón', 'Visón'), ('XLA', 'XLA'), ('Yak', 'Yak'), ('Yute', 'Yute'), ('Zafiro', 'Zafiro'), ('Zamak', 'Zamak'), ('Zorro', 'Zorro')], 'Primer material exterior.')
    segundo_ext = fields.Selection([('Piel', 'Piel'), ('Ante', 'Ante'), ('Acero', 'Acero'), ('Acero brillo', 'Acero brillo'), ('Acero y Piedras', 'Acero y Piedras'), ('Acetato', 'Acetato'), ('Acrílico', 'Acrílico'), ('Afelpado', 'Afelpado'), ('Algodón', 'Algodón'), ('Algodón canvas', 'Algodón canvas'), ('Algodón egipcio', 'Algodón egipcio'), ('Algodón encerado', 'Algodón encerado'), ('Algodón felpa francesa', 'Algodón felpa francesa'), ('Algodón jersey', 'Algodón jersey'), ('Algodón modal', 'Algodón modal'), ('Algodón orgánico', 'Algodón orgánico'), ('Algodón peinado', 'Algodón peinado'), ('Algodón pima', 'Algodón pima'), ('Algodón Voile', 'Algodón Voile'), ('Alpaca', 'Alpaca'), ('Aluminio', 'Aluminio'), ('Angora', 'Angora'), ('Arcilla', 'Arcilla'), ('Armys', 'Armys'), ('Bamboo', 'Bamboo'), ('Bambú', 'Bambú'), ('Box', 'Box'), ('Cachemire', 'Cachemire'), ('Cañamo', 'Cañamo'), ('Cáñamo', 'Cáñamo'), ('Carey', 'Carey'), ('Cashemire', 'Cashemire'), ('Cashmere', 'Cashmere'), ('Caucho', 'Caucho'), ('Caucho vulcanizado', 'Caucho vulcanizado'), ('Celulosa', 'Celulosa'), ('Cerámica', 'Cerámica'), ('Chapado', 'Chapado'), ('Charol', 'Charol'), ('Conejo', 'Conejo'), ('Coolmax', 'Coolmax'), ('Crystal Mesh', 'Crystal Mesh'), ('Cuero', 'Cuero'), ('Cuero sintético', 'Cuero sintético'), ('Cuero sintético ecológico', 'Cuero sintético ecológico'), ('Cuero vegetal', 'Cuero vegetal'), ('Cupro', 'Cupro'), ('Dralón', 'Dralón'), ('Ecopiel', 'Ecopiel'), ('Elastán', 'Elastán'), ('Elastano', 'Elastano'), ('Elastano double-weave twill', 'Elastano double-weave twill'), ('Elastodieno', 'Elastodieno'), ('Elastomero', 'Elastomero'), ('Elastomultiester', 'Elastomultiester'), ('Esparto', 'Esparto'), ('Etil-Vinil-Acetato (EVA)', 'Etil-Vinil-Acetato (EVA)'), ('EVA', 'EVA'), ('EVA celular', 'EVA celular'), ('EVA Foam', 'EVA Foam'), ('EVA moldeada', 'EVA moldeada'), ('Felpa', 'Felpa'), ('Latex', 'Latex'), ('Linen', 'Linen'), ('Lino', 'Lino'), ('Liocel', 'Liocel'), ('Lona', 'Lona'), ('Lurex', 'Lurex'), ('Lurex metálico', 'Lurex metálico'), ('Lycra', 'Lycra'), ('Lyocell', 'Lyocell'), ('Madera', 'Madera'), ('Madera natural', 'Madera natural'), ('Merino', 'Merino'), ('Meryl', 'Meryl'), ('Mesh', 'Mesh'), ('Metal', 'Metal'), ('Metalizado', 'Metalizado'), ('Mezcla de fibras', 'Mezcla de fibras'), ('Microfibra', 'Microfibra'), ('Microfribra', 'Microfribra'), ('Micromodal', 'Micromodal'), ('Micropoliéster', 'Micropoliéster'), ('Mimbre', 'Mimbre'), ('Mineral', 'Mineral'), ('Mineral abovedado', 'Mineral abovedado'), ('Modacrilico', 'Modacrilico'), ('Modal', 'Modal'), ('Mohair', 'Mohair'), ('Mouton vuelto', 'Mouton vuelto'), ('Nailon', 'Nailon'), ('Napa', 'Napa'), ('Napa flor', 'Napa flor'), ('Napa sintética', 'Napa sintética'), ('Neopreno', 'Neopreno'), ('Nobuck', 'Nobuck'), ('Nylon', 'Nylon'), ('Nylon angora', 'Nylon angora'), ('Nylon mohair', 'Nylon mohair'), ('Nylon reciclado', 'Nylon reciclado'), ('Nylon taffeta', 'Nylon taffeta'), ('Nylour', 'Nylour'), ('Organza', 'Organza'), ('Oro', 'Oro'), ('Otros materiales', 'Otros materiales'), ('Paja', 'Paja'), ('Pana', 'Pana'), ('Papel', 'Papel'), ('Pelo', 'Pelo'), ('Piel becerro', 'Piel becerro'), ('Piel bovina', 'Piel bovina'), ('Piel Caprina', 'Piel Caprina'), ('Piel cordero', 'Piel cordero'), ('Piel de búfalo', 'Piel de búfalo'), ('Piel de potro', 'Piel de potro'), ('Piel equina', 'Piel equina'), ('Piel metalizada', 'Piel metalizada'), ('Piel napa', 'Piel napa'), ('Piel nobuck', 'Piel nobuck'), ('Piel ovina', 'Piel ovina'), ('Piel porcina', 'Piel porcina'), ('Piel serpiente', 'Piel serpiente'), ('Piel serraje', 'Piel serraje'), ('Piel vacuna', 'Piel vacuna'), ('Piel vegana', 'Piel vegana'), ('Piqué', 'Piqué'), ('Plástico', 'Plástico'), ('Plata', 'Plata'), ('Plata de ley', 'Plata de ley'), ('Pluma', 'Pluma'), ('Pluma natural', 'Pluma natural'), ('Plumas', 'Plumas'), ('Plumeti', 'Plumeti'), ('Plumón', 'Plumón'), ('Poliacrílico', 'Poliacrílico'), ('Poliamida', 'Poliamida'), ('Poliamida Chiffon', 'Poliamida Chiffon'), ('Policarbonato', 'Policarbonato'), ('Poliéster', 'Poliéster'), ('Poliéster eduction', 'Poliéster eduction'), ('Poliéster micro', 'Poliéster micro'), ('Poliéster reciclado', 'Poliéster reciclado'), ('Poliéster tricot', 'Poliéster tricot'), ('Poliéster, plain weave', 'Poliéster, plain weave'), ('Polietileno', 'Polietileno'), ('Polipropileno', 'Polipropileno'), ('Poliuretano', 'Poliuretano'), ('Polivinilcloruro', 'Polivinilcloruro'), ('Polivinilo', 'Polivinilo'), ('Poly memory', 'Poly memory'), ('Propileno', 'Propileno'), ('PU', 'PU'), ('Pulsera', 'Pulsera'), ('Pura lana virgen', 'Pura lana virgen'), ('PVC', 'PVC'), ('Rafia', 'Rafia'), ('Ramil', 'Ramil'), ('Ramio', 'Ramio'), ('Raso', 'Raso'), ('Ratio', 'Ratio'), ('Rayón', 'Rayón'), ('Resina', 'Resina'), ('Resina acrílica', 'Resina acrílica'), ('Resina de plástico', 'Resina de plástico'), ('Resina poliuretano', 'Resina poliuretano'), ('Rex', 'Rex'), ('Rodio', 'Rodio'), ('Satén', 'Satén'), ('Seda', 'Seda'), ('Seda natural', 'Seda natural'), ('Serraje', 'Serraje'), ('Silicona', 'Silicona'), ('Sinamay', 'Sinamay'), ('Sintético', 'Sintético'), ('Softshell', 'Softshell'), ('Spandex', 'Spandex'), ('T400', 'T400'), ('Tactel', 'Tactel'), ('Tecno-policarbonato', 'Tecno-policarbonato'), ('Tela', 'Tela'), ('Tencel', 'Tencel'), ('Terciopelo', 'Terciopelo'), ('Textil', 'Textil'), ('Thermocool Poliéster', 'Thermocool Poliéster'), ('Titanio', 'Titanio'), ('TPU Compacto', 'TPU Compacto'), ('Trevira', 'Trevira'), ('Tul', 'Tul'), ('Varias', 'Varias'), ('Velour', 'Velour'), ('Vinilo', 'Vinilo'), ('Viscosa', 'Viscosa'), ('Viscosa Modal', 'Viscosa Modal'), ('Visón', 'Visón'), ('XLA', 'XLA'), ('Yak', 'Yak'), ('Yute', 'Yute'), ('Zafiro', 'Zafiro'), ('Zamak', 'Zamak'), ('Zorro', 'Zorro')], 'Segundo material exterior.')
    tercero_ext = fields.Selection([('Piel', 'Piel'), ('Ante', 'Ante'), ('Acero', 'Acero'), ('Acero brillo', 'Acero brillo'), ('Acero y Piedras', 'Acero y Piedras'), ('Acetato', 'Acetato'), ('Acrílico', 'Acrílico'), ('Afelpado', 'Afelpado'), ('Algodón', 'Algodón'), ('Algodón canvas', 'Algodón canvas'), ('Algodón egipcio', 'Algodón egipcio'), ('Algodón encerado', 'Algodón encerado'), ('Algodón felpa francesa', 'Algodón felpa francesa'), ('Algodón jersey', 'Algodón jersey'), ('Algodón modal', 'Algodón modal'), ('Algodón orgánico', 'Algodón orgánico'), ('Algodón peinado', 'Algodón peinado'), ('Algodón pima', 'Algodón pima'), ('Algodón Voile', 'Algodón Voile'), ('Alpaca', 'Alpaca'), ('Aluminio', 'Aluminio'), ('Angora', 'Angora'), ('Arcilla', 'Arcilla'), ('Armys', 'Armys'), ('Bamboo', 'Bamboo'), ('Bambú', 'Bambú'), ('Box', 'Box'), ('Cachemire', 'Cachemire'), ('Cañamo', 'Cañamo'), ('Cáñamo', 'Cáñamo'), ('Carey', 'Carey'), ('Cashemire', 'Cashemire'), ('Cashmere', 'Cashmere'), ('Caucho', 'Caucho'), ('Caucho vulcanizado', 'Caucho vulcanizado'), ('Celulosa', 'Celulosa'), ('Cerámica', 'Cerámica'), ('Chapado', 'Chapado'), ('Charol', 'Charol'), ('Conejo', 'Conejo'), ('Coolmax', 'Coolmax'), ('Crystal Mesh', 'Crystal Mesh'), ('Cuero', 'Cuero'), ('Cuero sintético', 'Cuero sintético'), ('Cuero sintético ecológico', 'Cuero sintético ecológico'), ('Cuero vegetal', 'Cuero vegetal'), ('Cupro', 'Cupro'), ('Dralón', 'Dralón'), ('Ecopiel', 'Ecopiel'), ('Elastán', 'Elastán'), ('Elastano', 'Elastano'), ('Elastano double-weave twill', 'Elastano double-weave twill'), ('Elastodieno', 'Elastodieno'), ('Elastomero', 'Elastomero'), ('Elastomultiester', 'Elastomultiester'), ('Esparto', 'Esparto'), ('Etil-Vinil-Acetato (EVA)', 'Etil-Vinil-Acetato (EVA)'), ('EVA', 'EVA'), ('EVA celular', 'EVA celular'), ('EVA Foam', 'EVA Foam'), ('EVA moldeada', 'EVA moldeada'), ('Felpa', 'Felpa'), ('Latex', 'Latex'), ('Linen', 'Linen'), ('Lino', 'Lino'), ('Liocel', 'Liocel'), ('Lona', 'Lona'), ('Lurex', 'Lurex'), ('Lurex metálico', 'Lurex metálico'), ('Lycra', 'Lycra'), ('Lyocell', 'Lyocell'), ('Madera', 'Madera'), ('Madera natural', 'Madera natural'), ('Merino', 'Merino'), ('Meryl', 'Meryl'), ('Mesh', 'Mesh'), ('Metal', 'Metal'), ('Metalizado', 'Metalizado'), ('Mezcla de fibras', 'Mezcla de fibras'), ('Microfibra', 'Microfibra'), ('Microfribra', 'Microfribra'), ('Micromodal', 'Micromodal'), ('Micropoliéster', 'Micropoliéster'), ('Mimbre', 'Mimbre'), ('Mineral', 'Mineral'), ('Mineral abovedado', 'Mineral abovedado'), ('Modacrilico', 'Modacrilico'), ('Modal', 'Modal'), ('Mohair', 'Mohair'), ('Mouton vuelto', 'Mouton vuelto'), ('Nailon', 'Nailon'), ('Napa', 'Napa'), ('Napa flor', 'Napa flor'), ('Napa sintética', 'Napa sintética'), ('Neopreno', 'Neopreno'), ('Nobuck', 'Nobuck'), ('Nylon', 'Nylon'), ('Nylon angora', 'Nylon angora'), ('Nylon mohair', 'Nylon mohair'), ('Nylon reciclado', 'Nylon reciclado'), ('Nylon taffeta', 'Nylon taffeta'), ('Nylour', 'Nylour'), ('Organza', 'Organza'), ('Oro', 'Oro'), ('Otros materiales', 'Otros materiales'), ('Paja', 'Paja'), ('Pana', 'Pana'), ('Papel', 'Papel'), ('Pelo', 'Pelo'), ('Piel becerro', 'Piel becerro'), ('Piel bovina', 'Piel bovina'), ('Piel Caprina', 'Piel Caprina'), ('Piel cordero', 'Piel cordero'), ('Piel de búfalo', 'Piel de búfalo'), ('Piel de potro', 'Piel de potro'), ('Piel equina', 'Piel equina'), ('Piel metalizada', 'Piel metalizada'), ('Piel napa', 'Piel napa'), ('Piel nobuck', 'Piel nobuck'), ('Piel ovina', 'Piel ovina'), ('Piel porcina', 'Piel porcina'), ('Piel serpiente', 'Piel serpiente'), ('Piel serraje', 'Piel serraje'), ('Piel vacuna', 'Piel vacuna'), ('Piel vegana', 'Piel vegana'), ('Piqué', 'Piqué'), ('Plástico', 'Plástico'), ('Plata', 'Plata'), ('Plata de ley', 'Plata de ley'), ('Pluma', 'Pluma'), ('Pluma natural', 'Pluma natural'), ('Plumas', 'Plumas'), ('Plumeti', 'Plumeti'), ('Plumón', 'Plumón'), ('Poliacrílico', 'Poliacrílico'), ('Poliamida', 'Poliamida'), ('Poliamida Chiffon', 'Poliamida Chiffon'), ('Policarbonato', 'Policarbonato'), ('Poliéster', 'Poliéster'), ('Poliéster eduction', 'Poliéster eduction'), ('Poliéster micro', 'Poliéster micro'), ('Poliéster reciclado', 'Poliéster reciclado'), ('Poliéster tricot', 'Poliéster tricot'), ('Poliéster, plain weave', 'Poliéster, plain weave'), ('Polietileno', 'Polietileno'), ('Polipropileno', 'Polipropileno'), ('Poliuretano', 'Poliuretano'), ('Polivinilcloruro', 'Polivinilcloruro'), ('Polivinilo', 'Polivinilo'), ('Poly memory', 'Poly memory'), ('Propileno', 'Propileno'), ('PU', 'PU'), ('Pulsera', 'Pulsera'), ('Pura lana virgen', 'Pura lana virgen'), ('PVC', 'PVC'), ('Rafia', 'Rafia'), ('Ramil', 'Ramil'), ('Ramio', 'Ramio'), ('Raso', 'Raso'), ('Ratio', 'Ratio'), ('Rayón', 'Rayón'), ('Resina', 'Resina'), ('Resina acrílica', 'Resina acrílica'), ('Resina de plástico', 'Resina de plástico'), ('Resina poliuretano', 'Resina poliuretano'), ('Rex', 'Rex'), ('Rodio', 'Rodio'), ('Satén', 'Satén'), ('Seda', 'Seda'), ('Seda natural', 'Seda natural'), ('Serraje', 'Serraje'), ('Silicona', 'Silicona'), ('Sinamay', 'Sinamay'), ('Sintético', 'Sintético'), ('Softshell', 'Softshell'), ('Spandex', 'Spandex'), ('T400', 'T400'), ('Tactel', 'Tactel'), ('Tecno-policarbonato', 'Tecno-policarbonato'), ('Tela', 'Tela'), ('Tencel', 'Tencel'), ('Terciopelo', 'Terciopelo'), ('Textil', 'Textil'), ('Thermocool Poliéster', 'Thermocool Poliéster'), ('Titanio', 'Titanio'), ('TPU Compacto', 'TPU Compacto'), ('Trevira', 'Trevira'), ('Tul', 'Tul'), ('Varias', 'Varias'), ('Velour', 'Velour'), ('Vinilo', 'Vinilo'), ('Viscosa', 'Viscosa'), ('Viscosa Modal', 'Viscosa Modal'), ('Visón', 'Visón'), ('XLA', 'XLA'), ('Yak', 'Yak'), ('Yute', 'Yute'), ('Zafiro', 'Zafiro'), ('Zamak', 'Zamak'), ('Zorro', 'Zorro')], 'Tercero material exterior.')

    tipo_de_cierre = fields.Selection([('Cremallera','Cremallera'), ('Hebilla','Hebilla'), ('Velcro','Velcro'), ('Cordones','Cordones'), ('Elastico', 'Elastico'), ('A Tubo', 'A Tubo'), ('Anudado', 'Anudado')], 'Tipo de cierre')
    material_principal = fields.Selection([('ALGODON', 'ALGODON'), ('ANTE', 'ANTE'), ('ECOPIEL', 'ECOPIEL'), ('NAPA', 'NAPA'), ('NOBUCK', 'NOBUCK'), ('OTROS MATERIALES', 'OTROS MATERIALES'), ('PIEL', 'PIEL'), ('PIEL VEGANA', 'PIEL VEGANA'), ('SERRAJE', 'SERRAJE'), ('SINTETICO', 'SINTETICO'), ('TEXTIL', 'TEXTIL')], 'Material principal')
    alto_cana = fields.Selection([('baja','baja'), ('media','media'), ('alta','alta')], 'Alto Caña')
    
    # BOOLEANOS

    producir = fields.Boolean('¿Aprobado para producir?')
    mostrar_modelo = fields.Boolean('Marcar como principal')
    
    # BNARIOS

    boceto_nvm = fields.Image("Boceto", help="Seleccionar Boceto")
    logo_marca_nvm = fields.Image("Logo", help="Logo de la marca")
    modelo_real_nvm = fields.Image("Foto Modelo", help="Seleccionar Modelo")
    
    pdf_nvm = fields.Binary("Documento carta color", help="Seleccionar documento")

    # RELACIONALES

    carta_color_nvm = fields.Many2one('cartacoloresnavima.cartacoloresnavima', 'Carta de color')
    horma_nvm = fields.Many2one('horma.horma', 'Horma')
    categoria_producto_nvm = fields.Many2one('product.category', 'Categoría de producto')
    old_stage_id = fields.Many2one('nvm_design.stage', string='Old stage')
    muestras = fields.One2many('muestras.navima.color', 'diseno_id', string="Muestras")
    cash_conversion = fields.Many2one('cash.conversion', 'Marca of CashConversion')
    hs_code = fields.Many2one('hs.master', 'Código Aduanero')
    tipo_de_producto = fields.Many2one('tipo.producto', string='Tipo de producto')

    tarifa = fields.Many2one('product.pricelist', 'Tarifa EUR')
    tarifa_usd = fields.Many2one('product.pricelist', 'Tarifa USD')
    tarifa_fob = fields.Many2one('product.pricelist', 'Tarifa F.O.B')
    tarifa_wholesalers = fields.Many2one('product.pricelist', 'Tarifa EUR')
    tarifa_wholesalers_usd = fields.Many2one('product.pricelist', 'Tarifa USD')

    moneda_del_proveedor = fields.Many2one('res.currency', string='Moneda del proveedor')

    material_principal_nvm = fields.Many2one('materiales.materiales', 'Material Principal')

    materiales = fields.Many2many(
        'materialporcentaje',
        string='Composición corte'
    )

    # OTROS CAMPOS

    carta_color_referencia = fields.Char("Carta color referencia interna")
    equipment_id = fields.Many2one('design.equipment', string='Equipment', ondelete='restrict', index=True, check_company=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    description = fields.Text('Description')
    request_date = fields.Date('Request Date', default=fields.Date.context_today, help="Date requested for the design to happen")
    owner_user_id = fields.Many2one('res.users', string='Created by User', default=lambda s: s.env.uid)
    user_id = fields.Many2one('res.users', string='Technician')
    stage_id = fields.Many2one('nvm_design.stage', string='Stage', ondelete='restrict', tracking=True, group_expand='_read_group_stage_ids', default=_default_stage, copy=False)

    priority = fields.Selection([('0', 'Muy baja'), ('1', 'Baja'), ('2', 'Normal'), ('3', 'Alta')], string='Prioridad')
    color = fields.Integer('Indice de color')
    close_date = fields.Date('Close Date', help="Date the design was finished. ")
    kanban_state = fields.Selection([('normal', 'In Progress'), ('blocked', 'Blocked'), ('done', 'Ready for next stage')],
                                    string='Kanban State', required=True, default='normal')
    archive = fields.Boolean(default=False, help="Archivar para esconder el boceto de la vista de diseño sin eliminarlo.")
    design_type = fields.Selection([('corrective', 'Corrective'), ('preventive', 'Preventive')], string='Design Type', default="corrective")
    schedule_date = fields.Datetime('Scheduled Date', help="Date the design team plans the design.  It should not differ much from the Request Date. ")
    design_team_id = fields.Many2one('design.team', string='Team', required=True, default=_get_default_team_id, check_company=True)
    duration = fields.Float(help="Duration in hours.")
    done = fields.Boolean(related='stage_id.done')

    # ACTUADORES

    @api.onchange('carta_color_nvm')
    def _valor_moneda_proveedor(self):

        #moneda = self.carta_color_nvm.proveedor.property_purchase_currency_id
        self.coleccion = self.carta_color_nvm.coleccion
        self.carta_color_referencia = self.carta_color_nvm.codigo_material_interno
        self.tipo_de_producto = self.carta_color_nvm.material.tipo_de_producto


    @api.onchange('coleccion')
    def _onchange_coleccion(self):

        try:

            self.logo_marca_nvm = self.coleccion.logo_marca

        except ValueError:

            pass


    @api.onchange('coste_propuesto')
    def _onchange_coste_propuesto(self):

        coleccion_calcular_precio = self.carta_color_nvm.coleccion
        multiplo_a_convertir = coleccion_calcular_precio.cash_conversion.multiplo_a_convertir
        multiplo_conversion = coleccion_calcular_precio.cash_conversion.multiplo_conversion
        _carta_color = self.env['cartacoloresnavima.cartacoloresnavima'].browse(self.carta_color_nvm.id)

        tp_multiplicador = _carta_color.material.tipo_de_producto.multiplo_precio

        if float(self.coste_propuesto) > 0 and float(coleccion_calcular_precio.multiplicador) > 0:

            self.coste_final_propuesto = self.coste_propuesto * tp_multiplicador
            self.precio_propuesto = (self.coste_propuesto * tp_multiplicador) * coleccion_calcular_precio.multiplicador

    
    @api.onchange('precio')
    def _onchange_precio(self):

        coleccion_calcular_precio = self.carta_color_nvm.coleccion
        multiplo_conversion = coleccion_calcular_precio.cash_conversion.multiplo_conversion
        _carta_color = self.env['cartacoloresnavima.cartacoloresnavima'].browse(self.carta_color_nvm.id)

        tp_multiplicador = _carta_color.material.tipo_de_producto.multiplo_precio

        if float(self.precio) > 0 and float(coleccion_calcular_precio.multiplicador) > 0:

            _coste_base = self.precio / coleccion_calcular_precio.multiplicador
            self.coste = _coste_base / tp_multiplicador

            self.coste_final = self.coste * tp_multiplicador
            self.precio_usa = (self.precio * multiplo_conversion) * coleccion_calcular_precio.multiplicador_usa
            self.precio_it = ((self.coste + self.extra_cost) * coleccion_calcular_precio.multiplicador_fob) * multiplo_conversion #F.O.B
            self.precio_pvr = (self.precio + self.extra_cost) * coleccion_calcular_precio.multiplicador_pvr
            self.precio_usa_pvr = self.precio_usa * coleccion_calcular_precio.multiplicador_usa_pvr

            _coste_base = _coste_base - self.extra_cost


    @api.onchange('categoria_producto_nvm', 'carta_color_nvm', 'primero_ext', 'product_name_nvm', 'atributo_con', 'horma_nvm')
    def _onchange_attfordescriprion(self):

        desc_categoria_zalzado = self.categoria_producto_nvm.name
        desc_marca = self.carta_color_nvm.marca.name
        desc_material_exterior = self.primero_ext
        desc_nombre_web = self.product_name_nvm
        desc_atributo_con = self.atributo_con
        desc_altura_cana = self.alto_cana
        desc_tacon_tipo = self.horma_nvm.tipo_de_tacon_nvm
        desc_altura_tacon = self.horma_nvm.alto_tacon_nvm
        desc_tipo_plataforma = self.horma_nvm.tipo_de_material_plataforma_nvm
        desc_altura_plataforma = self.horma_nvm.plataforma_nvm
        desc_puntera = self.horma_nvm.tipo_de_puntera_nvm

        descripcion_final = ""

        if self.categoria_producto_nvm.name:

            descripcion_final = descripcion_final + str(self.categoria_producto_nvm.name) + " "

        if self.carta_color_nvm.marca.name:

            descripcion_final = descripcion_final + str(self.carta_color_nvm.marca.name) + " "
        
        if self.primero_ext:

            descripcion_final = descripcion_final + " de " + str(self.primero_ext) + ". "

        if self.product_name_nvm: 

            descripcion_final = descripcion_final + str(self.product_name_nvm) + " "

        if self.atributo_con:

            descripcion_final = descripcion_final + " con " + str(self.atributo_con) + ". "

        if self.alto_cana:

            descripcion_final = descripcion_final + "Altura de caña " + str(self.alto_cana) + " "

        if self.horma_nvm.tipo_de_tacon_nvm:

            descripcion_final = descripcion_final + "con tacón de " + str(self.horma_nvm.tipo_de_tacon_nvm) + " "

        if self.horma_nvm.alto_tacon_nvm:

            descripcion_final = descripcion_final + "de " + str(self.horma_nvm.alto_tacon_nvm) + "cm, "

        if self.horma_nvm.tipo_de_material_plataforma_nvm:

            descripcion_final = descripcion_final + "con plataforma de " + str(self.horma_nvm.tipo_de_material_plataforma_nvm) + " "
        
        if self.horma_nvm.plataforma_nvm:

            descripcion_final = descripcion_final + "de " + str(self.horma_nvm.plataforma_nvm) + "cm "

        if self.horma_nvm.tipo_de_puntera_nvm:

            descripcion_final = descripcion_final + "con punta " + str(self.horma_nvm.tipo_de_puntera_nvm)

        self.descripcion_web = descripcion_final


    #agentes_colores = [{
    #    'agente': 'mateo',
    #    'colores': [{'color': 'Rojo', 'checked': True}, {'color': 'Azul', 'checked': False}, {'color': 'Verde', 'checked': True}]
    #},
    #{
    #    'agente': 'marta',
    #    'colores': [{'color': 'Rojo', 'checked': False}, {'color': 'Azul', 'checked': True}, {'color': 'Verde', 'checked': False}]
    #}]
    

    @api.depends('muestras')
    def _depends_muestras(self):

        self.actualizar_muestras()


    @api.onchange('agentes_design')
    def _onchange_agentes(self):
        pass


    @api.onchange('modelo_base_nvm', 'carta_color_nvm')
    def _onchange_modelo_base_nvm_carta_color(self):
        id_carta = self.carta_color_nvm.id
        if int(self.carta_color_nvm.id) > 0 and self.modelo_base_nvm != "":
            carta_color = self.env['cartacoloresnavima.cartacoloresnavima'].browse(id_carta)
            self.carta_color_modelo_base = str(self.modelo_base_nvm) + str(carta_color.material.cod_material)
        else:
            self.carta_color_modelo_base = "----"


    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        stage = self.env['nvm_design.stage'].browse(self.stage_id.id)
        nombre_etapa = stage.name
        carta_color = self.env['cartacoloresnavima.cartacoloresnavima'].browse(self.carta_color_nvm.id)

        comprobante = {
            'carta_color_nvm': False,
            'modelo_base_nvm': False,
            'name': False,
            'horma_nvm': False,
            'variante_de_horma_nvm': False,
            'boceto_nvm': False,
            'categoria_producto_nvm': False
        }

        for campo in comprobante:
            if self[campo]:
                comprobante[campo] = True

        if nombre_etapa == "Solicitud de prototipo":

            if comprobante['categoria_producto_nvm'] == True and comprobante['name'] == True and comprobante['boceto_nvm'] == True:
                pass

            else:
                campos_a_completar = ''
                for campo in comprobante:
                    if campo == 'categoria_producto_nvm' or campo == 'name' or campo == 'boceto_nvm':
                        if not self[campo]:
                            campos_a_completar = str(campos_a_completar) + str(campo) + ', '

                campos_a_completar = str(campos_a_completar[:-2])
                campos_a_completar = campos_a_completar + '.'
                campos_a_completar = 'Tienes que completar los siguientes campos: ' + str(campos_a_completar) + ' Una vez completados podrás cambiar el boceto a "Recepción de prototipo".'
                warning = {
                    'title': "¡Faltan campos!",
                    'message': str(campos_a_completar),
                }

                self.kanban_state = 'blocked'

                return {'warning': warning }

        if nombre_etapa == "Recepción de prototipo":

            if comprobante['categoria_producto_nvm'] == True and comprobante['name'] == True and comprobante['boceto_nvm'] == True:
                pass

            else:
                campos_a_completar = ''
                for campo in comprobante:
                    if campo == 'categoria_producto_nvm' or campo == 'name' or campo == 'boceto_nvm':
                        if not self[campo]:
                            campos_a_completar = str(campos_a_completar) + str(campo) + ', '

                campos_a_completar = str(campos_a_completar[:-2])
                campos_a_completar = campos_a_completar + '.'
                campos_a_completar = 'Tienes que completar los siguientes campos: ' + str(campos_a_completar) + ' Una vez completados podrás cambiar el boceto a "Recepción de prototipo".'
                warning = {
                    'title': "¡Faltan campos!",
                    'message': str(campos_a_completar),
                }

                self.kanban_state = 'blocked'

                return {'warning': warning }

        if nombre_etapa == "Solicitud muestra agentes":

            if comprobante['categoria_producto_nvm'] == True and comprobante['carta_color_nvm'] == True and comprobante['modelo_base_nvm'] == True and comprobante['name'] == True and comprobante['variante_de_horma_nvm'] == True and comprobante['horma_nvm'] == True and comprobante['boceto_nvm'] == True:
                pass

            else:
                campos_a_completar = ''
                for campo in comprobante:
                    if not self[campo]:
                        campos_a_completar = str(campos_a_completar) + str(campo) + ', '

                campos_a_completar = str(campos_a_completar[:-2])
                campos_a_completar = campos_a_completar + '.'
                campos_a_completar = 'Tienes que completar los siguientes campos: ' + str(campos_a_completar) + ' Una vez completados podrás cambiar el boceto a "Solicitud muestra agentes".'
                warning = {
                    'title': "¡Faltan campos!",
                    'message': str(campos_a_completar),
                }

                self.kanban_state = 'blocked'

                return {'warning': warning }

        if nombre_etapa == "Muestras de agentes":

            if comprobante['categoria_producto_nvm'] == True and comprobante['carta_color_nvm'] == True and comprobante['modelo_base_nvm'] == True and comprobante['name'] == True and comprobante['variante_de_horma_nvm'] == True and comprobante['horma_nvm'] == True and comprobante['boceto_nvm'] == True:
                
                pass

            else:

                campos_a_completar = ''
                for campo in comprobante:
                    if not self[campo]:
                        campos_a_completar = str(campos_a_completar) + str(campo) + ', '

                campos_a_completar = str(campos_a_completar[:-2])
                campos_a_completar = campos_a_completar + '.'
                campos_a_completar = 'Tienes que completar los siguientes campos: ' + str(campos_a_completar) + ' Una vez completados podrás cambiar el boceto a "Muestras de agentes".'
                warning = {
                    'title': "¡Faltan campos!",
                    'message': str(campos_a_completar),
                }

                self.kanban_state = 'blocked'

                return {'warning': warning }

        
        if nombre_etapa == "Producir":

            if not self.producir:

                warning = {
                    'title': "No se puede completar la operación.",
                    'message': "El boceto " + str(self.name) + ". No está aprobado para producción. Apruebalo para poder producirlo."
                }

                self.kanban_state = 'blocked'

                return {'warning': warning}

            else:

                if comprobante['categoria_producto_nvm'] == True and comprobante['carta_color_nvm'] == True and comprobante['modelo_base_nvm'] == True and comprobante['name'] == True and comprobante['variante_de_horma_nvm'] == True and comprobante['horma_nvm'] == True and comprobante['boceto_nvm'] == True:
                    team = self.env['design.team'].browse(self.design_team_id.id)
                    coleccion = self.env['colecciones.colecciones'].browse(team.coleccion_nvm.id)
                    carta_color_nuevo_producto = self.env['cartacoloresnavima.cartacoloresnavima'].browse(self.carta_color_nvm.id)

                    nombre_nuevo_producto = str(self.modelo_base_nvm) + str(self.carta_color_referencia) + " - " + str(self.coleccion.temporada) + " - D"

                    uom = self.env['uom.uom'].search([('name', '=', 'Pares')])

                    tmpl_id = self.env['product.template'].create({'name': nombre_nuevo_producto,
                                                        'marca_modelo_navima': self.coleccion.marca_nvm.id,
                                                        'carta_color_navima': self.carta_color_nvm.id,
                                                        'modelo_navima': str(self.modelo_base_nvm) + str(self.carta_color_referencia),
                                                        'horma_nvm': self.horma_nvm.id,
                                                        'type': 'product',
                                                        'route_ids': [(6, 0, [1, 5])],
                                                        'medidas_navima': self.modelo_base_nvm,
                                                        'coleccion_nvm': self.coleccion.id,
                                                        'tracking': 'lot',
                                                        'list_price': self.precio_pvp,
                                                        'sku_navima': self.id,
                                                        'can_be_expensed': True,
                                                        'image_1920': self.modelo_real_nvm,
                                                        'foto_marca': self.coleccion.logo_marca,
                                                        'categ_id': self.categoria_producto_nvm.id,
                                                        'product_add_mode': 'matrix',
                                                        'standard_price': self.coste,
                                                        'coste': self.coste,
                                                        'uom_id': uom.id,
                                                        'uom_po_id': uom.id,
                                                        'coste_final': self.coste_final,
                                                        'coste_propuesto': self.coste_propuesto,
                                                        'coste_final_propuesto': self.coste_final_propuesto,
                                                        'precio_propuesto': self.precio_propuesto,
                                                        'extra_cost': self.extra_cost,
                                                        'precio_usa': self.precio_usa,
                                                        'precio_it': self.precio_it,
                                                        'precio_final': self.precio_final,
                                                        'precio_final_usa': self.precio_final_usa,
                                                        'precio_final_it': self.precio_final_it,
                                                        'precio_pvr': self.precio_pvr,
                                                        'precio_usa_pvr': self.precio_usa_pvr,
                                                        'precio_pvp': self.precio_pvp,
                                                        'precio_usa_pvp': self.precio_usa_pvp,
                                                        #'moneda_del_proveedor': self.carta_color_nvm.proveedor.property_purchase_currency_id,
                                                        'precio': self.precio_final
                                                        })

                                                        

                    _carta_color = self.env['cartacoloresnavima.cartacoloresnavima'].browse(self.carta_color_nvm.id)
                    moneda_del_proveedor = self.carta_color_nvm.proveedor.property_purchase_currency_id.id  # en sp se llama currency_id, es un m20 para currency.
                    tiempo_inicial_de_entrega = 5                                                           # en sp se llama delay, es un entero.
                    cantidad_minima = 1.0                                                                   # en sp se llama min_qty, es float.
                    proveedor = _carta_color.proveedor.id                                         # en sp se llama name, es m2o para el contacto.
                    precio = self.coste_final                                                      # en sp se llama price, es un float.
                    product_tmpl_id = tmpl_id.id                                                               # en sp se llama product_tmpl_id, es m2o para la plantilla del producto.
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

                    # TARIFA WHOLESALERS EUR

                    id_tarifa_item_whslr_eur = self.env['product.pricelist.item'].create({
                        'applied_on': '1_product',
                        'compute_price': 'fixed',
                        'currency_id': 1,
                        'pricelist_id': _carta_color.coleccion.tarifa_wholesalers.id,
                        'product_tmpl_id': product_tmpl_id,
                        'fixed_price': self.precio_final
                    })

                    # TARIFA WHOLESALERS USD

                    id_tarifa_item_whslr_usd = self.env['product.pricelist.item'].create({
                        'applied_on': '1_product',
                        'compute_price': 'fixed',
                        'currency_id': 2,
                        'pricelist_id': _carta_color.coleccion.tarifa_wholesalers_usd.id,
                        'product_tmpl_id': product_tmpl_id,
                        'fixed_price': self.precio_final_usa
                    })

                    # TARIFA WHOLESALERS F.O.B

                    id_tarifa_item_whslr_fob = self.env['product.pricelist.item'].create({
                        'applied_on': '1_product',
                        'compute_price': 'fixed',
                        'currency_id': 2,
                        'pricelist_id': _carta_color.coleccion.tarifa_fob.id,
                        'product_tmpl_id': product_tmpl_id,
                        'fixed_price': self.precio_final_it
                    })

                    # TARIFA PVP EUR

                    id_tarifa_item_pvp_eur = self.env['product.pricelist.item'].create({
                        'applied_on': '1_product',
                        'compute_price': 'fixed',
                        'currency_id': 1,
                        'pricelist_id': _carta_color.coleccion.tarifa.id,
                        'product_tmpl_id': product_tmpl_id,
                        'fixed_price': self.precio_pvp
                    })

                    # TARIFA PVP USD

                    id_tarifa_item_pvp_usd = self.env['product.pricelist.item'].create({
                        'applied_on': '1_product',
                        'compute_price': 'fixed',
                        'currency_id': 2,
                        'pricelist_id': _carta_color.coleccion.tarifa_usd.id,
                        'product_tmpl_id': product_tmpl_id,
                        'fixed_price': self.precio_usa_pvp
                    })
                                                        
                    self.kanban_state = 'done'

                    producto_terminado = self.env['product.template'].browse(tmpl_id.id)

                    producto_terminado.make_variants()


                else:

                    campos_a_completar = ''
                    for campo in comprobante:
                        if not self[campo]:
                            campos_a_completar = str(campos_a_completar) + str(campo) + ', '

                    campos_a_completar = str(campos_a_completar[:-2])
                    campos_a_completar = campos_a_completar + '.'
                    campos_a_completar = 'Tienes que completar los siguientes campos: ' + str(campos_a_completar) + ' Una vez completados podrás cambiar el boceto a "Producir".'
                    
                    warning = {
                        'title': "¡Faltan Campos!",
                        'message': str(campos_a_completar),
                    }

                    self.kanban_state = 'blocked'
                    return {'warning': warning, 'type': 'ir_actions_act_reload_view'} 

        self.old_stage_id = self.stage_id.id


    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id and self.design_team_id:
            if self.design_team_id.company_id and not self.design_team_id.company_id.id == self.company_id.id:
                self.design_team_id = False


    # FUNCIONES

    def add_colors(self):

        for color in self.carta_color_nvm.color:

            self.env['muestras.navima.color'].create({
                #'name': self.carta_color_nvm.coleccion.temporada + "-" + self.modelo_base_nvm + self.carta_color_nvm.material.cod_material,
                'name': "w",
                'colores_muestra_nvm': color.id,
                'diseno_id': self.id
            })


    def _default_stage(self):
        return self.env['nvm_design.stage'].search([], limit=1)
        

    def _get_default_team_id(self):
        MT = self.env['design.team']
        team = MT.search([('company_id', '=', self.env.company.id)], limit=1)
        if not team:
            team = MT.search([], limit=1)
        return team.id


    def archive_equipment_request(self):
        self.write({'archive': True})

    
    def actualizar_muestras(self):

        html_table = '<p><h1><b> NAVIMA - SALESMANN REQUEST </b></h1></p>'
        html_table += '<div style="width: 100%;">'
        html_table += '<img style="width: 400px !important; text-align: center !important; height: auto !important;" src="data:image/jpeg;base64,' + str(self.boceto_nvm).replace("b'", "")[:-1] + '=="/>'
        html_table += '<br/>'
        html_table += '<span style="text-align: left"><h2><b> Suppler Reference: ' + str(self.horma_nvm.name) + ' - ' + str(self.variante_de_horma_nvm) + '<br/><br/> Navima Reference: ' + str(self.modelo_base_nvm) + str(self.carta_color_referencia) + '</b></h2></span>'

        html_table += '</div><br/><br/>'

        agentes_max = 0

        colores_agentes = {}
        totales_agentes = {}

        for muestra in self.muestras:

            agentes = ""

            color = str(muestra.colores_muestra_nvm.name)

            agentes_por_color = 0

            for agente in muestra.agente_de_venta:

                agentes += str(agente.name) + ", "

                agentes_por_color += 1

            agentes = agentes[:-2]

            if agentes_por_color > agentes_max:

                agentes_max = agentes_por_color

            colores_agentes[color] = agentes
            totales_agentes[color + "total"] = agentes_por_color


        html_table += '<div style="width: 100% !important;>'
        html_table += '<div style="width: 50% !important; text-align: right !important;>'

        html_table += '<table style="border: 1px solid #000;"><tr><th style="border: 1px solid #000; text-align: center !important;">&nbsp;Samples To:&nbsp;</th><th style="border: 1px solid #000; text-align: center !important;">&nbsp;PARES&nbsp;</th><th style="border: 1px solid #000; text-align: center !important;">&nbsp;Agentes:&nbsp;</th></tr>'

        for color_unitario in colores_agentes:

            html_table += '<tr><td style="border: 1px solid #000; text-align: center !important;">&nbsp;' + color_unitario +'&nbsp;</td>'
            html_table += '<td style="border: 1px solid #000; text-align: center !important;">&nbsp;'

            html_table += str(totales_agentes[color_unitario + "total"])

            html_table += '&nbsp;</td>'
            html_table += '<td style="border: 1px solid #000; text-align: center !important;">&nbsp;'

            html_table += str(colores_agentes[color_unitario])

            html_table += '&nbsp;</td></tr>'

        html_table += '</table>'
        html_table += '</div>'
        html_table += '</div>'

        self.mensaje_muestras = html_table

    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):

        """ Read group customization in order to display all the stages in the
            kanban view, even if they are empty
        """
        stage_ids = stages._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)


    def send_mail(self):
        self.ensure_one()
        
        ir_model_data = self.env['ir.model.data']
        
        try:    
            template_id = self.env['mail.template'].browse(29)
        except ValueError:    
            template_id = False

        try:
            compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[1:3][1]
        except ValueError:
            compose_form_id = False
        

        ctx = {

            'default_model': 'nvm_design.request',    
            'default_res_id': self.id,    
            'default_use_template': bool(template_id),    
            'default_template_id': template_id.id,    
            'default_composition_mode': 'comment',
            'body_html': self.mensaje_muestras,
            'body': self.mensaje_muestras,
            'force_email': True,

        }

        return {    

            'type': 'ir.actions.act_window',    
            'view_mode': 'form',    
            'res_model': 'mail.compose.message', 
            'body': self.mensaje_muestras,   
            'views': [(compose_form_id, 'form')],    
            'view_id': compose_form_id,
            'reply_to_mode': 'update',    
            'target': 'new',    
            'context': ctx,

        }


    def modify_template_streaming(self, id):

        id = max(self.env['mail.compose.message'].search([]))
        mensaje = self.env['mail.compose.message'].browse(id)
        mensaje.body = self.mensaje_muestras
        