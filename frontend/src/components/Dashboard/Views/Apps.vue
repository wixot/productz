<template>
  <div>
    <card>
      <button  class="btn btn-info btn-fill float-left"  v-on:click="getStatus()">
            New App
      </button>
    </card>

    <card v-if="divStatus === true">
      <new-apps-card>
      </new-apps-card>
    </card>

    <card>
      <apps-card :apps="apps">
      </apps-card>
    </card>
  </div>
</template>
<script>
  import Card from 'src/components/UIComponents/Cards/Card.vue'
  import AppsCard from 'src/components/Dashboard/Views/Apps/AppsCard.vue'
  import NewAppsCard from 'src/components/Dashboard/Views/Apps/NewAppsCard.vue'
  import axios from 'axios'

  export default {
    components: {
      Card,
      AppsCard,
      NewAppsCard
    },
    beforeMount () {
      this.getApps()
    },
    data () {
      return {
        apiResponse: '',
        divStatus: '',
        apps: []
      }
    },
    methods: {
      getStatus () {
        if (this.divStatus !== true) {
          this.divStatus = true
        } else {
          this.divStatus = false
        }
      },
      getApps () {
        axios.get(this.$apiLink + '/apps')
          .then(response => {
            this.apps = response.data
          })
      }
    }
  }
</script>
<style>

</style>
