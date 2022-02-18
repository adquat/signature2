# -*- coding: utf-8 -*-
############################################################################################
#
#    ADQUAT
#
############################################################################################

from odoo import _, api, fields, models
import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class sale_order(models.Model):
    _inherit = "sale.order"

    def create_project(self):
        if len(self.company_id) == 1:
            # All orders are in the same company
            self.order_line.sudo().with_company(self.company_id)._timesheet_service_generation()
        else:
            # Orders from different companies are confirmed together
            for order in self:
                order.order_line.sudo().with_company(order.company_id)._timesheet_service_generation()
        return True

class task(models.Model):
    _inherit = "project.task"

    planned_date_begin = fields.Datetime("Start date", tracking=True, task_dependency_tracking=True, default=lambda self: fields.Datetime.now())
    planned_date_end = fields.Datetime("End date", tracking=True, task_dependency_tracking=True, default=lambda self: fields.Datetime.now() + datetime.timedelta(days=1))

    def action_get_project_forecast_by_user(self):
        allowed_tasks = (self | self._get_all_subtasks() | self.depend_on_ids)
        action = self.env["ir.actions.actions"]._for_xml_id("project_forecast.project_forecast_action_schedule_by_employee")
        first_slot = self.env['planning.slot'].search([('start_datetime', '>=', datetime.datetime.now()), ('task_id', 'in', allowed_tasks.ids)], limit=1, order="start_datetime")
        action_context = {
            'group_by': ['task_id', 'resource_id'],
        }
        if first_slot:
            action_context.update({'initialDate': first_slot.start_datetime})
        else:
            if not allowed_tasks.mapped('planned_date_begin'):
                min_date = datetime.datetime.now()
            else:
                min_date = min(allowed_tasks.mapped('planned_date_begin'))
            if min_date and min_date > datetime.datetime.now():
                action_context.update({'initialDate': min_date})
        action['context'] = action_context
        action['domain'] = [('task_id', 'in', allowed_tasks.ids)]
        return action

class saleorderline(models.Model):
    _inherit = "sale.order.line"

    def write(self, values):
        res = super(saleorderline, self).write(values)
        if 'customer_lead' in values:
            for so in self:
                so.move_ids.date_deadline = so.scheduled_date
                so.move_ids.date = so.scheduled_date
        return res