<template>
  <v-snackbar v-model="snackDlg" :timeout="timeout" :color="status">
    {{ message }}
    <template v-slot:action="{ attrs }">
      <v-btn
        v-if="refresh"
        dark
        text
        small
        v-bind="attrs"
        @click="refreshPage"
      >
        Refresh
      </v-btn>
      <v-btn
        dark
        text
        small
        v-bind="attrs"
        @click="snackDlg = false"
      >
        Close
      </v-btn>
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
      timeout () {
        return this.refresh ? -1 : 5000
      },
      message () {
        return this.$store.getters['snackbar/message']
      },
      status () {
        return this.$store.getters['snackbar/status']
      },
      refresh () {
        return this.$store.getters['snackbar/refresh']
      }
    },

    watch: {
      refresh(val) {
        if (val) {
          const self = this
          setTimeout(() => self.refreshPage(), 3000)
        }
      }
    },

    methods: {
      refreshPage () {
        this.snackDlg = false
        this.$emit('update')
      }
    }
  }
</script>