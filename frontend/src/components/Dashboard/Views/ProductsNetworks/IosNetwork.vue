<template>
    <div>

        <div>
            <card>
                IOS Products Accounts
                <l-table class="table table-hover table-striped" :columns="tableColumns" :data="iosData">
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
                          v-model="newIos.name">
                </fg-input>
                <fg-input type="text"
                          label="User Name"
                          placeholder="name"
                          v-model="newIos.username">
                </fg-input>
                <fg-input type="text"
                          label="Password"
                          placeholder="password"
                          v-model="newIos.password">
                </fg-input>
                <button class="btn btn-info btn-fill align-self-auto" v-on:click="createFirst(newIos)">
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
                    <fg-input type="text"
                              label="User Name"
                              placeholder="name"
                              v-model="rowData.credentials.username">
                    </fg-input>
                    <fg-input type="text"
                              label="Password"
                              placeholder="password"
                              v-model="rowData.credentials.password">
                    </fg-input>
                    <button class="btn btn-info btn-fill align-self-auto" v-on:click="updateFirst(rowData)">
                        Update
                    </button>
                </card>
            </div>
        </card>


    </div>
</template>
<script>
    import Card from 'src/components/UIComponents/Cards/Card.vue'
    import LTable from 'src/components/UIComponents/Table.vue'

    export default {
        components: {
            Card,
            LTable
        },
        props: ['iosData', 'updateNetwork', "createNetwork", "deleteNetwork"],
        data() {
            return {
                tableColumns: ['Name', 'Active', 'Operations'],
                currentType: '',
                rowData: {},
                newIos: {
                    provider: 'itunes',
                    active: 'false'
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
                let credentials = {'username': currentData.username, 'password': currentData.password}
                this.createNetwork(currentData, credentials)
            },
            updateFirst(rowData) {
                let credentials = {
                    'username': rowData.credentials.username,
                    'password': rowData.credentials.password
                }
                this.updateNetwork(rowData, credentials)
            },
            handleDelete(row) {
                this.deleteNetwork(row)
            }
        }
    }

</script>
<style>

</style>
