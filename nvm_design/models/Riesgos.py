from odoo import models, fields, api

class Riesgos(models.Model):
    _name = 'riesgos'
    _description = 'Empresas de riesgo con las que trabaja navima'
    
    name = fields.Char('Riesgo')
    #empresa_riesgo = fields.Many2one('res.partner', string="Empresa de riesgo")
    coletilla = fields.Text('Coletilla')