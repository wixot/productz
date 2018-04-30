<script>
    import {Bar, mixins} from 'vue-chartjs'

    const {reactiveProp} = mixins

    export default {
        extends: Bar,
        mixins: [reactiveProp],
        props: [
            'chartData',
            'chartLabels'
        ],
        // mounted() {
        //     // Overwriting base render method with actual data.
        //     this.renderChart(this.chartData, {responsive: false})
        // },
        data() {
            return {
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            },
                            gridLines: {
                                display: true
                            }
                        }],
                        xAxes: [{
                            gridLines: {
                                display: false
                            }
                        }]
                    },
                    legend: {
                        display: true
                    },
                    responsive: true,
                    maintainAspectRatio: false
                }
            }
        },
        mounted() {
            this.renderChart({
                labels: this.chartLabels,
                datasets: this.chartData
            }, this.options)
        },
    }
</script>

<style>
</style>