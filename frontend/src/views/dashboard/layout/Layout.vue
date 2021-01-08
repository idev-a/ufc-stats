<template>
  <v-app>
    <span class="bg"></span>
    <dashboard-core-view />
  </v-app>
</template>

<script>
  export default {
    name: 'DashboardIndex',

    components: {
      DashboardCoreView: () => import('../components/core/View'),
    },
  }
</script>

<style type="text/css">
  .bg {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    background: url( '../../../assets/contest.jpeg') no-repeat center center;
    background-size: cover;
    transform: scale(1.1);
  }
</style>
