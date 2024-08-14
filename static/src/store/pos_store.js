/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";


patch(PosStore.prototype, {
    
    _loadProductProduct(products) {
        products.forEach(product => {
            product.minimum_sale_price = product.minimum_sale_price || 0;
        });
        super._loadProductProduct(products);
    }
});