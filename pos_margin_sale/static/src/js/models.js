odoo.define('pos_margin_sale.models', function (require) {
    "use strict";

    const { PosGlobalState, Product, Orderline } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const PosGlobalStateExtended = (PosGlobalState) => class PosGlobalStateExtended extends PosGlobalState {
        
        _loadProductProduct (products) {
            products.forEach(product => {
                product.minimum_sale_price = product.minimum_sale_price || 0;
            });            
            return super._loadProductProduct(...arguments);
        }
    }

    Registries.Model.extend(PosGlobalState, PosGlobalStateExtended);
    
    const ProductPosInherit = (Product) => 
        class extends Product {
            get_minimum_sale_price() {
                return this.minimum_sale_price;
            }
            
        }

    Registries.Model.extend(Product, ProductPosInherit);


    const OrderlineExtended = (Orderline) => 
        class extends Orderline {

            get_minimum_sale_price() {
                return this.product.get_minimum_sale_price();
            }
        }
    
        Registries.Model.extend(Orderline, OrderlineExtended);
});