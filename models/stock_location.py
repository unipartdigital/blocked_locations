# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

class StockLocation(models.Model):
    _inherit = 'stock.location'

    # blocked locations are not pickable
    u_blocked = fields.Boolean(string='Is Blocked?',
                               help=('Check this box to prevent stock ' +
                                     'picks from this location'),
                               index=True)

    u_blocked_reason = fields.Char(string='Reason for Block:', required=False)

    def check_blocked(self, prefix=''):
        """ Checks if any of the locations in self are blocked.

            :param prefix: string
        """
        if not isinstance(prefix, str):
            raise ValidationError(
                    _("Prefix parameter for check_blocked should be string"))
        blocked_locations = self.filtered(lambda x: x.u_blocked)
        if blocked_locations:
            raise ValidationError(
                    _('%s %s Please speak to a team leader '
                      'to resolve the issue.') %
                      (prefix, ' '.join(blocked_locations._prepare_blocked_msg())))

    @api.one
    def _prepare_blocked_msg(self):
        """ Prepares a message for the location depending if it is
            blocked or not.
        """
        if self.u_blocked:
            reason = _('(reason: no reason specified)')
            if self.u_blocked_reason:
                reason = _('(reason: %s)') % (str(self.u_blocked_reason))
            msg = _('Location %s is blocked %s.') % (self.name, reason)
        else:
            msg = _('Location %s is not blocked.') % (self.name)

        return msg

    @api.onchange('u_blocked')
    def onchange_u_blocked(self):
        """ Empty blocked reason when locations is unblocked
        """
        if not self.u_blocked:
            self.u_blocked_reason = ''

    @api.constrains('u_blocked')
    def _check_reserved_quants(self):
        """ Check if there is any stock.quant already reserved
            for the locations trying to be blocked
        """
        Quant = self.env['stock.quant']
        for record in self:
            if record.u_blocked:
                n_quants = Quant.search_count([
                    ('reserved_quantity', '>', 0),
                    ('location_id', '=', record.id),
                    ])
                if n_quants > 0:
                    raise ValidationError(
                            _('Location cannot be blocked because '
                              'it contains reserved stock.'))

    def _prepare_info(self, extended=False, **kwargs):
        """
            Prepares the following extra info of the location in self
            when extended paramameter is True:
            - u_blocked: boolean
            - u_blocked_reason: string
        """
        info = super(StockLocation, self)._prepare_info(**kwargs)
        if extended:
            info['u_blocked'] = self.u_blocked
            info['u_blocked_reason'] = self.u_blocked_reason

        return info
