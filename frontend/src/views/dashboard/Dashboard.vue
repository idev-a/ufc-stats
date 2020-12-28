<template>
  <v-container
    id="dashboard"
    fluid
    tag="section"
  >
    <selection />
  </v-container>
</template>

<script>
  import upperFirst from 'lodash/upperFirst'
  import { Get, Post, BASE_API } from '@/api/index'

  export default {
    name: 'DashboardDashboard',

    components: {
      Selection: () => import('./component/Selection')
    },

    data () {
      return {
        loading: false,
      }
    },

    mounted () {
    },

    computed: {
    },

    methods: {
    },
  }
</script>

<style>
</style>