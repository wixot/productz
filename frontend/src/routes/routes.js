import DashboardLayout from '../components/Dashboard/Layout/DashboardLayout.vue'
import User from 'src/components/Dashboard/Views/User.vue'
import Apps from 'src/components/Dashboard/Views/Apps.vue'
import Networks from 'src/components/Dashboard/Views/Networks.vue'
import Dashboard from 'src/components/Dashboard/Views/Dashboard.vue'
import DashboardDetails from 'src/components/Dashboard/Views/Dashboard/DasboardDetails.vue'

const routes = [
    {
        path: '/',
        component: DashboardLayout,
        redirect: '/user',
        children: [
            {
                path: 'user',
                name: 'User',
                component: User
            },
            {
                path: 'apps',
                name: 'Apps',
                component: Apps
            },
            {
                path: 'networks',
                name: 'Networks',
                component: Networks
            },
            {
                path: 'dashboard',
                name: 'Dashboard',
                component: Dashboard
            },
            {
                path: '/details/:app',
                name: 'Details',
                component: DashboardDetails
            }
        ]
    },
]

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
 function view(name) {
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

export default routes
