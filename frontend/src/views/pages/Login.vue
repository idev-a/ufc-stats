<template>
  <v-dialog
    v-model="propDlg"
    fullscreen
  >
    <v-snackbar
      v-model="snackbar"
      absolute
      top
      center
      :color="snackbar_color"
      :multi-line="multiLine"
    >
      <span>{{ snackbar_message }}</span>
      <v-icon
        dark
      >
        mdi-checkbox-marked-circle
      </v-icon>
    </v-snackbar>
    <v-row justify="center" align="center" style="min-height: 100vh;">
      <v-slide-y-transition appear>
        <v-card
          light
          max-width="100%"
          width="400"
          class="px-5 py-5"
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
                label="Email address."
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
                label="Password."
                prepend-icon="mdi-key"
                @keyup.enter="submit"
                required
              />

              <v-btn
                class="ma-1 mt-1"
                color="primary"
                :loading="authenticating"
                @click="submit"
              >
                Login
              </v-btn>
              <div class="text-center mt-2 grey--text body-1 font-weight-light">
                If you don't have any account, please <a href="javascript:;" @click="gotoSignup" class="">sign up</a>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-slide-y-transition>
    </v-row>
  </v-dialog>
</template>

<script>
  import { BASE_API } from '../../api'
  import { DOMAIN_LIST } from '../../util'
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
        password: ''
      })

      return {
        valid: true,
        loading: false,
        formHasErrors: false,
        errorMessages: {
          email: {
            required: false,
            invalid: false,
            business: false
          },
        },
        snackbar: false,
        snackbar_message: '',
        snackbar_color: 'success',
        multiLine: true,
        defaultForm,
        form: Object.assign({}, defaultForm),
        code: '',
        keepMeLogin: false,
        rules: {
          required: value => {
            this.errorMessages.email.required = !!value
            return this.errorMessages.email.required || 'This field is required.'
          },
          counter: value => value.length >= 6 || 'Min 6 characters',
          email: value => {
            const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            this.errorMessages.email.invalid = pattern.test(value)
            return this.errorMessages.email.invalid || 'Invalid e-mail.'
          },
          validEmail: value => {
            const domain = value.split('@')[1]
            this.errorMessages.email.business = value.includes('@') && !DOMAIN_LIST.includes(domain.toLowerCase()) 
            return this.errorMessages.email.business || 'Please enter a business email'
          }
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
          this.$store.commit('auth/showLoginDlg', value)
        },
      },
    },

    watch: {
      authenticating (val) {
        if (!val && !this.error) {
          this.$router.push({name: 'Dashboard'})
        }
      },
    },

    methods: {
      gotoSignup () {
        this.$store.commit('auth/showLoginDlg', false)
        this.$store.commit('signup/showRegisterDlg')
      },
      gotoDashboard (user) {
        localStorage.setItem('jwt', 'success')
        localStorage.setItem('user', JSON.stringify(user))
        // this.$router.push({ name: "Dashboard" });
        this.$store.commit('signup/showRegisterDlg', false)
      },
      resetForm () {
        this.form = Object.assign({}, this.defaultForm)
        this.$refs.form.reset()
        this.formHasErrors = false
      },
      submit () {
        this.$refs.form.validate()

        if (this.valid) {
          const data = {
            username: this.form.email,
            password: this.form.password
          }
          this.$store.dispatch('auth/login', data)
        }
      },
    },
  }
</script>
