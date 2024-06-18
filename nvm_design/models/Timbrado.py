from odoo import models, fields, api

class Timbrado(models.Model):
    _name = 'timbrado'
    _description = 'Timbrado para los packs que se envian'

    display_name = fields.Char('Shipping Mark', required=True)
    name = fields.Char('Shipping Mark', required=True)
    cliente = fields.Many2one('res.partner', 'Cliente', required=True, domain=[('type', '=', 'contact')])

    @api.onchange('display_name')
    def _onchange_display_name(self):
        self.name = self.display_name