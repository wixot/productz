<script>
    import {Bar, mixins} from 'vue-chartjs'
    import {createChart} from './utils.js'

    const {reactiveProp} = mixins

    export default {
        extends: Bar,
        mixins: [reactiveProp],
        props: [
            'chartData',
            'filters',
            'name'
        ],
        computed: {
          filtercont : function () {
              return [this.filters.metric, this.chartData]
          },
        },
        watch: {
          filtercont () {
              this.updateChart()
          }
        },
        data() {
            return {
                options: {
                    scales: {
                        yAxes: [{
                            stacked: true,
                            ticks: {
                                beginAtZero: true
                            },
                            gridLines: {
                                display: true
                            },
                        }],
                        xAxes: [{
                            gridLines: {
                                display: true
                            },

                        }]
                    },
                    legend: {
                        display: true
                    },
                    maintainAspectRatio: false,
                    responsive: true,
                }
            }
        },
        mounted() {
            createChart(this.chartData , this.filters)
                .then(response => {
                    this.renderChart({labels: response.labels, datasets : response.chartData}, this.options)

                });
        },
        updated() {
            createChart(this.chartData , this.filters)
                .then(response => {
                    this.renderChart({labels: response.labels, datasets : response.chartData}, this.options)

                });
        },
        methods: {
            updateChart () {
                createChart(this.chartData , this.filters)
                .then(response => {
                    this.renderChart({labels: response.labels, datasets : response.chartData}, this.options)

                });
            },

        }
    }
</script>

<style>
</style>