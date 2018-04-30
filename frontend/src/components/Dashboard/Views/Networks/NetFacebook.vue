<template>
    <div>
        <div>
            <card>
                FACEBOOK Accounts
                <l-table class="table table-hover table-striped" :columns="tableColumns" :data="facebookData">
                    <template slot="columns">
                        <th>Name</th>
                        <th>Active</th>
                        <th>Operations</th>
                    </template>

                    <template slot-scope="{row}">
                        <td><b>{{row.name}}</b></td>
                        <td>{{row.active}}</td>
                        <td>
                            <button class="btn btn-icon btn-info" @click="handleEdit(row)"><i class="fa fa-edit"></i>
                            </button>
                            <button class="btn btn-icon btn-danger" @click="handleDelete(row)"><i
                                    class="fa fa-trash"></i></button>
                        </td>
                    </template>

                </l-table>
                <div align="left">
                    <button class="btn btn-info btn-fill align-self-auto" v-on:click="divStatus('create')">
                        CREATE
                    </button>
                </div>
            </card>
        </div>


        <div align="center" v-if="currentType === 'create'  ">


            <card>
                <fg-input type="text"
                          label="Name"
                          placeholder="name"
                          v-model="newFacebook.name">
                </fg-input>

                <div class="facebook-login">
                    <button class="btn btn-info btn-fill align-self-auto" v-on:click="buttonClicked()">
                        <i v-if="isWorking">{{getButtonText}}</i>
                        <i v-if="!isWorking">{{getButtonText}} </i>
                    </button>
                </div>

                <button class="btn btn-info btn-fill align-self-auto" v-on:click="createFirst(newFacebook)">
                    SAVE
                </button>
            </card>
        </div>


        <card v-if="currentType === 'edit'  ">
            <div align="right">
                <button class="btn top-right" v-on:click="closeDiv()">
                    X
                </button>
            </div>

            <div align="center">
                <card>
                    <fg-input type="text"
                              label="Name"
                              placeholder="name"
                              v-model="rowData.name">
                    </fg-input>

                    <div class="facebook-login">
                        <button class="btn btn-info btn-fill align-self-auto" v-on:click="buttonClicked()">
                            <i v-if="isWorking">{{getButtonText}}</i>
                            <i v-if="!isWorking">{{getButtonText}} </i>
                        </button>
                    </div>


                    <button class="btn btn-info btn-fill align-self-auto" v-on:click="updateFirst(rowData)">
                        Update
                    </button>
                </card>
            </div>
        </card>
        <!--<div id="fb-root"></div>-->
        <!--<fb:login-button scope="public_profile,email" :onlogin="createFirst()">-->
        <!--</fb:login-button>-->
        <!--<div class="fb-login-button" data-max-rows="1" data-size="large" data-button-type="continue_with"-->
        <!--data-show-faces="false" data-auto-logout-link="true" data-use-continue-as="true"></div>-->
    </div>
</template>
<script>
    import Card from 'src/components/UIComponents/Cards/Card.vue'
    import LTable from 'src/components/UIComponents/Table.vue'
    import {
        loadFbSdk,
        getFbLoginStatus,
        fbLogout,
        fbLogin
    } from './facebook_utils.js'

    export default {
        components: {
            Card,
            LTable,
        },
        props: ['facebookData', 'updateNetwork', "createNetwork", "deleteNetwork"],
        data() {
            return {
                tableColumns: ['Name', 'Active', 'Operations'],
                currentType: '',
                rowData: {},
                newFacebook: {
                    provider: 'facebook',
                    active: 'false'
                },
                facebookResponseData: {},
                isWorking: false,
                isConnected: false,
                appId: '<MUST BE INITIALIZED>',
                version: 'v2.8',
                logoutLabel: 'Log out from Facebook',
                loginLabel: 'Log in to Facebook',
                loginOptions: {
                    scope: 'email,read_insights'
                }
            }
        },
        mounted() {
            this.isWorking = true
            loadFbSdk(this.appId, this.version)
                .then(getFbLoginStatus)
                .then(response => {
                    if (response.status === 'connected') {
                        this.isConnected = true
                        this.facebookResponseData = response
                    }
                    this.isWorking = false
                    /** Event `get-initial-status` to be deprecated in next major version! */
                })
        },
        computed: {
            getButtonText() {
                switch (this.isConnected) {
                    case true:
                        return this.logoutLabel
                    case false:
                        return this.loginLabel
                    default:
                        return 'this is default'
                }
            }
        },
        methods: {
            divStatus(currentType) {
                if (this.currentType !== currentType) {
                    this.currentType = currentType
                } else {
                    this.currentType = ''
                }
            },
            handleEdit(row) {
                this.currentType = 'edit'
                this.rowData = row
            },
            closeDiv() {
                this.currentType = ''
            },
            createFirst(currentData) {
                if (this.facebookResponseData.status === 'connected') {
                    let credentials = {'access_token': this.facebookResponseData.authResponse.accessToken}
                    this.createNetwork(currentData, credentials)
                }
                else {
                    alert('Please Login With Facebook')
                }
            },
            updateFirst(rowData) {
                if (this.facebookResponseData.status === 'connected') {
                    let credentials = {'access_token': this.facebookResponseData.authResponse.accessToken}
                    this.createNetwork(rowData, credentials)
                }
                else {
                    alert('Please Login With Facebook')
                }
            },
            handleDelete(row) {
                this.deleteNetwork(row)
            },
            buttonClicked() {
                this.$emit('click')
                if (this.isConnected) {
                    this.logout()
                } else {
                    this.login()
                }
            },
            login() {
                this.isWorking = true
                fbLogin(this.loginOptions)
                    .then(response => {
                        if (response.status === 'connected') {
                            this.isConnected = true
                            this.facebookResponseData = response
                        } else {
                            this.isConnected = false
                        }
                        this.isWorking = false
                    })
            },
            logout() {
                this.isWorking = true
                fbLogout()
                    .then(response => {
                            this.isWorking = false
                            this.isConnected = false
                            this.facebookResponseData = {}
                        }
                    )
            }
        }
    }

</script>
<style>

</style>
