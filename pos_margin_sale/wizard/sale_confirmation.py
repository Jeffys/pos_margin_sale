from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleConfirmationWizard(models.TransientModel):
    _name = 'sale.confirmation.wizard'
    _description = "Sale confirmation wizard"

    message = fields.Text(string="Message", translate=True)

    def action_confirms(self):
        active_model = self._context.get('active_model')
        active_ids = self._context.get('active_ids', [])
        
        if active_model == 'sale.order':
            sale = self.env[active_model].browse(active_ids)

            if sale.is_rental_order:
                # Directly confirm the sale if it's a rental order
                return sale.action_confirm()

            # For non-rental orders, check minimum sale price
            products_below_minimum = sale.check_product_price()
            if products_below_minimum:
                # Handle the case where the products are below minimum price
                product_str = '\n'.join(
                    f"{i + 1}. {product.display_name} minimum price is {product.currency_id.symbol} {product.minimum_sale_price:.2f}"
                    for i, product in enumerate(products_below_minimum)
                )
                raise ValidationError(_(
                    f"The price of this product is lower than the minimum sale price:\n{product_str}"
                ))

            # Confirm the sale order if all checks pass
            sale.with_context(skip_check_price=True).action_confirm()
