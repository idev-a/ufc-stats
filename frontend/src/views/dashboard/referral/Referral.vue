<template>
  <v-dialog 
    v-model="insideValue"
    width="600px"
    persistent
  >
    <v-card
      class="fq-popup"
    >
      <v-app-bar
        class="pt-3 mb-5"
        color="rgba(0, 0, 0, 0)"
      >
        <div class="text-center display-2 font-weight-bold">
          Refer A Friend
        </div>
        <v-spacer />
        <v-btn icon @click="insideValue=false"><v-icon>mdi-close</v-icon></v-btn>
      </v-app-bar>
      <v-card-text>
        <v-text-field
          ref="link"
          outlined
          readonly
          success
          :value="link"
          :append-icon="copyIcon"
          @click:append="copyLink"
        >
        </v-text-field>
        <input type="hidden" id="referral-code" :value="link">
        <v-card-actions class="d-flex justify-center">
          <v-tooltip
            bottom
          >
            <template v-slot:activator="{ on }">
              <v-btn 
                fab
                small
                v-on="on"
                link
                target="_blank"
                :href="tweetShareLink"
              >
                <v-icon size="24" color="twitter">mdi-twitter</v-icon>
              </v-btn>
            </template>
            Share with Twitter
          </v-tooltip>
        </v-card-actions>
      </v-card-text>
    </v-card>

<!--     <v-snackbar v-model="snack" :timeout="3000" :color="status">
      {{ message }}
      <template v-slot:action="{ attrs }">
        <v-btn
          dark
          text
          v-bind="attrs"
          @click="snack = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar> -->
  </v-dialog>
</template>
<script>
  import { BASE_API } from '@/api'
  export default {
    name: "Referral",

    props: ['value'],

    computed: {
      insideValue: {
        get() {
          return this.value
        },
        set () {
          this.$emit('update');
        }
      },
      copyIcon() {
        return this.copy ? 'mdi-content-paste' : 'mdi-content-copy'
      },
      link() {
        const id = this.$store.getters['auth/authUser']?.pk || this.$store.getters['auth/authUser']?.id
        return `${process.env.VUE_APP_URL}/rf/${id}`
      },
      tweetShareLink () {
        return encodeURI(`https://twitter.com/intent/tweet?url=${this.link}&via=fightquake&text=Join me on FIGHTQUAKE to play fantasy MMA!&hashtags=ufc,fightquake,survival`)
      }
    },

    data: () => ({
      copy: false,
      snackbar: {
        message: 'Copied',
        status: 'warning',
        snack: true,
      }
    }),

    methods: {
      copyLink() {
        this.copy = true
        let testingCodeToCopy = document.querySelector('#referral-code')
        testingCodeToCopy.setAttribute('type', 'text')
        testingCodeToCopy.select()

        try {
          var successful = document.execCommand('copy');
          this.snackbar.message = successful ? 'Copied' : 'Cannot copy';
          this.snackbar.status = successful ? 'success' : 'warning';
        } catch (err) {
          this.snackbar.message = 'Oops, unable to copy';
        }

        /* unselect the range */
        testingCodeToCopy.setAttribute('type', 'hidden')
        window.getSelection().removeAllRanges()
        const self = this
        setTimeout(() => self.copy = false, 1000)
        this.$store.commit('snackbar/setSnack', this.snackbar)
      }
    }
  }
</script>