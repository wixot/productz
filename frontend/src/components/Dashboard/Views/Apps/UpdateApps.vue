<template>
  <card>
    <form @submit.prevent="validateBeforeSubmit">
    <div class="column is-12">
        <label class="label">Name</label>
        <p class="control has-icon has-icon-right">
            <input name="name" v-model="rowData.name"  v-validate="{ required: true, regex: /^[a-z0-9_-]{3,15}$/ }" :class="{'input': true, 'is-danger': errors.has('email') }" type="text" placeholder="Name">
            <i v-show="errors.has('name')" class="fa fa-warning"></i>
            <span v-show="errors.has('name')" class="help is-danger">{{ errors.first('name') }}</span>
        </p>
    </div>
    <div class="column is-12">
        <label class="label">Label</label>
        <p class="control has-icon has-icon-right">
            <input name="label" v-model="rowData.label" v-validate="'required|alpha'" :class="{'input': true, 'is-danger': errors.has('name') }" type="text" placeholder="Label">
            <i v-show="errors.has('label')" class="fa fa-warning"></i>
            <span v-show="errors.has('label')" class="help is-danger">{{ errors.first('label') }}</span>
        </p>
    </div>

        <div class="form-group">
                Google Api Key:
                <div>
                <textarea  rows="4" id="googleApiKey" v-model="rowData.google_key"></textarea>
                </div>
            </div>

    <div class="column is-12">
        <p class="control">
            <button class="btn btn-info btn-fill float-right"  type="submit">Submit</button>
        </p>
    </div>
</form>
  </card>
</template>

<script>
  import Card from 'src/components/UIComponents/Cards/Card.vue'
  import axios from 'axios'

  export default {
    components: {
      Card
    },
    props: ['rowData'],
    data () {
      return {
      }
    },
    methods: {
      updateApps (currentData) {
        axios.patch(this.$apiLink + '/apps', {
          body: (currentData)
        })
          .then(response => {
            this.api_response = response.data.status
            alert(this.api_response)
          })
          .catch(e => {
            this.errors.push(e)
          })
        location.reload()
      },
        validateBeforeSubmit() {
            this.$validator.validateAll().then((result) => {
                if (result) {
                    this.updateApps(this.rowData)
                }
                else {alert('Correct them errors!'); }
            });
        }
    }
  }

</script>
<style>

</style>
