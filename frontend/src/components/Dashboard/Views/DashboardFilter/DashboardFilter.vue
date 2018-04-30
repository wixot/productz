<template>
    <div>
        <div class="card">


                <div class="form-group row" style="margin-top: 15px;">
                    <label class="col-2 col-form-label">Date</label>
                    <div class="col-3">
                        <input class="form-control" type="date" id="startDate"
                               v-model="filters.start">
                    </div>
                    <div class="col-3">
                        <input class="form-control" type="date" id="endDate"
                               v-model="filters.end">

                    </div>

                </div>

                <div class="row" >
                    <label class="col-2 col-form-label">Provider</label>
                    <div v-for="item in filters.adFilter.options" >
                            <div class="custom-control custom-checkbox">
                      <input type="checkbox" class="custom-control-input" id="item.value" style="margin-left: 5px;" v-model="selected">
                      <label class="custom-control-label" for="item.value" style="margin-left: 5px;">{{item.text}}</label>
                        </div>
                    </div>
                </div>
        </div>
    </div>
</template>

<script>

    export default {
        components: {},
        data() {
            return {
                filters: {
                    adFilter: {
                        options: [
                            {text: 'Chartboost', value: 'chartboost'},
                            {text: 'Admob', value: 'admob'},
                            {text: 'Unity Ads', value: 'unity_ads'},
                            {text: 'Facebook', value: 'facebook'}
                        ],
                        selected: []
                    },
                    start: '',
                    end: ''
                },
                type: 'date'
            }
        }
    }
</script>
<style>

</style>
