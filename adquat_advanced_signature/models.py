# -*- coding: utf-8 -*-
############################################################################################
#
#    ADQUAT
#
############################################################################################

from odoo import _, api, fields, models
from datetime import date, datetime, time, timedelta
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

class res_partner(models.Model):
    _inherit = "res.partner"
    type_partner = fields.Selection([('prospect', 'Prospect'),('customer', 'Client'),('none','Aucun')],
                                    compute='_compute_type_partner', string="Type de partenariat", store=False)

    @api.depends('opportunity_count', 'sale_order_ids', 'sale_order_ids.state')
    def _compute_type_partner(self):
        for record in self:
            if any(order.state == "sale" for order in record.sale_order_ids):
                self.type_partner = 'customer'
            elif record.opportunity_count > 0:
                self.type_partner = 'prospect'
            else:
                self.type_partner = 'none'