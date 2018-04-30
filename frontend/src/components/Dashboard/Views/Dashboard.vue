<template>
    <div>
        <div v-for="app in apps">
            <card id="appsData">
                <div align="center">
                    <button id="appDetail" class="btn-danger" v-on:click="routeDetails(app.name)">{{app.name}}
                    </button>
                </div>
            </card>

            <div class="row">
                <card id="AdRevenue" class="col-md-6">

                </card>

                <card id="orderRevenue" class="col-md-6">

                </card>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import Card from 'src/components/UIComponents/Cards/Card.vue'

    export default {
        components: {
            Card,
        },
        props: {},
        methods: {
            routeDetails(app) {
                this.$router.push("/details/" + app)
            }
        },
        data() {
            return {
                apps: null,
                dates: null
            }
        },
        beforeCreate() {
            axios.get(this.$apiLink + '/apps')
                .then(response => {
                    this.apps = response.data
                })
        },


    }

</script>

<style>

</style>