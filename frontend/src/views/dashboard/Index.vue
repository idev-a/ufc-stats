<template>
  <v-app>
    <span class="bg"></span>
    <!-- <v-img
      :src="require('@/assets/register.jpg')" 
      :lazy-src="require('@/assets/register.jpg')" 
    > 
    </v-img> -->
    <dashboard-core-app-bar :key="key" v-model="expandOnHover" />

    <!-- <dashboard-core-drawer :expand-on-hover.sync="expandOnHover" /> -->

    <dashboard-core-view />

    <!-- <dashboard-core-settings v-model="expandOnHover" /> -->
    <login-view  />
    <register-view />
    <v-overlay :value="overlay" :opacity=".7" absolute></v-overlay>

  </v-app>
</template>

<script>
  import { BASE_API } from '../../api'
  import axios from 'axios'
  import { mapGetters } from 'vuex'
  
  export default {
    name: 'DashboardIndex',

    components: {
      DashboardCoreAppBar: () => import('./components/core/AppBar'),
      DashboardCoreDrawer: () => import('./components/core/Drawer'),
      DashboardCoreSettings: () => import('./components/core/Settings'),
      DashboardCoreView: () => import('./components/core/View'),
      LoginView: () => import('../pages/Login'),
      RegisterView: () => import('../pages/Register')
    },

    data: () => ({
      expandOnHover: false,
      key: 0,
      loginDlg: false,
      registerDlg: false
    }),

    computed: {
      overlay () {
        return this.$store.getters['auth/launchLogin'] || this.$store.getters['signup/launchRegister']
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
    background: url( '../../assets/bg.jpg') no-repeat center center;
    background-size: cover;
    transform: scale(1.1);
  }
</style>
