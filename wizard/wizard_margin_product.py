from odoo import _, api, fields, models


class WizardMarginProduct(models.TransientModel):
    _name = 'wizard.margin.product'
    _description = 'Set margin on every product'


    product_template_ids = fields.Many2many('product.template', string='Products')
    margin = fields.Float('Margin')


    def action_assing_margin(self):
        for product in self.product_template_ids:
            product.margin_sale = self.margin
        return True
    