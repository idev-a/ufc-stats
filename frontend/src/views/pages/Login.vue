<template>
  <v-dialog
    v-model="propDlg"
    fullscreen
  >
    <v-row justify="center" align="center" style="min-height: 100vh;">
      <v-slide-y-transition appear>
        <v-card
          light
          max-width="100%"
          width="400"
          class="px-auto py-5"
        >
          <v-app-bar
            flat
            color="rgba(0, 0, 0, 0)"
          >
            <div class="text-center display-2 font-weight-bold">
              Login
            </div>
            <v-spacer />
            <v-btn icon @click="propDlg=false"><v-icon>mdi-close</v-icon></v-btn>
          </v-app-bar>

          <v-card-text
            class="text-center"
          >
            <v-btn 
              block
              color="#1DA1F2"
              class="mb-5"
              :loading="authenticating"
              @click="twitterLogin()"
            >
              Login with Twitter
              <v-icon right>mdi-twitter</v-icon>
            </v-btn>
            <div class="my-2">Or</div>
            <v-btn
              block
              color="teal accent-4"
              @click="reveal = true"
            >
              Login with Email
            </v-btn>
          </v-card-text>
          <div class="text-center mt-2 grey--text body-1 font-weight-light">
            If you don't have any account, please <a href="javascript:;" @click="gotoSignup" class="">sign up</a>
          </div>

          <v-expand-transition>
            <v-card
              tile
              v-if="reveal"
              class="transition-fast-in-fast-out v-card--reveal"
              style="height: calc(100%); top:70px"
            >
              <v-card-text class="pb-0">
                <v-form
                  ref="form"
                  v-model="valid"
                >
                  <v-text-field
                    ref="email"
                    v-model="form.email"
                    :rules="[rules.required, rules.email]"
                    :loading="authenticating"
                    hide-details="auto"
                    class="mb-5"
                    color="secondary"
                    label="Email address"
                    prepend-icon="mdi-email"
                    @keyup.enter="submit"
                    required
                  />

                  <v-text-field
                    ref="password"
                    type="password"
                    v-model="form.password"
                    :rules="[rules.required]"
                    :loading="authenticating"
                    hide-details="auto"
                    class="mb-7"
                    color="secondary"
                    label="Password"
                    prepend-icon="mdi-key"
                    @keyup.enter="submit"
                    required
                  />

                  <v-btn
                    class="mt-5"
                    color="primary"
                    :loading="authenticating"
                    @click="submit"
                    block
                  >
                    Submit
                  </v-btn>
                  <v-btn
                    class="mt-5"
                    color="teal accent-4"
                    @click="reveal = false"
                    block
                  >
                    Close
                  </v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </v-expand-transition>
        </v-card>
      </v-slide-y-transition>
    </v-row>
  </v-dialog>
</template>

<script>
  import auth from '@/api/auth'
  import axios from 'axios'
  import { mapState, mapGetters } from 'vuex'

  export default {
    name: 'PagesLogin',

    components: {
    },

    props: ['value'],

    data () {
      const defaultForm = Object.freeze({
        email: '',
        password: '',
        displayname: ''
      })

      return {
        reveal: false,
        valid: true,
        loading: false,
        snackbar: {
          snack: false,
          message: '',
          status: 'success',
        },
        defaultForm,
        form: Object.assign({}, defaultForm),
        rules: {
          required: value => {
            return !!value || 'This field is required.'
          },
          counter: value => value.length >= 6 || 'Min 6 characters',
          email: value => {
            const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            return pattern.test(value)|| 'Invalid e-mail.'
          },
        },
        socials: [
          {
            href: '#',
            icon: 'mdi-google',
          },
        ],
      }
    },

    computed: {
      ...mapState('auth', ['authenticating', 'error']),
      ...mapGetters('auth', ['isAuthenticated']),
      propDlg: {
        get () { return this.$store.getters['auth/launchLogin'] },
        set (value) { 
          this.reveal = false
          this.$store.commit('auth/showLoginDlg', value)
        },
      },
    },

    watch: {
      authenticating (val) {
        if (!val && !this.error && this.$route.name != 'Selection') {
          this.$router.push({name: 'Selection'})
        }
      },
      error (val) {
        if (val) {
          const snackbar = {
            message: val,
            status: 'failed',
            snack: true
          }
          this.$store.dispatch('snackbar/setSnack', snackbar)
        }
      }
    },

    methods: {
      gotoSignup () {
        this.$store.commit('auth/showLoginDlg', false)
        this.$store.commit('signup/showRegisterDlg')
      },
      gotoDashboard (user) {
        localStorage.setItem('jwt', 'success')
        localStorage.setItem('user', JSON.stringify(user))
        this.$store.commit('signup/showRegisterDlg', false)
      },
      submit () {
        this.$refs.form.validate()

        if (this.valid) {
          this.form.username = this.form.email
          this.$store.dispatch('auth/login', this.form)
        }
      },
      twitterLogin() {
        this.$store.dispatch('auth/twitterLogin')
      }
    },
  }
</script>

