from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_rental_order = fields.Boolean(
        string="Created In App Rental",
        compute='_compute_is_rental_order',
        store=True, precompute=True, readonly=False,
        # By default, all orders created in rental app are Rental Orders
        default=lambda self: self.env.context.get('in_rental_app'))

    @api.depends('order_line.rental_start_date', 'order_line.rental_end_date')
    def _compute_is_rental_order(self):
        for order in self:
            # If a rental product is added in the rental app to the order, it becomes a rental order
            order.is_rental_order = order.is_rental_order or order.has_rented_products

    def action_confirm(self):
        """Override action_confirm to check for minimum sale price."""
        
        # If it's a rental order, skip the entire confirmation process
        if self.is_rental_order:
            return super(SaleOrder, self).action_confirm()

        skip_check_price = self._context.get('skip_check_price', False)
        check_product = self.check_product_price()
        blocking_warning = self.env['ir.config_parameter'].sudo().get_param('post_margin_sale.blocking_transaction_order')

        # If there are products below minimum price and checks are not skipped
        if check_product and not skip_check_price:
            product_str = ('\n').join(f" {i + 1}. {product.display_name} minimum price is {product.currency_id.symbol}. {product.minimum_sale_price:.2f}" for i, product in enumerate(check_product))
            product_str_fr = ('\n').join(f" {i + 1}. {product.display_name} le prix minimum est {product.currency_id.symbol}. {product.minimum_sale_price:.2f}" for i, product in enumerate(check_product))
            
            message = (_(f"Price of this product is less than minimum sale price \n\n{product_str}"))
            message_fr = f"Le prix de ce produit est inférieur au prix de vente minimum \n\n{product_str_fr}"
            user_language = self.detect_user_language()

            # Handle blocking warning
            if blocking_warning:
                if user_language == 'French':
                    raise ValidationError(_(f"{message_fr} \n\nTransaction bloquée car prix inférieur au prix minimum de vente."))
                else:
                    raise ValidationError(_(f"{message} \n\nTransaction blocked due to price being lower than the minimum sale price."))
            else:
                # Show confirmation wizard
                wizard = self.env['sale.confirmation.wizard'].create({'message': message})
                wizard.with_context(lang='fr_FR').write({'message': message_fr})

                return {
                    'type': 'ir.actions.act_window',
                    'name': _('Confirm Maximum sale price'),
                    'view_mode': 'form',
                    'res_model': 'sale.confirmation.wizard',
                    'target': 'new',
                    'res_id': wizard.id,
                }

        return super(SaleOrder, self).action_confirm()

    def detect_user_language(self):
        """Detect the user's language from the context."""
        user_lang = self.env.context.get('lang', 'en_US')  # Default to English if not specified
        return 'French' if user_lang.startswith('fr') else 'Other'

    def check_product_price(self):
        """Check product prices against minimum sale prices."""
        products = []
        
        # If this is a rental order, return empty list
        if self.is_rental_order:
            return products  

        # Check each line for minimum sale price condition
        for line in self.order_line:
            # Add condition to check if the product is rent_ok
            if line.price_unit < line.minimum_sale_price and not line.product_id.rent_ok:
                products.append(line.product_id)
        
        return products


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    minimum_sale_price = fields.Float(string="Minimum sale price", related='product_id.minimum_sale_price')
