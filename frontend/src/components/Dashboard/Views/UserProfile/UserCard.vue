<template>
  <card class="card-user">
    <img slot="image" src="https://ununsplash.imgix.net/photo-1431578500526-4d9613015464?fit=crop&fm=jpg&h=300&q=75&w=400" alt="..."/>
    <div class="author">
      <a href="#">
        <img class="avatar border-gray" src="static/img/wixot-profile.png" alt="..."/>

        <h4 class="title">{{userCardData.username}}<br />
          <small>User: {{userCardData.email}}</small>
        </h4>
      </a>
    </div>
    <p class="description text-center">
      {{userCardData.email}}  <br>
    </p>
    <div slot="footer" class="text-center">
      <button href="#" class="btn btn-simple"><i class="fa fa-facebook-square"></i></button>
      <button href="#" class="btn btn-simple"><i class="fa fa-twitter"></i></button>
      <button href="#" class="btn btn-simple"><i class="fa fa-google-plus-square"></i></button>
    </div>
  </card>
</template>
<script>
  import Card from 'src/components/UIComponents/Cards/Card.vue'
  export default {
    components: {
      Card
    },
    props: ['userCardData'],
    data () {
      return {
      }
    },
    methods: {
    }
  }
</script>
<style>

</style>
