import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // Ruta padre
      path: '/',
      name: 'restaurante',
      meta: {
        title: 'Restaurante'
      },
      component: () => import('../AppLayout/AppLayout.vue'),
      children: [
        {
          path: '',
          name: 'home',
          meta: {
            title: 'Producto y servicios'
          },
          component: () => import('../views/home.vue'),
        },
        {
          path: 'categoria/:category_name/:category_id',
          name: 'categoria',
          meta: {
            title: 'Categoría'
          },
          component: () => import('../views/CategoryView.vue'),
        },
        {
          path: 'carta',
          name: 'carta',
          meta: {
            title: 'Noticias'
          },
          component: () => import('../views/carta.vue'),
        },

        {
          path: 'Horarios',
          name: 'Horarios',
          meta: {
            title: 'Horarios'
          },
          component: () => import('../views/Horarios.vue'),
        },
        {
          path: 'rastrear',
          name: 'rastrear',
          meta: {
            title: 'Rastrear Pedido'
          },
          component: () => import('../views/Rastrear.vue'),
        },
        {
          path: 'cart',
          name: 'cart',
          meta: {
            title: 'Carrito'
          },
          component: () => import('@/views/cart.vue'),
        },
        {
          path: 'pay',
          name: 'pay',
          meta: {
            title: 'Pago'
          },
          component: () => import('@/views/pay.vue'),
        },
        {
          path: 'gracias',
          name: 'gracias',
          meta: {
            title: 'Gracias'
          },
          component: () => import('@/views/gracias.vue'),
        },
      ],
    },
  ],
})





router.afterEach((to) => {
  const defaultTitle = `Ing Master`

  if (to.name === 'categoria' && to.params.category_name) {
    // Capitalizamos el nombre de la categoría
    const categoryNameCapitalized = capitalizeFirstLetter(to.params.category_name)
    document.title = `${categoryNameCapitalized} | ${defaultTitle}`
  } else {
    // De lo contrario, usamos meta.title o el título por defecto
    document.title = to.meta?.title
      ? `${to.meta.title} | ${defaultTitle}`
      : defaultTitle
  }
})


function capitalizeFirstLetter(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
}

export default router
