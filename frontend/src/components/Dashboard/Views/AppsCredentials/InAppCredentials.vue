<template>
    <div>
        <div align="center">
            <h2>App: {{app.name}}</h2>
            <div>
                <card>
                    <div align="right">
                        <h2 class="card-title">Google Play</h2>
                    </div>
                    <div>
                        <fg-input type="text"
                                  label="Package Name"
                                  placeholder="package_name"
                                  v-model="all_credentials.play.package_name">
                        </fg-input>
                    </div>
                    <div align="center" v-for="item in all_credentials.play.allData">
                        <input type="radio" v-bind:id="item.id" v-model="all_credentials.play.network_id"
                               v-bind:value="item.id">
                        {{item.name}}
                    </div>
                    <div align="left">
                        <button class="btn btn-info btn-fill "
                                v-on:click="createNetwork(all_credentials.play.package_name , all_credentials.play.network_id, 'play' , app['_id']['$oid'] )">
                            SAVE
                        </button>
                    </div>

                </card>
                <card>
                    <div align="right">
                        <h2 class="card-title">Apple Store</h2>
                    </div>
                    <div>
                        <fg-input type="text"
                                  label="App Id"
                                  placeholder="app_id"
                                  v-model="all_credentials.itunes.package_name">
                        </fg-input>
                    </div>
                    <div v-for="item in all_credentials.itunes.allData">
                        <input type="radio" v-bind:id="item.id" v-model="all_credentials.itunes.network_id"
                               v-bind:value="item.id">
                        {{item.name}}
                    </div>
                    <div align="left">
                        <button class="btn btn-info btn-fill "
                                v-on:click="createNetwork(all_credentials.itunes.package_name , all_credentials.itunes.network_id, 'itunes' , app['_id']['$oid'] )">
                            SAVE
                        </button>
                    </div>
                </card>

            </div>
        </div>
    </div>
</template>

<script>
    import Card from 'src/components/UIComponents/Cards/Card.vue'
    import axios from 'axios'

    export default {
        components: {
            Card
        },
        props: ['app'],
        created() {
            this.getNetworkData('play', this.app['_id']['$oid'])
            this.getNetworkData('itunes', this.app['_id']['$oid'])
        },
        data() {
            return {
                all_credentials: {
                    play: {
                        allData: {},
                        network_id: '',
                        package_name: ''
                    },
                    itunes: {
                        allData: {},
                        network_id: '',
                        package_name: ''
                    }
                }
            }
        },
        methods: {
            getNetworkData(provider, app) {
                axios.get(this.$apiLink + '/appcredentials?provider=' + provider + '&app=' + app)
                    .then(response => {
                        this.all_credentials[provider]['allData'] = response.data.all_data
                        this.all_credentials[provider]['network_id'] = response.data.network_id
                        this.all_credentials[provider]['package_name'] = response.data.package_name
                    })

            },
            createNetwork(currentData, network_id, provider, app) {
                axios.post(this.$apiLink + '/appcredentials?provider=' + provider + '&app=' + app, {
                    body: (currentData), network_id: (network_id)
                })
                    .then(response => {
                        this.api_response = response.data.status
                        alert(this.api_response)
                    })
                    .catch(e => {
                        this.errors.push(e)
                    })
            },
        }
    }

</script>
<style>

</style>
