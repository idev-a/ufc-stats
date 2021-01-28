<template>
  <v-container
    id="contest"
    fluid
    tag="section"
    class="pa-0"
  >
    <div class="d-flex justify-center align-center" style="min-height: 100vh;">
      <v-progress-circular
        :size="100"
        :width="7"
        color="purple"
        indeterminate
      ></v-progress-circular>
    </div>
  </v-container>
</template>
<script>
  import auth from '@/api/auth'
  import { BASE_API } from '@/api'

  export default {
    name: 'ReferralCallback',

    mounted() {
      this.$store.dispatch('signup/referralCallback', this.$route.params)
    },
  }
</script>