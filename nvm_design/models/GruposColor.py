from odoo import models, fields, api

class GruposColor(models.Model):
    _name = 'gruposcolores'
    _description = 'Un modelo que agrupa los colores'

    display_name = fields.Char('Grupo Color')
    name = fields.Char('Grupo Color')
    colores_count = fields.Integer(compute='compute_count')

    @api.onchange('name')
    def _onchange_display_name(self):
        self.display_name = self.name


    def compute_count(self):
        for record in self:
            record.colores_count = self.env['coloresnnavima'].search_count([('proveedor', '=', self.id)])


    def compute_colores_count(self):

        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Colores',
            'view_mode': 'tree',
            'res_model': 'coloresnnavima',
            'domain': [('proveedor', '=', self.id)],
            'context': "{'create': False}"
        }
