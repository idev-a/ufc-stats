<template>
  <v-content>
    <router-view />
  </v-content>
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
