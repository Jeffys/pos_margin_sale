from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    margin_sale = fields.Float(string="Margin", tracking=True)
    minimum_sale_price = fields.Float(string="Minimum sale price", compute='_compute_minimum_sale_price', 
                                      inverse='_inverse_minimum_sale_price', store=True, readonly=False)


    @api.depends('margin_sale', 'standard_price')
    def _compute_minimum_sale_price(self):
        for rec in self:
            rec.minimum_sale_price = rec.standard_price * (1 + rec.margin_sale/100)
            
    def _inverse_minimum_sale_price(self):
        for rec in self:
            if rec.standard_price:
                rec.margin_sale = ((rec.minimum_sale_price / rec.standard_price) - 1) * 100
            else:
                rec.margin_sale = 0.0

    def action_assign_margin(self):
        wizard = self.env['wizard.margin.product'].create({
            'product_template_ids': [(6, 0, self.ids)]
        })
        return {
            'type': 'ir.actions.act_window',
            'name': _('Update margin sale'),
            'view_mode': 'form',
            'res_model': 'wizard.margin.product',
            'target': 'new',
            'res_id': wizard.id,
        }


# class ProductProduct(models.Model):
#     _inherit = 'product.S'

    