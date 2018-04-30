<template>
  <div>
    <form>
      <h4 slot="header" class="card-title">User Profile</h4>
      <div class="row">
        <div class="col-md-3">
          <fg-input type="text"
                    label="Company"
                    v-model="userProfileData.details.company">
          </fg-input>
        </div>
        <div class="col-md-3">
          <fg-input type="text"
                    label="Username"
                    :disabled="true"
                    v-model="userProfileData.username">
          </fg-input>
        </div>
        <div class="col-md-3">
          <fg-input type="email"
                    label="Email"
                    :disabled="true"
                    v-model="userProfileData.email">
          </fg-input>
        </div>
      </div>

      <div class="row">
        <div class="col-md-6">
          <fg-input type="text"
                    label="First Name"
                    v-model="userProfileData.details.first_name">
          </fg-input>
        </div>
        <div class="col-md-6">
          <fg-input type="text"
                    label="Last Name"
                    v-model="userProfileData.details.last_name">
          </fg-input>
        </div>
      </div>

      <div class="row">
        <div class="col-md-4">
          <fg-input type="text"
                    label="City"
                    v-model="userProfileData.details.city">
          </fg-input>
        </div>
        <div class="col-md-4">
          <fg-input type="text"
                    label="Country"
                    v-model="userProfileData.details.country">
          </fg-input>
        </div>

         <div class="clearfix"></div>

      <div class="text-center" style="margin-left: 170px; margin-top: 33px;">
          <button type="submit" class="btn btn-info btn-fill float-right" v-on:click="updateUser(userProfileData)">
            Update Profile
          </button>
        </div>

      </div>
    </form>

    <card >
      <div class="col-md-6">
          <fg-input type="text"
                    label="User Id"
                    :disabled="true"
                    v-model="userProfileData._id.$oid">
          </fg-input>
        </div>

      <div class="row" >
      <div class="col-md-8">
          <fg-input type="text"
                    label="Api Key"
                    :disabled="true"
                    v-model="userProfileData.api_key">
          </fg-input>
        </div>

      <div class="col-md-3" style="margin-top: 12px;" >
        <div class="modal-body">
            <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#apiKeyModal">
              Renew Api Key
            </button>
        </div>
      </div>
        </div>
    </card>


      <div class="modal fade" id="apiKeyModal" tabindex="-1" role="dialog" aria-labelledby="apiKeyModal" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalLabel">Renew Api Key</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <div>
                <label>...............................................................................................</label>
              </div>

                  <label for="message-text" class="col-form-label">User Name:</label>
                  <input type="text" class="form-control" id="message-text"  v-model="controlName">

            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
              <button type="button" class="btn btn-primary" v-on:click="controlUsername(controlName)">Renew</button>
            </div>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
  import Card from 'src/components/UIComponents/Cards/Card.vue'
  export default {
    components: {
      Card
    },
    props: ['userProfileData', 'updateUser' , 'renewApiKey'],
    data () {
      return {
          controlName: ''
      }
    },
    methods: {
        controlUsername (username) {
            if (username === this.userProfileData.username) {
                this.renewApiKey(username)
                this.closeMolal()

            }
        },
        closeMolal () {
                $('#apiKeyModal').modal('hide')
            }
    }
  }
</script>