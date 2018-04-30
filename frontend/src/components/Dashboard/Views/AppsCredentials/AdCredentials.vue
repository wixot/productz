<template>
    <div>
        <card>
            <div align="center">
                <h2 class="card-title">Chartboost</h2>
            </div>
            <div v-for="(value ,key) in all_credentials.chartboost.allData">
                <h3 style="color: #dc143c">Chartboost Account = {{key}}</h3>
                <div v-for="item in value">
                    <div v-if="isExist(item.id , 'chartboost')">
                        <button style="color: #3e8f3e" class="btn btn-link" type="button" data-toggle="collapse"
                                v-bind:data-target="'#'+item.id" aria-expanded="false" v-bind:aria-controls="item.id">
                            {{item.name}} -- {{item.id}}
                        </button>
                    </div>
                    <div v-else>
                        <button style="color: #3B0D06" class="btn btn-link" type="button" data-toggle="collapse"
                                v-bind:data-target="'#'+item.id" aria-expanded="false" v-bind:aria-controls="item.id">
                            {{item.name}} -- {{item.id}}
                        </button>
                    </div>
                    <div class="collapse" v-bind:id="item.id">
                        <card>
                            <div class="row">
                                -> {{item.name}}<br>
                                -> {{item.id}}<br>
                                -> {{item.nickname}}


                                <div style="margin-left: 30px;">
                                    <input type="radio" v-bind:id="item.id + '1' " v-model="item.platform" value="ios">
                                    IOS
                                    <input type="radio" v-bind:id="item.id + '1' " v-model="item.platform"
                                           value="android"> Android
                                </div>
                            </div>
                            <div align="right">
                                <button class="btn btn-secondary "
                                        v-on:click="createNetwork(item , 'chartboost', app['_id']['$oid'] )">
                                    Save
                                </button>
                                <button v-if="isExist(item.id , 'chartboost')" class="btn btn-danger"
                                        v-on:click="deleteNetwork(item , 'chartboost' ,app['_id']['$oid'])">
                                    Delete
                                </button>
                            </div>
                        </card>
                    </div>
                </div>
            </div>
        </card>


        <card>
            <div align="center">
                <h2 class="card-title">Unity-Ads</h2>
            </div>
            <div v-for="(value ,key) in all_credentials.unity_ads.allData">
                <h3 style="color: #dc143c">Unity-ADs Account = {{key}}</h3>
                <div v-for="item in value">
                    <div v-if="isExist(item.id , 'unity_ads')">
                        <button style="color: #3e8f3e" class="btn btn-link" type="button" data-toggle="collapse"
                                v-bind:data-target="'#'+item.id" aria-expanded="false" v-bind:aria-controls="item.id">
                            {{item.name}} -- {{item.id}}
                        </button>
                    </div>
                    <div v-else>
                        <button style="color: #3B0D06" class="btn btn-link" type="button" data-toggle="collapse"
                                v-bind:data-target="'#'+item.id" aria-expanded="false" v-bind:aria-controls="item.id">
                            {{item.name}} -- {{item.id}}
                        </button>
                    </div>
                    <div class="collapse" v-bind:id="item.id">
                        <card>
                            <div class="row">
                                -> {{item.name}}<br>
                                -> {{item.id}}<br>


                                <div style="margin-left: 30px;">
                                    <input type="radio" v-bind:id="item.id + '1' " v-model="item.platform" value="ios">
                                    IOS
                                    <input type="radio" v-bind:id="item.id + '1' " v-model="item.platform"
                                           value="android"> Android
                                </div>
                            </div>
                            <div align="right">
                                <button class="btn btn-secondary "
                                        v-on:click="createNetwork(item , 'unity_ads', app['_id']['$oid'] )">
                                    Save
                                </button>
                                <button v-if="isExist(item.id , 'unity_ads')" class="btn btn-danger"
                                        v-on:click="deleteNetwork(item , 'unity_ads' ,app['_id']['$oid'])">
                                    Delete
                                </button>
                            </div>
                        </card>
                    </div>
                </div>
            </div>
        </card>


        <card>
            <div align="center">
                <h2 class="card-title">Admob</h2>
            </div>
            <div v-for="(value ,key) in all_credentials.admob.allData">
                <h3 style="color: #dc143c">Admob Account = {{key}}</h3>
                <div v-for="item in value">
                    <div v-if="isExist(item.id , 'admob')">
                        <button style="color: #3e8f3e" class="btn btn-link" type="button" data-toggle="collapse"
                                v-bind:data-target="'#'+item.id" aria-expanded="false" v-bind:aria-controls="item.id">
                            {{item.name}} -- {{item.id}}
                        </button>
                    </div>
                    <div v-else>
                        <button style="color: #3B0D06" class="btn btn-link" type="button" data-toggle="collapse"
                                v-bind:data-target="'#'+item.id" aria-expanded="false" v-bind:aria-controls="item.id">
                            {{item.name}} -- {{item.id}}
                        </button>
                    </div>
                    <div class="collapse" v-bind:id="item.id">
                        <card>
                            <div class="row">
                                -> {{item.name}}<br>
                                -> {{item.id}}<br>


                                <div style="margin-left: 30px;">
                                    <input type="radio" v-bind:id="item.id + '1' " v-model="item.platform" value="ios">
                                    IOS
                                    <input type="radio" v-bind:id="item.id + '1' " v-model="item.platform"
                                           value="android"> Android
                                </div>
                            </div>
                            <div align="right">
                                <button class="btn btn-secondary "
                                        v-on:click="createNetwork(item , 'admob', app['_id']['$oid'] )">
                                    Save
                                </button>
                                <button v-if="isExist(item.id , 'admob')" class="btn btn-danger"
                                        v-on:click="deleteNetwork(item , 'admob' ,app['_id']['$oid'])">
                                    Delete
                                </button>
                            </div>
                        </card>
                    </div>
                </div>
            </div>
        </card>


        <card>
            <div align="center">
                <h2 class="card-title">Facebook</h2>
            </div>
            <div v-for="(value ,key) in all_credentials.facebook.allData">
                <h3 style="color: #dc143c">Facebook Account = {{key}}</h3>
                <div v-for="item in value">
                    <div v-if="isExist(item.id , 'facebook')">
                        <button style="color: #3e8f3e" class="btn btn-link" type="button" data-toggle="collapse"
                                v-bind:data-target="'#'+item.id" aria-expanded="false" v-bind:aria-controls="item.id">
                            {{item.name}} -- {{item.id}}
                        </button>
                    </div>
                    <div v-else>
                        <button style="color: #3B0D06" class="btn btn-link" type="button" data-toggle="collapse"
                                v-bind:data-target="'#'+item.id" aria-expanded="false" v-bind:aria-controls="item.id">
                            {{item.name}} -- {{item.id}}
                        </button>
                    </div>
                    <div class="collapse" v-bind:id="item.id">
                        <card>
                            <div class="row">
                                -> {{item.name}}<br>
                                -> {{item.id}}<br>


                                <div style="margin-left: 30px;">
                                    <input type="radio" v-bind:id="item.id + '1' " v-model="item.platform" value="ios">
                                    IOS
                                    <input type="radio" v-bind:id="item.id + '1' " v-model="item.platform"
                                           value="android"> Android
                                </div>
                            </div>
                            <div align="right">
                                <button class="btn btn-secondary "
                                        v-on:click="createNetwork(item , 'facebook', app['_id']['$oid'] )">
                                    Save
                                </button>
                                <button v-if="isExist(item.id , 'facebook')" class="btn btn-danger"
                                        v-on:click="deleteNetwork(item , 'facebook' ,app['_id']['$oid'])">
                                    Delete
                                </button>
                            </div>
                        </card>
                    </div>
                </div>
            </div>
        </card>


    </div>
</template>

<script>
    import axios from 'axios'
    import Card from "../../../UIComponents/Cards/Card";

    export default {
        components: {
            Card
        },
        props: ['app'],
        created() {
            this.getNetworkData('chartboost', this.app['_id']['$oid'])
            this.getNetworkData('unity_ads', this.app['_id']['$oid'])
            this.getNetworkData('facebook', this.app['_id']['$oid'])
            this.getNetworkData('admob', this.app['_id']['$oid'])
        },
        data() {
            return {
                all_credentials: {
                    chartboost: {
                        allData: {},
                        current_list: [],
                    },
                    unity_ads: {
                        allData: {},
                        current_list: [],
                    },
                    facebook: {
                        allData: {},
                        current_list: [],
                    },
                    admob: {
                        allData: {},
                        current_list: [],
                    },
                }
            }
        },
        methods: {
            isExist(item, provider) {
                for (var i = 0; i < this.all_credentials[provider].current_list.length; i++) {
                    if (this.all_credentials[provider].current_list[i].id === item) {
                        return true
                    }
                }
                return false
            },
            getNetworkData(provider, app) {
                axios.get(this.$apiLink + '/credentials?provider=' + provider + '&app=' + app)
                    .then(response => {
                        this.all_credentials[provider]['allData'] = response.data.all_data
                        this.all_credentials[provider]['current_list'] = response.data.credentials_list
                    })
            },
            createNetwork(currentData, provider, app) {
                axios.post(this.$apiLink + '/credentials?provider=' + provider + '&app=' + app, {
                    body: (currentData)
                })
                    .then(response => {
                        this.api_response = response.data.status
                        if (this.api_response === 'ok') {
                            this.getNetworkData(provider, app)
                        }
                    })
                    .catch(e => {
                        this.errors.push(e)
                    })
            },
            deleteNetwork(currentData, provider, app) {
                axios.delete(this.$apiLink + '/credentials?provider=' + provider + '&app=' + app + '&id=' + currentData.credentials_id, {})
                    .then(response => {
                        this.api_response = response.data.status
                        if (this.api_response === 'ok') {
                            this.getNetworkData(provider, app)
                        }
                    })
                    .catch(e => {
                        this.errors.push(e)
                    })

            }
        }
    }

</script>
<style>

</style>
