from odoo import _, api, fields, models
from odoo.exceptions import ValidationError



class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def action_confirm(self):
        skip_check_price = self._context.get('skip_check_price')
        check_product = self.check_product_price()
        blocking_warning = self.env['ir.config_parameter'].sudo().get_param('post_margin_sale.blocking_transaction_order')
        if len(check_product) > 0 and not skip_check_price:
            product_str = ('\n').join(f" {i + 1}. {product.display_name} minimum price is {product.currency_id.symbol}. {product.minimum_sale_price}" for i,product in enumerate(check_product))
            message = f"Price of this product is less than minimum sale price \n\n{product_str}"
            if blocking_warning:
                raise ValidationError(_(f"{message} \n\nTransaction blocked due to price being lower than the minimum sale price."))
            else:
                message += "\n\nDo you want to continue with the quotation for making sale order?"
                wizard = self.env['sale.confirmation.wizard'].create({'message': message})
                return {
                    'type': 'ir.actions.act_window',
                    'name': _('Confirm minimum sale price'),
                    'view_mode': 'form',
                    'res_model': 'sale.confirmation.wizard',
                    'target': 'new',
                    'res_id': wizard.id,
                }
        return super(SaleOrder, self).action_confirm()

            

    def check_product_price(self):
        products = []
        for line in self.order_line:
            if line.price_unit < line.minimum_sale_price:
                products.append(line.product_id)
        return products

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    minimum_sale_price = fields.Float(string="Minimum sale price", related='product_id.minimum_sale_price')
