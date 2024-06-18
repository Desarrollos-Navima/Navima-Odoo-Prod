/*
odoo.define('nvm_sales.color_set', function (require) {
    "use strict";

    const SaleOrderLineProductField = require('@sale_product_matrix/js/sale_product_field').SaleOrderLineProductField;
    const { onPatched } = owl.hooks;

    class MiExtension extends SaleOrderLineProductField {
        setup() {
            super.setup();
            onPatched(() => {
                if (this.props.record && this.props.record.model === 'sale.order.line.variant.grid') {
                    this.miFuncion();
                }
            });
        }
        miFuncion() {
            try {

                var els = document.getElementsByClassName("o_matrix_input");
        
                Array.prototype.forEach.call(els, function(el) {
                    
                    el.addEventListener('change', function() {
                        if (el.value === '0') {
                            el.style.color = 'white';
                        } else {
                            el.style.color = 'black';
                        }
                    });
        
                    if (el.value === '0') {
                        el.style.color = 'white';
                    } else {
                        el.style.color = 'black';
                    }

                });
        
            } catch (error) {

                console.error('Error al colorear la matriz:', error);

            }
        }
    }

    //MiExtension.template = "sale.SaleProductField";

    //registry.category("fields").add("pol_product_many2one", MiExtension);

    //return { MiExtension };

});
*/

function color_grid() {
    try {
        var els = document.getElementsByClassName("o_matrix_input");

        Array.prototype.forEach.call(els, function(el) {
            
            el.addEventListener('change', function() {
                if (el.value === '0') {
                    el.style.color = 'white';
                } else {
                    el.style.color = 'black';
                }
            });

            if (el.value === '0') {
                el.style.color = 'white';
            } else {
                el.style.color = 'black';
            }
        });

    } catch (error) {
        console.error('Error al colorear la matriz:', error);
    }
}