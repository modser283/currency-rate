from odoo import models, fields, api, _


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    currency_rate = fields.Float(string='Currency Rate')



    @api.onchange('currency_rate')
    def _onchange_currency_rate(self):
        for item in self.env['product.pricelist.item'].search([('pricelist_id', '=', self.id)]):
            item._compute_new_price()


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    new_price = fields.Float(string='New Price', compute='_compute_new_price', store=True)

    @api.depends('fixed_price', 'pricelist_id.currency_rate')
    def _compute_new_price(self):
        for item in self:
            item.new_price = item.fixed_price * item.pricelist_id.currency_rate


