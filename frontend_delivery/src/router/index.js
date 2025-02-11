import { createRouter, createWebHashHistory,createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';
import axios from 'axios';

import { URI } from '@/service/conection'
import { menuOptions } from '@/service/menuOptions';
import { ableMenu } from '../service/menuOptions';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: AppLayout,
      children: [
        {
          path: '/',
          name: 'Home',
          component: () => import('@/views/pages/Home.vue'),
          meta: { requiresAuth: true }, 
          children: [
            {
              path: '/',
              name: 'pedidos',
              component: () => import('@/views/pages/Carta.vue'),
              
            },

            {
              path: '/validar',
              name: 'validar',
              component: () => import('@/views/pages/validar.vue'),
              
            },
            {
              path: '/cuadre',
              name: 'cuadre',
              component: () => import('@/views/pages/cuadre.vue'),
              
            },

            {
              path: '/admin',
              name: 'admin',
              component: () => import('@/views/pages/admin.vue'),
              
              children:[

                {
                  path: '/admin/post',
                  name: 'admin-post',
                  component: () => import('@/views/pages/post.vue'),
                  
                },
                {
                  path: '/admin/banners',
                  name: 'admin-banners',
                  component: () => import('@/views/pages/Banners.vue'),
                  
                },
                {
                  path: '/admin/carta',
                  name: 'admin-carta',
                  component: () => import('@/views/pages/Carta.vue'),
                  
                },
                {
                  path: '/admin/reorder_categories',
                  name: 'reorder_categories',
                  component: () => import('@/views/pages/reorder_categories.vue'),
                  
                },
                {
                  path: '/admin/domicilios/',
                  name: 'domicilios',
                  component: () => import('@/views/pages/domicilios.vue'),
                  meta:{permision_id: 4},
                  children: [
                    {
                      path: '/admin/domicilios/:site_id',
                      name: 'domicilio',
                      component: () => import('@/views/pages/domicilio.vue')
                    },
                  ]
                },


            {
              path: '/tienda-menu',
              name: 'menuTienda',
              component: () => import('@/views/pages/tienda/MenuTienda.vue'),
              children:[
                  {
                    path: 'productos/:menu_name/:category_id',
                    name: 'sesion',
                    component: () => import('@/views/pages/tienda/sesion.vue')
                    // meta: { requireMenu: true },
                    // meta: { requiresAuth: true },
                  },

                  {
                    path: 'productos/adiciones',
                    name: 'adicionales',
                    component: () => import('@/views/pages/tienda/adicionales.vue')
                    // meta: { requireMenu: true },
                    // meta: { requiresAuth: true },
                  },

                  {
                    path: 'productos/sabores',
                    name: 'sabores',
                    component: () => import('@/views/pages/tienda/sabores.vue')
                    // meta: { requireMenu: true },
                    // meta: { requiresAuth: true },
                  },
                  // {
                  //     path: '/tienda-menu/productos/:sesion',
                  //     name: 'tienda-productos',
                  //     component: () => import('@/views/pages/tienda/sesion.vue')
                  // },
                  

              ]
          },
          


              ]
            },

            {
              path: '/reporte-ventas/',
              name: 'reporte-ventas',
              component: () => import('@/views/pages/reporteVentas.vue'),
              children: [
                {
                  path: '/reporte-ventas/valor-ventas',
                  name: 'reporte-ventas-valor-ventas',
                  component: () => import('@/views/pages/RepValorVentas.vue'),
                },
                {
                  path: '/reporte-ventas/no-ordenes',
                  name: 'reporte-ventas-no-ordenes',
                  component: () => import('@/views/pages/RepNoOrdenes.vue'),
                },
                {
                  path: '/reporte-ventas/ticket',
                  name: 'reporte-ventas-ticket',
                  component: () => import('@/views/pages/RepTicket.vue'),
                }
                ,
                {
                  path: '/reporte-ventas/clientes',
                  name: 'reporte-ventas-clientes',
                  component: () => import('@/views/pages/RepClientes.vue'),
                },
                {
                  path: '/reporte-ventas/ordenes',
                  name: 'reporte-ventas-ordenes',
                  component: () => import('@/views/pages/ordenes.vue'),
                }
    
              ]
            },
            
            {
              path: '/horarios',
              name: 'horarios',
              component: () => import('@/views/pages/horarios.vue'),
              
            },
            {
              path: '/historial',
              name: 'historial',
              component: () => import('@/views/pages/historial-pedidos.vue'),
              
            },
            {
              path: '/resumen-sedes',
              name: 'resumen-sedes',
              component: () => import('@/views/pages/views_admin/resumen_sedes.vue'),
              
            },
  
          ]
        },

      ]
    },

    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/pages/auth/Login.vue')
    },


      

  ]
});



router.beforeEach(async (to, from, next) => {
  // Verificar si la ruta requiere autenticación
  if (to.meta.requiresAuth) {
    // Obtener el token de acceso desde localStorage
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      // Si no hay un token de acceso, redirigir a la página de inicio de sesión
      next('/login');
    } else {
      // Si hay un token de acceso, continuar con la navegación
      next();
    }
  } else {
    // Si la ruta no requiere autenticación, continuar con la navegación
    next();
  }
});


export default router