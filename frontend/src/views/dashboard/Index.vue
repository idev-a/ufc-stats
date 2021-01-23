<template>
  <v-app>
    <span class="bg" :class="{'contest-bg': contestPage, 'selection-bg': selectionPage, 'contest-over-bg': contestOverPage}"></span>
    <dashboard-core-app-bar :key="`key${key}`" v-model="expandOnHover" />

    <dashboard-core-view :key="`newKey${newKey}`"/>

    <snackbar @update="reloadPage"/>
    <login-view  />
    <register-view />
    <v-overlay :value="overlay" :opacity=".7" absolute></v-overlay>

  </v-app>
</template>

<script>
  import { mapGetters, mapState } from 'vuex'
  
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
      newKey: 0,
    }),

    computed: {
      ...mapState(['event']),
      overlay () {
        return this.$store.getters['auth/launchLogin'] || this.$store.getters['signup/launchRegister']
      },
      contestPage () {
        return this.$route.name == 'Contest' && this.event.action != 'completed'
      },
      contestOverPage () {
        return this.$route.name == 'Contest' && this.event.action == 'completed'
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

    methods: {
      reloadPage () {
        this.key++
        this.newKey++
      }
    }
  }
</script>

<style src='vue-dialog-drag/dist/vue-dialog-drag.css'></style>
<style src="vue-dialog-drag/dist/dialog-styles.css"></style>

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

  @media only screen and (max-width: 600px) {
    .v-data-table > .v-data-table__wrapper > table > tbody > tr > td, .v-data-table > .v-data-table__wrapper > table > tbody > tr > th, .v-data-table > .v-data-table__wrapper > table > thead > tr > td, .v-data-table > .v-data-table__wrapper > table > thead > tr > th, .v-data-table > .v-data-table__wrapper > table > tfoot > tr > td, .v-data-table > .v-data-table__wrapper > table > tfoot > tr > th {
      padding: 0 2px !important;
    }
  }

  .bg-dead {
    background: #E0E0E;
  }

  .dialog-drag {
    background-color: transparent;
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
    background-image: url( '../../assets/contest.jpeg');
  }

  .selection-bg {
    background-image: url( '../../assets/selection.jpeg');
  }

  .contest-over-bg {
    background-image: url( '../../assets/contest-over.jpeg');
  }

  .fixed-card {
    padding: .5rem 0;
    position: fixed;
    right: 10px;
  }

  .dialog-drag {
    border: none;
  }

  .dialog-drag .dialog-header {
    background-color: #969494;
  }

  .dialog-drag .dialog-body {
    padding: 0;
  }

  .dialog-drag.fixed {
    border-style: none;
  }
</style>
