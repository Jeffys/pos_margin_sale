odoo.define('pos_margin_sale.ProductScreen', function (require) {
    "use strict";

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const { Gui } = require('point_of_sale.Gui');

    const ProductScreenExtended = (ProductScreen) => 
        class extends ProductScreen {
            async _onClickPay() {
                // Accessing the order lines correctly
                const orderLines = this.env.pos.get_order().get_orderlines();
                const lessMinimumSalePrice = orderLines.filter(line => line.get_unit_price() < line.product.get_minimum_sale_price());
                const blocked = this.env.pos.config.is_blocked_warning
                if (lessMinimumSalePrice.length > 0) {
                    if (!blocked) {
                        const { confirmed } = await Gui.showPopup('ConfirmPopup', {
                            title: this.env._t("Price unit less than minimum price"),
                            body: this.env._t("Some products are below the minimum price. Proceed to payment?")
                        });
                        if (!confirmed) {
                            return;
                        }
                    } else {
                        await Gui.showPopup('ErrorPopup', {
                            title: this.env._t("Price unit less than minimum price"),
                            body: this.env._t("Some products are below the minimum price. Please check !")
                        });
                        return;
                    }
                }
                
                // Call the parent method
                await super._onClickPay(...arguments);
            }
        };

    // Register the extended component
    Registries.Component.extend(ProductScreen, ProductScreenExtended);

    return ProductScreenExtended;
});
