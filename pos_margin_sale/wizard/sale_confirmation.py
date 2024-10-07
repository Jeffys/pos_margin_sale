# from odoo import _, api, fields, models

# class SaleConfirmationWizard(models.TransientModel):
#     _name = 'sale.confirmation.wizard'
#     _description = "Sale confirmation wizard"

#     message = fields.Text(string="Message", translate=True)

#     def action_confirm(self):
#         active_model = self._context.get('active_model')
#         active_id = self._context.get('active_ids')
#         if active_model == 'sale.order':
#             sale = self.env[active_model].browse(active_id)

#             # Check if the sale order is a rental order
#             if sale.is_rental_order:  # Assuming is_rental_order is the field indicating rental orders
#                 return  # Skip the confirmation for rental orders

#             # For non-rental orders, proceed with the confirmation
#             sale.with_context(skip_check_price=True).action_confirm()