# -*- coding: utf-8 -*-

from odoo import api, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.constrains('location_id','location_dest_id')
    def _check_locations_not_blocked(self):
        """ Check if any of the source or destination locations are blocked
        """
        self.mapped('location_id').check_blocked(prefix=_('Wrong source location creating transfer.'))
        self.mapped('location_dest_id').check_blocked(prefix=_('Wrong destination location creating transfer.'))
