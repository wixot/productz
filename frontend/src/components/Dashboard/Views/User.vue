<template>
  <div>
    <div>
      <card>
        <user-card :userCardData="user">
        </user-card>
      </card>

      <card>
        <user-profile :userProfileData="user"  :updateUser="updateUser" :renewApiKey="renewApiKey">
        </user-profile>
      </card>

    </div>
  </div>
</template>
<script>
  import Card from 'src/components/UIComponents/Cards/Card.vue'
  import UserCard from 'src/components/Dashboard/Views/UserProfile/UserCard.vue'
  import UserProfile from 'src/components/Dashboard/Views/UserProfile/UserProfile.vue'
  import axios from 'axios'

  export default {
    components: {
      Card,
      UserCard,
      UserProfile
    },
    beforeMount () {
      this.getUser()
    },
    data () {
      return {
        user: {},
        api_response: ''
      }
    },
    methods: {
      getUser () {
        axios.get(this.$apiLink + '/user')
          .then(response => {
            this.user = response.data
          })
      },
      updateUser (currentData) {
        axios.post(this.$apiLink + '/user', { body: (currentData) })
          .then(response => {
            this.api_response = response.data.status
          })
      },
      renewApiKey(currentData) {
          axios.post(this.$apiLink + '/apikey', { body: (currentData) })
              .then(response => {
                  this.api_response = response.data.status
                  if (this.api_response === 'ok') {
                      this.getUser()
                  }
              })
      }
    }
  }
</script>
<style>

</style>
