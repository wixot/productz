 <template>
  <div>

    <div>
      <card>
          <div align="center">
          <h4 class="card-title">AD NETWORKS</h4>
          <button  class="btn btn-info btn-fill " v-on:click="OpendivStatus('chartboost')">
                Chartboost
          </button>
          <button class="btn btn-info btn-fill " v-on:click="OpendivStatus('unityads')">
                UnityAds
          </button>
          <button class="btn btn-info btn-fill " v-on:click="OpendivStatus('facebook')">
                Facebook
          </button>
          <button  class="btn btn-info btn-fill " v-on:click="OpendivStatus('admob')">
                Admob
          </button>
            </div>
      </card>
       <card>
          <div align="center">
           <h4 class="card-title">PRODUCTS NETWORKS</h4>
              <button  class="btn btn-info btn-fill " v-on:click="OpendivStatus('play')">
                    Android
              </button>
              <button class="btn btn-info btn-fill " v-on:click="OpendivStatus('itunes')">
                    IOS
              </button>

          </div>
       </card>
    </div>


    <net-chartboost v-if="divStatus === 'chartboost' " :chartboostData="networks.chartboost"
                    :updateNetwork="updateNetwork"
                    :createNetwork="createNetwork"
                    :deleteNetwork="deleteNetwork"
    >
    </net-chartboost>

    <net-unity  v-if="divStatus === 'unityads' " :unityAdsData="networks.unity_ads"
               :updateNetwork="updateNetwork"
               :createNetwork="createNetwork"
               :deleteNetwork="deleteNetwork"
    >
    </net-unity>

    <net-facebook v-if="divStatus === 'facebook' " :facebookData="networks.facebook"
                  :updateNetwork="updateNetwork"
                  :createNetwork="createNetwork"
                  :deleteNetwork="deleteNetwork"
    >
    </net-facebook>

    <net-admob v-if=" divStatus === 'admob' " :admobData="networks.admob"
               :updateNetwork="updateNetwork"
               :createNetwork="createNetwork"
               :deleteNetwork="deleteNetwork"
    >
    </net-admob>

      <android-network v-if=" divStatus === 'play' " :androidData="networks.play"
               :updateNetwork="updateNetwork"
               :createNetwork="createNetwork"
               :deleteNetwork="deleteNetwork">
      </android-network>

      <ios-network v-if=" divStatus === 'itunes' " :iosData="networks.itunes"
               :updateNetwork="updateNetwork"
               :createNetwork="createNetwork"
               :deleteNetwork="deleteNetwork">
      </ios-network>
</div>
</template>


<script>
  import Card from 'src/components/UIComponents/Cards/Card.vue'
  import NetAdmob from 'src/components/Dashboard/Views/Networks/NetAdmob.vue'
  import NetChartboost from 'src/components/Dashboard/Views/Networks/NetChartboost.vue'
  import NetUnity from 'src/components/Dashboard/Views/Networks/NetUnity.vue'
  import NetFacebook from 'src/components/Dashboard/Views/Networks/NetFacebook.vue'
  import AndroidNetwork from 'src/components/Dashboard/Views/ProductsNetworks/AndroidNetwork.vue'
  import IosNetwork from 'src/components/Dashboard/Views/ProductsNetworks/IosNetwork.vue'
  import axios from 'axios'

  export default {
    components: {
      Card,
      NetAdmob,
      NetChartboost,
      NetFacebook,
      NetUnity,
      IosNetwork,
      AndroidNetwork
    },
    created () {
      this.getNetworks('chartboost')
      this.getNetworks('admob')
      this.getNetworks('unity_ads')
      this.getNetworks('facebook')
      this.getNetworks('play')
      this.getNetworks('itunes')
    },
    data () {
      return {
        divStatus: '',
          auth_url: '',
        networks: {
            chartboost: '',
            unity_ads: '',
            facebook: '',
            admob: '',
            play: '',
            itunes: ''
        }
      }
    },
    methods: {
      OpendivStatus: function (currentDiv) {
        if (this.divStatus !== currentDiv) {
          this.divStatus = currentDiv
        } else {
          this.divStatus = ''
        }
      },
      getNetworks (provider) {
        axios.get(this.$apiLink + '/network?provider=' + provider)
         .then(response => {
             this.networks[provider] = response.data
         })
      },
      createNetwork (currentData, credentials) {
        axios.post(this.$apiLink + '/network', {
          body: (currentData), credentials: (credentials)
        })
          .then(response => {
              if (response.data.status === 'google') {
                  this.auth_url = response.data.auth_url
                  window.location.replace(this.auth_url)
              }
              if (response.data.status === 'ok') {
                  alert('OK')
              }
              if (response.data.status === 'error') {
                  alert('Error')
              }
          })
          .catch(e => {
            this.errors.push(e)
          })
      },
      updateNetwork (currentData, credentials) {
        axios.patch(this.$apiLink + '/network', {
          body: (currentData), credentials: (credentials)
        })
          .then(response => {
            if (response.data.status === 'google') {
                  this.auth_url = response.data.auth_url
                  window.location.replace(this.auth_url)
              }
              if (response.data.status === 'ok') {
                  alert('OK')
              }
              if (response.data.status === 'error') {
                  alert('Error')
              }
          })
          .catch(e => {
            this.errors.push(e)
          })
      },
      deleteNetwork (currentData) {
        axios.delete(this.$apiLink + '/network?id=' + currentData['_id']['$oid'])
          .then(response => {
            this.api_response = response.data.status
            alert(this.api_response)
          })
          .catch(e => {
            this.errors.push(e)
          })
        location.reload()
      }
    }
  }
</script>
<style>
</style>