<template>
  <v-main>
    <router-view :key="$route.fullPath"/>
  </v-main>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    name: 'DashboardCoreView',

    components: {
      DashboardCoreFooter: () => import('./Footer'),
    },

    computed: {
      ...mapState(['snackbar', 'snackMsg', 'snackColor'])
    }
  }
</script>
