import { defineStore } from 'pinia'
import { URI } from '../service/conection'

export const usecartStore = defineStore('tezos-cart', {
  persist: {
    key: 'tezos-cart',
    storage: localStorage,
    paths: ['cart', 'last_order'],
  },
  state: () => ({
    currentProduct: {},
    visibles: {
      currentProduct: false,
      addAdditionToCart: false,
      last_order: '',
    },
    cart: {
      products: [],
      total_cost: 0,
      additions: [], // Maneja las adiciones a nivel del carrito
    },
    last_order: '',
    sending_order: false,
  }),

  getters: {
    totalItems: state => {
      return state.cart.products.reduce(
        (total, product) => total + product.quantity,
        0,
      )
    },
    totalAdditions: state => {
      return state.cart.additions.reduce(
        (total, addition) => total + addition.price * addition.quantity,
        0,
      )
    },
    isProductInCart: state => productId => {
      return state.cart.products.some(
        product => product.product.id === productId,
      )
    },
  },

  actions: {
    incrementAdditionQuantity(additionId) {
      const addition = this.cart.additions.find(a => a.id === additionId)
      if (addition) {
        addition.quantity += 1
        this.calculateCartTotal()
      }
    },
    removeAdditionCompletelyFromCart(additionId) {
      const additionIndex = this.cart.additions.findIndex(
        a => a.id === additionId,
      )
      if (additionIndex > -1) {
        this.cart.additions.splice(additionIndex, 1)
        this.calculateCartTotal()
      }
    },

    decrementAdditionQuantity(additionId) {
      const addition = this.cart.additions.find(a => a.id === additionId)
      if (addition && addition.quantity > 1) {
        addition.quantity -= 1
        this.calculateCartTotal()
      }
    },

    setCurrentProduct(product) {
      this.currentProduct = product
    },

    setVisible(item, status) {
      this.visibles[item] = status
    },

    addProductToCart(product, quantity = 1, additionalItems = [], flavors = [], gaseosa = null) {
      // Busca el producto en el carrito, incluyendo sabores y gaseosa
      const cartProduct = this.cart.products.find(
        p => 
          p.product.id === product.id && 
          JSON.stringify(p.flavors) === JSON.stringify(this.groupFlavors(flavors)) &&
          JSON.stringify(p.gaseosa) === JSON.stringify(gaseosa)
      );
  
      if (cartProduct) {
        // Si el producto, sabores y gaseosa coinciden, incrementa la cantidad y el costo total
        cartProduct.quantity += quantity;
        cartProduct.total_cost += this.calculateProductTotal(
          product,
          quantity,
          additionalItems,
          flavors
        );
      } else {
        // Si el producto, sabores o gaseosa son diferentes, agrega una nueva entrada en el carrito
        this.cart.products.push({
          product,
          quantity,
          additionalItems: this.groupAdditionalItems(additionalItems),
          flavors: this.groupFlavors(flavors),
          gaseosa: gaseosa, // Almacena la gaseosa seleccionada
          total_cost: this.calculateProductTotal(
            product,
            quantity,
            additionalItems,
            flavors
          ),
        });
      }
      this.calculateCartTotal();
    },
    

    removeProductFromCart(productId, flavors = []) {
      // Agrupamos los sabores para que coincidan con el formato usado en el carrito
      const groupedFlavors = this.groupFlavors(flavors);
    
      // Filtramos el carrito para eliminar el producto específico
      this.cart.products = this.cart.products.filter(
        p => !(p.product.id === productId && JSON.stringify(p.flavors) === JSON.stringify(groupedFlavors))
      );
      this.calculateCartTotal();
    },

    addAdditionalItem(productId, additionalItem) {
      const product = this.cart.products.find(
        product => product.product.id === productId,
      )
      if (product) {
        product.additionalItems.push(additionalItem)
        product.total_cost += additionalItem.price * additionalItem.quantity
        this.calculateCartTotal()
      }
    },
    removeAdditionalItem(productId, additionalItemId) {
      const product = this.cart.products.find(
        product => product.product.id === productId,
      )
      if (product) {
        const itemIndex = product.additionalItems.findIndex(
          item => item.id === additionalItemId,
        )
        if (itemIndex > -1) {
          product.total_cost -=
            product.additionalItems[itemIndex].price *
            product.additionalItems[itemIndex].quantity
          product.additionalItems.splice(itemIndex, 1)
          this.calculateCartTotal()
        }
      }
    },
    groupAdditionalItems(additionalItems) {
      return additionalItems.reduce((acc, item) => {
        ;(acc[item.type] = acc[item.type] || []).push(item)
        return acc
      }, {})
    },

    groupFlavors(flavors) {
      // Agrupa los sabores seleccionados
      return flavors.reduce((acc, flavor) => {
        const existingFlavor = acc.find(f => f.id === flavor.id)
        if (existingFlavor) {
          existingFlavor.quantity += 1
        } else {
          acc.push({ ...flavor, quantity: 1 })
        }
        return acc
      }, [])
    },

    calculateProductTotal(product, quantity, additionalItems, flavors = []) {
      // Calcula el costo total del producto, incluyendo adicionales y sabores opcionales
      const additionalCost = additionalItems.reduce(
        (total, item) => total + item.price * item.quantity,
        0,
      );
      const flavorCost = flavors.reduce((total, flavor) => {
        return total + (flavors.length === 2 ? flavor.price / 2 : flavor.price);
      }, 0);
      return (product.price + additionalCost + flavorCost) * quantity;
    },

    removeProductInstance(productId, flavors = []) {
      // Agrupamos los sabores para que coincidan con el formato usado en el carrito
      const groupedFlavors = this.groupFlavors(flavors);
      
      // Encontramos el producto específico en el carrito
      const cartProduct = this.cart.products.find(
        p => p.product.id === productId && JSON.stringify(p.flavors) === JSON.stringify(groupedFlavors)
      );
    
      if (cartProduct) {
        if (cartProduct.quantity > 1) {
          cartProduct.quantity -= 1;
    
          // Calcula el costo de los sabores asociados al producto, si los tiene
          const flavorsTotal = cartProduct.flavors.reduce((total, flavor) => {
            return total + (cartProduct.flavors.length === 2 ? flavor.price / 2 : flavor.price);
          }, 0);
    
          // Restamos el precio del producto y el costo de los sabores
          cartProduct.total_cost -= (cartProduct.product.price + flavorsTotal);
        } else {
          // Si solo queda una instancia, eliminamos el producto completo del carrito
          this.removeProductFromCart(productId, groupedFlavors);
        }
      }
    
      this.calculateCartTotal();
    }
,    

    calculateCartTotal() {
      const productsTotal = this.cart.products.reduce((total, product) => {
        const flavorsTotal = product.flavors
          ? product.flavors.reduce((flavorTotal, flavor) => {
              return (
                flavorTotal +
                (product.flavors.length === 2 ? flavor.price / 2 : flavor.price)
              )
            }, 0)
          : 0

        return total + (product.total_cost + flavorsTotal * product.quantity)
      }, 0)

      const additionsTotal = this.totalAdditions
      this.cart.total_cost = productsTotal + additionsTotal
    },

    addAdditionToCart(addition) {
      const existingAddition = this.cart.additions.find(
        a => a.id === addition.id,
      )
      if (existingAddition) {
        existingAddition.quantity += addition.quantity
      } else {
        this.cart.additions.push({ ...addition })
      }
      this.calculateCartTotal()
    },

    removeAdditionFromCart(additionId) {
      const additionIndex = this.cart.additions.findIndex(
        a => a.id === additionId,
      )
      if (additionIndex > -1) {
        if (this.cart.additions[additionIndex].quantity > 1) {
          this.cart.additions[additionIndex].quantity -= 1
        } else {
          this.cart.additions.splice(additionIndex, 1)
        }
        this.calculateCartTotal()
      }
    },
  },
})
