# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DesignEquipment(models.Model):
    _name = 'design.equipment'
    _description = 'Design Equipment'
    _check_company_auto = True

    """
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        equipment_ids = []
        if name:
            equipment_ids = self._search([('name', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid)
        if not equipment_ids:
            equipment_ids = self._search([('name', operator, name)] + args, limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(equipment_ids).with_user(name_get_uid))
    """
    name = fields.Char('Equipment Name', required=True, translate=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    active = fields.Boolean(default=True)
    owner_user_id = fields.Many2one('res.users', string='Owner')

    design_ids = fields.One2many('nvm_design.request', 'equipment_id')
    design_count = fields.Integer(compute='_compute_design_count', string="Design Count", store=True)
    design_open_count = fields.Integer(compute='_compute_design_count', string="Current Design", store=True)
    design_team_id = fields.Many2one('design.team', string='Familia', check_company=True)
    design_duration = fields.Float(help="Design Duration in hours.")

    color = fields.Integer('Color Index')

    @api.depends('design_ids.stage_id.done')
    def _compute_design_count(self):
        for equipment in self:
            equipment.design_count = len(equipment.design_ids)
            equipment.design_open_count = len(equipment.design_ids.filtered(lambda x: not x.stage_id.done))

    
    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id and self.design_team_id:
            if self.design_team_id.company_id and not self.design_team_id.company_id.id == self.company_id.id:
                self.design_team_id = False


    def _create_new_request(self, date):
        self.ensure_one()
        self.env['design.request'].create({
            'name': _('Preventive Design - %s') % self.name,
            'request_date': date,
            'schedule_date': date,
            #'category_id': self.category_id.id,
            'equipment_id': self.id,
            'design_type': 'preventive',
            'owner_user_id': self.owner_user_id.id,
            'user_id': self.technician_user_id.id,
            'design_team_id': self.design_team_id.id,
            'duration': self.design_duration,
            'company_id': self.company_id.id or self.env.company.id
            })
