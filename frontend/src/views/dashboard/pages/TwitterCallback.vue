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
    <v-overlay :value="true" :opacity=".7" absolute></v-overlay>
  </v-container>
</template>
<script>
  import auth from '@/api/auth'
  import { BASE_API } from '@/api'

  export default {
    name: 'Callback',

    mounted() {
      this.parseUrl()
    },

    methods: {
      parseUrl() {
        if (this.$route.query.denied) {
          this.$router.push({name: 'Selection'})
        } else {
          this.$store.dispatch('auth/twitterCallback', this.$route.query)
        }
      }
    }
  }
</script>