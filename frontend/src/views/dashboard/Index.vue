<template>
  <v-app>
    <span class="bg" :class="{'contest-bg': contestPage, 'selection-bg': selectionPage, 'contest-over-bg': contestOverPage}"></span>
    <dashboard-core-app-bar :key="`key${key}`" v-model="expandOnHover" />

    <dashboard-core-drawer v-if="$vuetify.breakpoint.mobile" :expand-on-hover.sync="expandOnHover" />

    <dashboard-core-view :key="`newKey${newKey}`"/>

    <snackbar @update="reloadPage"/>
    <login-view @update="reloadPage"/>
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
      DashboardCoreDrawer: () => import('./components/core/Drawer'),
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
        return this.$route.name == 'Selection'
      }
    },

    mounted() {
      // login
      // this.$store.subscribe((mutation, state) => {
      // })
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

  .y-scroll {
    overflow-x: hidden;
    overflow-y: scroll;
    -webkit-overflow-scrolling: touch;
  }

  .w-100 {
    width: 100%;
  }

  .w-60 {
    width: 60%;
  }

  .w-50 {
    width: 50%;
  }

  .bg-dead {
    background: #E0E0E;
  }

  .bg {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    background-size: cover;
    background-image: url( 'https://ik.imagekit.io/cuhwrvztecz/selection_y1o6t0Jv-PF2p.jpeg');
  }

  .contest-bg {
    background-image: url( 'https://ik.imagekit.io/cuhwrvztecz/contest_e3BTQfvtQ58x.jpeg');
  }

  .selection-bg {
    background-image: url( 'https://ik.imagekit.io/cuhwrvztecz/selection_y1o6t0Jv-PF2p.jpeg');
  }

  .contest-over-bg {
    background-image: url( 'https://ik.imagekit.io/cuhwrvztecz/contest-over__hEVgOYfN.jpeg');
  }

  .fixed-card {
    padding: .5rem 0;
    position: fixed;
    right: 10px;
  }

  .fq-popup {
    background-image: url('https://ik.imagekit.io/cuhwrvztecz/bg_A4TO7AM8_E43.jpg');
    background-size: cover;
    background-attachment: fixed;
    background-blend-mode: multiply;
  }

  .dialog-drag {
    /*background-color: transparent;*/
    border: none;
  }

  .dialog-drag .dialog-header {
    background-color: #969494;
    background-image: url('https://ik.imagekit.io/cuhwrvztecz/bg-pattern_SBQUjHQZs.png');
    background-repeat: repeat-x;
  }

  .dialog-drag .dialog-body {
    padding: 0;
  }

  .dialog-drag.fixed {
    border-style: none;
  }

  .v-card--reveal {
    bottom: 0;
    opacity: 1 !important;
    position: absolute;
    width: 100%;
  }

  .stats-title {
    margin: .2rem 0 .5rem;
    font-size: 14px;
    text-transform: uppercase;
    font-weight: 700;
  }

  .theme--dark.v-tabs-items {
    background: none;
  }

  .v-slide-group__next, .v-slide-group__prev {
    display: none !important;
  }

  .instruction-list {
    list-style: none;
    font-weight: 300;
    letter-spacing: 0;
  }


  * {
    scrollbar-width: thin;
    scrollbar-color: rgba(0,0,0,.7) rgba(0,0,0,0.5);
  }

  ::-webkit-scrollbar {
    -webkit-appearance: none;
    width: 8px;
    height: 8px;
  }
   
  ::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3); 
    border-radius: 4px;
  }
   
  ::-webkit-scrollbar-thumb {
    border-radius: 4px;
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,1); 
  }

  ::-webkit-scrollbar-thumb:vertical
  {
    background:black url('https://ik.imagekit.io/cuhwrvztecz/bg-pattern_SBQUjHQZs.png');
  }

  ::-webkit-scrollbar-thumb:horizontal
  {
    background:black url('https://ik.imagekit.io/cuhwrvztecz/bg-pattern_SBQUjHQZs.png');
  }
</style>


<style lang="scss">
  .top-btn {
    padding: 10px 10px !important; margin: 0 1px;
  }
  .fq-btn {
    background: transparent;

    &:hover {
      box-shadow: 0 2px 15px #8df094;
    }
    &:active {
      //border: 1px solid #5BBD74;
    }
  }
  .fq-btn-active {
    color: #8df094 !important;
  }
  .fq-menu-item {
    &:hover, &:active {
      color: #8df094 !important;
    }

  }
  #contest-table {
    backdrop-filter: blur(30px) contrast(1.0);

    .v-data-table { 
      overflow-x: auto !important;
      background: none;

      tr:hover {
        background: url('https://ik.imagekit.io/cuhwrvztecz/bg_A4TO7AM8_E43.jpg');
        background-size: cover;
        background-attachment: fixed;
        backdrop-filter: blur(40px);
      }

      thead > tr > th {
        background-color: #808080db;
        backdrop-filter: blur(40px);
      }
    }

    table { border-collapse: collapse; empty-cells: show; }

    td { position: relative; }

    tr.strike-through td {
      background-color: #B71C1C;
      opacity: 0.9;
      color: #EEEEEE;
      
      &:first-child {
        border-top-left-radius: 6px;
        border-bottom-left-radius: 6px;
      }
      
      &:last-child {
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
      }
    }
    .v-application .survivor-header {
      text-align: center !important;
    }
  }
  .v-chip__content {
    font-size: 12px;
    font-weight: 400;
  }

  .max-60 {
    max-width: 800px;
  }

  .max-600 {
    max-width: 600px;
  }
</style>