<template>

<div>
  <card>
  <l-table class="table table-hover table-striped" :columns="tableColumns" :data="apps">
    <template slot="columns">
          <th>App</th>
          <th>Update</th>
          <th>Credentials</th>
          <th>InAppCredentials</th>
          <th>InAppsData</th>
          <th>Delete</th>
      </template>
    <template slot-scope="{row}">
        <td><b>{{row.name}}</b></td>
        <td>
          <button class="btn btn-icon btn-info"  @click="divStatus(row , 'update')"><i class="fa fa-edit"></i></button>
        </td>
        <td>
          <button class="btn btn-icon btn-info"  @click="divStatus(row , 'adCredentials')"><i class="fa fa-edit"></i></button>
        </td>
        <td>
          <button class="btn btn-icon btn-info"  @click="divStatus(row , 'inApps')"><i class="fa fa-edit"></i></button>
        </td>
        <td>
          <button class="btn btn-icon btn-info"  @click="divStatus(row , 'inAppsData')"><i class="fa fa-edit"></i></button>
        </td>
        <td>
          <button class="btn btn-icon btn-danger" @click="deleteApp(row)"><i class="fa fa-trash"></i></button>
        </td>
      </template>
  </l-table>
    </card>

    <card v-if="rowDivStatus === 'update' ">
        <update-apps v-bind:rowData="rowData"> </update-apps>
    </card>

    <card v-if="rowDivStatus === 'adCredentials' ">
        <ad-credentials v-bind:app="rowData">

        </ad-credentials>
    </card>

    <card v-if="rowDivStatus === 'inApps' ">
        <in-app-credentials v-bind:app="rowData">
        </in-app-credentials>
    </card>

    <card v-if="rowDivStatus === 'inAppsData' ">
      <in-apps-data v-bind:app="rowData"></in-apps-data>
    </card>
</div>

</template>

<script>
  import Card from 'src/components/UIComponents/Cards/Card.vue'
  import LTable from 'src/components/UIComponents/Table.vue'
  import UpdateApps from 'src/components/Dashboard/Views/Apps/UpdateApps.vue'
  import AdCredentials from '../AppsCredentials/AdCredentials.vue'
  import InAppCredentials from 'src/components/Dashboard/Views/AppsCredentials/InAppCredentials.vue'
  import InAppsData from 'src/components/Dashboard/Views/InAppsProducts/InAppsProducts.vue'
  import axios from 'axios'

  export default {
    components: {
      Card,
      LTable,
      UpdateApps,
      AdCredentials,
      InAppCredentials,
      InAppsData
    },
    props: ['apps'],
    data () {
      return {
        tableColumns: ['App', 'Update', 'Credentials', 'InAppCredentials','InAppsData', 'Delete'],
        rowDivStatus: '',
        rowData: {},
      }
    },
    methods: {
      divStatus (row, divStatus) {
        if (this.rowDivStatus !== divStatus) {
          this.rowDivStatus = divStatus
          this.rowData = row
        } else {
          this.rowDivStatus = ''
          this.rowData = {}
        }
      },
      deleteApp (row) {
        axios.delete(this.$apiLink + '/apps?id=' + row['_id']['$oid'])
          .then(response => {
            this.api_response = response.data.status
            alert(this.api_response)
          })
          .catch(e => {
            this.errors.push(e)
          })
        location.reload()
      }
    }
  }

</script>
<style>

</style>
