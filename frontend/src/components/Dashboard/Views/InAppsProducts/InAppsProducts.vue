<template>
    <div class="container">
        <table>
            <thead class="align-items-center">
            <tr>
                <th>
                    <button class="btn btn-primary" v-on:click="updateAllInApps()">Update All In Apps</button>
                </th>
            </tr>
            </thead>
            <hr/>
            <tr>
                <th>Image</th>
                <th>Provider</th>
                <th>SKU</th>
                <th>Name</th>
                <th>Category</th>
                <th>Resource</th>
                <th>Amount</th>
                <th>Is active?</th>
                <th>Edit</th>
            </tr>
            <draggable v-model="products" :element="'tbody'">
                <tr v-for="row in products" :key="row.sku" :options="{group:'provider'}"
                    :element="'tbody'" class="position-static">


                    <td v-if="row.image_url">
                        <img v-bind:src="$apiLink+'/'+row.image_url" height="120px;"
                             style="align: right; height: 100px;"/>

                    </td>
                    <td v-else>
                        <code>No</code><br/>
                        <code>Image</code><br/>
                        <code>Uploaded</code><br/>
                    </td>

                    <td>{{row.provider}}</td>
                    <td>{{row.sku}}</td>
                    <td>{{row.name}}</td>
                    <td>{{row.category}}</td>


                    <td>{{row.resource}}</td>
                    <td>{{row.amount}}</td>
                    <td>{{row.active}}</td>
                    <td>
                        <span>
                            <button style="color: #3e8f3e" class="btn btn-icon btn-info" type="button"
                                    v-on:click="modalUtils(row)">
                            </button>
                        </span>
                    </td>

                </tr>
            </draggable>
        </table>


        <div class="modal fade" id="inAppModal" tabindex="-1" role="dialog" aria-labelledby="inAppModal"
             aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel"><span><b>{{modalData.provider}}: </b></span>{{modalData.sku}}
                        </h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        Name:<b>{{modalData.name}}</b><br>
                        Labels:<b v-for="key,value in modalData.labels"><br>{{value }}
                        <span>title:{{key.title}}: </span>desc:{{key.description}}
                    </b><br>
                        Category:<b>{{modalData.category}}</b><br>
                        Resource:<b>{{modalData.resource}}</b><br>
                        Amount:<b>{{modalData.amount}}</b><br>
                        Image:<b>{{modalData.image_url}}</b><br>


                        billing_period:<b>{{modalData.billing_period}}</b><br>
                        trial_period:<b>{{modalData.trial_period}}</b><br>
                        grace_period: <b>{{modalData.grace_period}}</b><br>
                        Active:<b>{{modalData.active}}</b><br>

                        Resource:<input type="text" class="form-control" id="resource" v-model="modalData.resource">


                        Amount:<input type="text" class="form-control" id="amount" v-model="modalData.amount">

                        Product Order:<input type="text" class="form-control" id="productorder"
                                             v-model="modalData.product_order">


                        Unity_Category:
                        <b-form-select v-model="modalData.unity_category" :options="unity_options" class="mb-3"
                                       size="sm"/>


                        Image:
                        <b-form-file ref="fileinput" v-model="modalData.image" :state="Boolean(modalData.image)"
                                     placeholder="Choose a file..."></b-form-file>
                        <button type="button" class="btn btn-primary" v-on:click="uploadImage()">Upload
                        </button>
                        <div class="mt-3">Selected file: {{modalData.image && modalData.image.name}}</div>

                        <div v-if="modalData.image_url">
                            <img v-bind:src="$apiLink+'/'+modalData.image_url" style="width: 450px; height: 350px;"/>
                        </div>


                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" v-on:click="updateProducts()">Update
                        </button>
                    </div>
                </div>
            </div>
        </div>


    </div>

</template>

<script>
    import Card from 'src/components/UIComponents/Cards/Card.vue'
    import LTable from 'src/components/UIComponents/Table.vue'
    import draggable from 'vuedraggable'
    import axios from 'axios'

    export default {
        components: {
            Card,
            LTable,
            draggable
        },
        props: ['app'],
        created() {
            this.getInApps(this.app['_id']['$oid'])
        },
        updated () {
            axios.post(this.$apiLink + '/updateiapsorder', {"data": this.products.map(item => item._id)})
                    .then(response => {
                        console.log(response)
                    })
                    .catch(e => {
                        console.log(evt)
                        // this.errors.push(e)
                    })
        },
        data() {
            return {
                tableColumns: ['EDIT', 'Provider', 'SKU', 'Name', 'Category', 'Resource', 'Amount', 'Image', 'Active?'],
                products: [],
                modalData: {},
                url: '',
                response: '',
                selected: null,
                unity_options: [
                    {value: null, text: 'Unity Category'},
                    {value: 'Consumable', text: 'Consumable'},
                    {value: 'NonConsumable', text: 'NonConsumable'},
                    {value: 'Subscription', text: 'Subscription'},

                ]
            }
        },

        methods: {
            getInApps(app) {
                axios.get(this.$apiLink + '/inappsproducts?app=' + app)
                    .then(response => {
                        this.products = response.data.data
                    })
            },
            modalUtils(rowData) {
                this.modalData = rowData
                $('#inAppModal').modal('show')
            },
            updateProducts() {
                axios.post(this.$apiLink + '/inappsproducts?app=' + this.app['_id']['$oid'], {
                    body: (this.modalData)
                })
                    .then(response => {
                        this.api_response = response.data.status
                        if (this.api_response === 'ok') {
                            $('#inAppModal').modal('hide')
                        }

                    })
                    .catch(e => {
                        this.errors.push(e)
                    })
            },
            uploadImage() {
                var data = new FormData()
                data.append('file', this.modalData.image)
                axios.post(this.$apiLink + '/media/files/iaps', data)
                    .then(response => {
                        this.api_response = response.data.status
                        this.url = response.data.file_path
                        if (this.api_response === 'ok') {
                            this.modalData.image_url = this.url
                            this.$refs.fileinput.reset();
                        }
                    })
                    .catch(e => {
                        this.errors.push(e)
                    })
            },
            updateAllInApps() {
                axios.get(this.$apiLink + '/inappsproducts/update?app=' + this.app['_id']['$oid'])
                    .then(response => {
                        this.response = response.data.status
                        if (this.response === 'ok') {
                            alert('ok')

                        }
                    })

            },
        }
    }

</script>
<style>

</style>
