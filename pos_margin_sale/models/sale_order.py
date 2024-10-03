from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirms(self):
        skip_check_price = self._context.get('skip_check_price')
        check_product = self.check_product_price()
        blocking_warning = self.env['ir.config_parameter'].sudo().get_param('post_margin_sale.blocking_transaction_order')

        # Skip price checks and wizard for rental orders
        if self._is_rental_order():  # Ensure you have a method to identify rental orders
            return super(SaleOrder, self).action_confirms()

        # Proceed with price checks for non-rental orders
        if len(check_product) > 0 and not skip_check_price:
            product_str = ('\n').join(
                f"{i + 1}. {product.display_name} minimum price is {product.currency_id.symbol}{product.minimum_sale_price:.2f}"
                for i, product in enumerate(check_product)
            )
            message = _(f"Price of this product is less than minimum sale price:\n{product_str}")

            user_language = self.detect_user_language()
            if blocking_warning:
                if user_language == 'French':
                    raise ValidationError(_(f"{message}\n\nTransaction bloquée car prix inférieur au prix minimum de vente."))
                else:
                    raise ValidationError(_(f"{message}\n\nTransaction blocked due to price being lower than the minimum sale price."))
            else:
                # Proceed with wizard invocation
                wizard = self.env['sale.confirmation.wizard'].create({'message': message})
                return {
                    'type': 'ir.actions.act_window',
                    'name': _('Confirm minimum sale price'),
                    'view_mode': 'form',
                    'res_model': 'sale.confirmation.wizard',
                    'target': 'new',
                    'res_id': wizard.id,
                }

        return super(SaleOrder, self).action_confirms()

    def _is_rental_order(self):
        # Add logic to determine if this sale order is a rental order
        # This could be based on specific fields or conditions in your model
        return self.order_type == 'rental'  # Example condition, adjust as needed

    def detect_user_language(self):
        # Get the user's language from the context
        user_lang = self.env.context.get('lang', 'en_US')  # Default to English if not set

        # Check if the user language is French
        if user_lang.startswith('fr'):
            return 'French'
        else:
            return 'Other'

    def check_product_price(self):
        products = []
        for line in self.order_line:
            if line.price_unit < line.minimum_sale_price:
                products.append(line.product_id)
        return products

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    minimum_sale_price = fields.Float(string="Minimum sale price", related='product_id.minimum_sale_price')
