from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        # Cek apakah pesanan ini adalah rental order (sale_renting)
        if self.is_rental_order():  # Menggunakan metode pengecekan rental order
            return super(SaleOrder, self).action_confirm()

        skip_check_price = self._context.get('skip_check_price')
        check_product = self.check_product_price()
        blocking_warning = self.env['ir.config_parameter'].sudo().get_param('post_margin_sale.blocking_transaction_order')

        if len(check_product) > 0 and not skip_check_price:
            product_str = ('\n').join(f" {i + 1}. {product.display_name} minimum price is {product.currency_id.symbol}. {product.minimum_sale_price:.2f}" for i, product in enumerate(check_product))
            message = (_(f"Price of this product is less than minimum sale price \n\n{product_str}"))

            # Tampilkan wizard untuk produk non-rental
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

    def detect_user_language(self):
        # Get the user's language from the context
        user_lang = self.env.context.get('lang', 'en_US')  # Default to English if not set

        # Check if the user language is French
        if user_lang.startswith('fr'):
            return 'French'
        else:
            return 'Other'

    def is_rental_order(self):
        """Metode untuk memeriksa apakah ini adalah order rental"""
        return any(line.product_id.rent_ok for line in self.order_line)

    def check_product_price(self):
        """Pengecekan produk yang memiliki harga di bawah minimum"""
        products = []
        for line in self.order_line:
            if line.price_unit < line.minimum_sale_price:
                products.append(line.product_id)
        return products


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    minimum_sale_price = fields.Float(string="Minimum sale price", related='product_id.minimum_sale_price')