import { defineStore } from "pinia";
import { URI } from "../service/conection";


export const useProductStore = defineStore('product', {

    persist: {

        key: 'product',
        storage: localStorage,
        paths: []
    },

    state: () => {
        return {
            currentProductToEdit: {
            },
            currentProductToDelete:{

            },
            visibles: {
                dialogEditProduct: false,
                dialogAddProduct: false,
                dialogDeleteProduct: false,
                dialogGestorCategoria: false
            }
        }
    },

    getters: {
    },

    actions: {
    },


})


