<template>
  <div class="wrapper">
    <side-bar>
      <mobile-menu slot="content"></mobile-menu>
      
      <sidebar-link to="/dashboard">
        <i class="nc-icon nc-circle-09"></i>
        <p>Dashboard</p>
      </sidebar-link>

      <sidebar-link to="/apps">
        <i class="nc-icon nc-circle-09"></i>
        <p>Apps</p>
      </sidebar-link>

      <sidebar-link to="/networks">
        <i class="nc-icon nc-circle-09"></i>
        <p>Networks</p>
      </sidebar-link>

    </side-bar>
    <div class="main-panel">
      <top-navbar></top-navbar>

      <dashboard-content @click="toggleSidebar">

      </dashboard-content>

      <content-footer></content-footer>
    </div>
  </div>
</template>
<style lang="scss">

</style>
<script>
  import TopNavbar from './TopNavbar.vue'
  import ContentFooter from './ContentFooter.vue'
  import DashboardContent from './Content.vue'
  import MobileMenu from './MobileMenu.vue'
  export default {
    components: {
      TopNavbar,
      ContentFooter,
      DashboardContent,
      MobileMenu
    },
    methods: {
      toggleSidebar () {
        if (this.$sidebar.showSidebar) {
          this.$sidebar.displaySidebar(false)
        }
      }
    }
  }

</script>
