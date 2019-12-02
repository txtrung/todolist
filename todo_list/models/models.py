# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TodoList(models.Model):
    _name = 'todo_list.todo_list'

    # def _default_value(self):
    #     employee = self.env['hr.employee']
    #     resource = self.env['resource.resource']
    #     resource_id = resource.search([('user_id', '=', self._uid)], limit=1).id
    #     return employee.search([('resource_id', '=', resource_id)], limit=1).parent_id

    name = fields.Text(compute='_compute_name')
    description = fields.Text('Description')
    create_date = fields.Date('Create Date')
    deadline = fields.Date('Deadline')
    responsible = fields.Many2one('res.users', string='Responsible')
    # manager = fields.Many2one('hr.employee', string='Manager', default=_default_value, readonly=True)
    manager_id = fields.Many2one('res.users', string='Manager')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting for Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', copy=False, readonly=True)

    @api.one
    def _compute_name(self):
        self.name = "%s" % (self.description if len(self.description) > 0 else '' or '')

    @api.model
    def create(self, vals):
        vals['state'] = 'draft'
        return super(TodoList, self).create(vals)

    @api.multi
    def action_confirm(self):
        self.write({'state': 'waiting'})

    @api.multi
    def action_approve(self):
        self.write({'state': 'approved'})

    @api.multi
    def action_reject(self):
        self.write({'state': 'rejected'})


