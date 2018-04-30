
import axios from 'axios'
import {apiLink} from 'src/main'
function getRandomColour() {
    return Math.random() * 0xFF | 0
}


function extapis(platform, providers, app) {
    return new Promise(resolve => {
    var extapis_data = {};
    for (let i = 0; i < providers.length; i++) {
        axios.get(apiLink + '/credentialsdata?provider=' + providers[i] + '&app=' + app + '&platform=' + platform)
            .then(response => {
                extapis_data[providers[i]] = response.data
            })
    }
    resolve({'extapis_data' : extapis_data})
        })
}


export function requestChartData(app , filters) {
    return new Promise(resolve => {
    axios.get(apiLink + '/data?app=' + app +  '&start_date=' +
            filters.startDate + '&end_date=' + filters.endDate )
            .then(response => {
                resolve(response.data)
            })
            .catch(e => {
                this.errors.push(e)
            })

})
}

export function createChart(game_data, filters) {
    return new Promise(resolve => {
    var endDate =  new Date(filters.endDate);
    var startDate =  new Date(filters.startDate);
    var labels = []
    for (let i = startDate.getTime(); i < endDate.getTime(); i=i+86400000) {
        var date = new Date(i)
        labels.push(date.toISOString().split('T')[0])
    }

    var chartData = [];
    for (const [provider , provider_data] of Object.entries(game_data)) {
        for (const [extapi , extapi_data] of Object.entries(provider_data)) {
            var column_data = extapi_data[filters.metric]


            var provider_labels = extapi_data['date_of_revenue'];
            var  new_chart_data = [];

            for (var i = 0 ; i <labels.length; i++) {
                if (provider_labels.indexOf(labels[i]) !== -1) {
                        new_chart_data.push(column_data[provider_labels.indexOf(labels[i])]);
                } else {
                    var x = 0;
                    new_chart_data.push(x);
                }
            }

            chartData.push({
                                label: provider + extapi,
                                borderColor: 'transparent',
                                pointBackgroundColor: 'white',
                                borderWidth: 1,
                                pointBorderColor: '#249EBF',
                                backgroundColor: 'rgba(' + getRandomColour() + ',' + getRandomColour() + ',' + getRandomColour() + ',0.7)',
                                stack: "0",
                                data: new_chart_data
                            })

        }
    }
    resolve({'labels' : labels , 'chartData' : chartData})
    })
}