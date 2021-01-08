<template>
  <v-app>
    <span class="bg" :class="{'contest-bg': contestPage, 'selection-bg': selectionPage}"></span>
    <dashboard-core-app-bar :key="key" v-model="expandOnHover" />

    <dashboard-core-view />

    <snackbar />
    <login-view  />
    <register-view />
    <v-overlay :value="overlay" :opacity=".7" absolute></v-overlay>

  </v-app>
</template>

<script>
  import { mapGetters } from 'vuex'
  
  export default {
    name: 'DashboardIndex',

    components: {
      DashboardCoreAppBar: () => import('./components/core/AppBar'),
      DashboardCoreView: () => import('./components/core/View'),
      LoginView: () => import('../pages/Login'),
      RegisterView: () => import('../pages/Register'),
      Snackbar: () => import('./component/Snackbar'),
    },

    data: () => ({
      expandOnHover: false,
      key: 0,
    }),

    computed: {
      overlay () {
        return this.$store.getters['auth/launchLogin'] || this.$store.getters['signup/launchRegister']
      },
      contestPage () {
        return this.$route.name == 'Contest'
      },
      selectionPage () {
        return this.$route.name == 'Dashboard'
      }
    },

    mounted() {
      // login
      this.$store.subscribe((mutation, state) => {
        this.key++
      })
    },
  }
</script>

<style type="text/css">
  tbody tr:nth-of-type(odd) {
    background-color: rgba(0, 0, 0, .05);
  }
  .highcharts-credits {
    display: none;
  }

  tr.v-data-table__mobile-table-row:nth-of-type(odd) td.v-data-table__mobile-row{
    background: rgba(0, 0, 0, .05);
  }

  .theme--light.v-data-table thead tr:last-child th {
    /*background: #64B5F6;*/
    font-weight: 500 !important;
  }

  .bg-dead {
    background: #E0E0E;
  }

  .min-50 {
    min-height: 50px;
  }

  .max-height-300 {
    max-height: 300px;
  }

  .max-width-300 {
    max-width: 300px;
  }

  .bg {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    background-size: cover;
  }

  .contest-bg {
    background: url( '../../assets/contest.jpeg') no-repeat center center;
  }

  .selection-bg {
    background: url( '../../assets/selection.jpeg') no-repeat center center;
  }

  .fixed-card {
    padding: .5rem 0;
    position: fixed;
    right: 10px;
  }
</style>
