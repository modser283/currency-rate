from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'order_id.pricelist_id')
    def onchange_product_pricelist(self):
        for line in self:
            if line.product_id and line.order_id.pricelist_id:
                pricelist = line.order_id.pricelist_id

                # Find the corresponding pricelist item for the product
                pricelist_item = self.env['product.pricelist.item'].search([
                        ('pricelist_id', '=', pricelist.id),
                    ('product_tmpl_id', '=', line.product_id.product_tmpl_id.id)
                ], limit=1)

                if pricelist_item:
                    line.price_unit = pricelist_item.new_price



