# -*- coding: utf-8 -*-

from odoo import api, models, _


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.constrains('location_id','location_dest_id')
    def _check_locations_not_blocked(self):
        self.mapped('location_id').check_blocked(prefix=_('Wrong source location creating stock move line.'))
        self.mapped('location_dest_id').check_blocked(prefix=_('Wrong destination location creating stock move line.'))
