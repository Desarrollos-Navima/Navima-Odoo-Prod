from odoo import models, fields, api

class MarcasNavima(models.Model):
    _name = 'marcasnavima'
    _description = 'Marcas que utiliza navima'

    display_name = fields.Char('Marca', required=True)
    name = fields.Char('Marca', required=True)
    cliente = fields.Many2one('res.partner', 'Cliente', required=True, domain=[('type', '=', 'contact')])

    @api.onchange('display_name')
    def _onchange_display_name(self):
        self.name = self.display_name