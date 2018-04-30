<template>
    <div class="allPage">
        <div class="row">
            <card class="col-md-6">

                <b-button-group>
                    <b-button v-for="metric in metrics" :pressed.sync="metric.state" :variant="metric.variant"
                              :key="metric.key"
                              v-on:click="updateChart(metric.value)">
                        {{ metric.name}}
                    </b-button>
                </b-button-group>
            </card>


            <card class="col-md-6">
                <b-container fluid>
                    <b-row class="my-1">
                        <b-col sm="6">
                            <b-form-input :id="`type-date`" type="date" v-model="filters.startDate">
                            </b-form-input>
                        </b-col>

                        <b-col sm="6">
                            <b-form-input :id="`type-date`" type="date" v-model="filters.endDate">
                            </b-form-input>
                        </b-col>
                    </b-row>
                </b-container>
            </card>
        </div>

        <div v-if="status === 'ready' " ref="dashboard">
            <div v-for="value , key in gameData">
                <card>
                    <ad-line-chart  :chartData="value" :name="key"  :filters="filters">  </ad-line-chart>
                </card>
            </div>
        </div>

    </div>
</template>

<script>
    import axios from 'axios'
    import Card from 'src/components/UIComponents/Cards/Card.vue'
    import {requestChartData} from './utils.js'
    import AdLineChart from 'src/components/Dashboard/Views/Dashboard/AdRevenueLineChart.vue'


    export default {
        components: {
            Card,
            AdLineChart

        },
        props: {},
        computed: {
          dateComp : function () {
              return [this.filters.endDate , this.filters.startDate]
          },
            metricComp: function () {
                return [this.filters.metric]
            }
        },
        watch: {
          dateComp () {
              this.status = 'wait';
              this.getChartData()
          },
            metricComp: function () {
              setTimeout(function () {
                  this.status = 'ready'
              }.bind(this),50);

            }
        },
        data() {
            return {
                metrics: [
                    {
                        name: 'REVENUE',
                        value: 'revenue',
                        state: true,
                        variant: 'success',
                        caption: 'Toggle 1',
                        key: '1'
                    },
                    {
                        name: 'ECPM',
                        value: 'ecpm',
                        state: false,
                        variant: 'success',
                        caption: 'Toggle 1',
                        key: '2'
                    },

                    {
                        name: 'CLICK',
                        value: 'clicks',
                        state: false,
                        variant: 'success',
                        caption: 'Toggle 1',
                        key: '3'
                    },

                    {
                        name: 'VIEWS',
                        value: 'views',
                        state: false,
                        variant: 'success',
                        caption: 'Toggle 1',
                        key: '4'
                    },
                    {
                        name: 'IMPRESSIONS',
                        value: 'impressions',
                        state: false,
                        variant: 'success',
                        caption: 'Toggle 1',
                        key: '5'
                    },

                    {
                        name: 'CTR',
                        value: 'ctr',
                        state: false,
                        variant: 'success',
                        caption: 'Toggle 1',
                        key: '6'
                    },

                    {
                        name: 'CPC',
                        value: 'cpc',
                        state: false,
                        variant: 'success',
                        caption: 'Toggle 1',
                        key: '7'
                    },
                    {
                        name: 'RPM',
                        value: 'rpm',
                        state: false,
                        variant: 'success',
                        caption: 'Toggle 1',
                        key: '8'
                    },
                    {
                        name: 'CPCV',
                        value: 'cpcv',
                        state: false,
                        variant: 'success',
                        caption: 'Toggle 1',
                        key: '9'
                    },
                ],
                app: '',
                filters: {
                    metric: 'revenue',
                    endDate: (new Date()).toISOString().split('T')[0],
                    startDate: (new Date(new Date().getTime() - (86400000 * (7)))).toISOString().split('T')[0],
                },
                gameData: null,
                status: '',
            }
        },
        created() {
            this.app = this.$route.params.app
            this.getChartData()
        },

        methods: {
            getChartData () {
            requestChartData(this.app, this.filters)
                .then(response => {
                    this.gameData = response
                    this.status = 'ready'
                });
            },
            updateChart(value) {
                if (this.filters.metric !== value) {
                    this.status = 'wait'
                    this.filters.metric = value
                }
            }
        },
    }
</script>

<style>
    .allPage {
        margin-left: 10px;
    }
</style>

