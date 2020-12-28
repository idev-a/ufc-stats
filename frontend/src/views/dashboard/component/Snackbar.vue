<template>
  <v-snackbar v-model="snackDlg" :timeout="5000" :color="status">
    {{ message }}
    <template v-slot:action="{ attrs }">
     <!--  <v-btn
        dark
        text
        v-bind="attrs"
        @click="snackDlg = false"
      >
        Close
      </v-btn> -->
    </template>
  </v-snackbar>
</template>

<script>
  export default {
    name: 'Snackbar',

    computed: {
      snackDlg: {
        get () { return this.$store.getters['snackbar/snack'] },
        set (value) { 
          this.$store.commit('snackbar/showSnack', value)
        },
      },
      message () {
        return this.$store.getters['snackbar/message']
      },
      status () {
        return this.$store.getters['snackbar/status']
      }
    }
  }
</script>