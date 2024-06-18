# -*- coding: utf-8 -*-
# TESTEO CAMBIO
from odoo import models, fields, api

class DesignTeam(models.Model):
    _name = 'design.team'
    _description = 'Design Teams'

    name = fields.Char('Team Name', required=True, translate=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)
    member_ids = fields.Many2many(
        'res.users', 'design_team_users_rel', string="Team Members",
        domain="[('company_ids', 'in', company_id)]")
    color = fields.Integer("Color Index", default=0)
    request_ids = fields.One2many('nvm_design.request', 'design_team_id', copy=False)
    coleccion_nvm = fields.Many2one('colecciones.colecciones')

    # For the dashboard only
    todo_request_ids = fields.One2many('nvm_design.request', string="Requests", copy=False, compute='_compute_todo_requests')
    todo_request_count = fields.Integer(string="Number of Requests", compute='_compute_todo_requests')
    todo_request_count_date = fields.Integer(string="Number of Requests Scheduled", compute='_compute_todo_requests')
    todo_request_count_high_priority = fields.Integer(string="Number of Requests in High Priority", compute='_compute_todo_requests')
    todo_request_count_block = fields.Integer(string="Number of Requests Blocked", compute='_compute_todo_requests')
    todo_request_count_unscheduled = fields.Integer(string="Number of Requests Unscheduled", compute='_compute_todo_requests')

    @api.depends('request_ids.stage_id.done')
    def _compute_todo_requests(self):
        for team in self:
            team.todo_request_ids = team.request_ids.filtered(lambda e: e.stage_id.done==False)
            team.todo_request_count = len(team.todo_request_ids)
            team.todo_request_count_date = len(team.todo_request_ids.filtered(lambda e: e.schedule_date != False))
            team.todo_request_count_high_priority = len(team.todo_request_ids.filtered(lambda e: e.priority == '3'))
            team.todo_request_count_block = len(team.todo_request_ids.filtered(lambda e: e.kanban_state == 'blocked'))
            team.todo_request_count_unscheduled = len(team.todo_request_ids.filtered(lambda e: not e.schedule_date))
