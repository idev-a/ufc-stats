<template>
  <v-dialog
    v-model="propDlg"
    fullscreen
  >
    <v-row no-gutters justify="center" align="center" style="min-height: 100vh;">
      <v-slide-y-transition appear>
        <v-card
          max-width="100%"
          width="400"
          class="px-auto py-3 fq-popup"
          :height="height"
        >
          <v-app-bar
            flat
            color="rgba(0, 0, 0, 0)"
          >
            <div class="text-center display-2 font-weight-bold">
              Register to UFC Survivor
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
              Signup with Twitter
              <v-icon right>mdi-twitter</v-icon>
            </v-btn>
            <div class="my-2">Or</div>
            <v-btn
              block
              color="teal accent-4"
              @click="reveal = true"
            >
              Signup with Email
            </v-btn>
          </v-card-text>

          <div class="text-center grey--text mt-2 body-1 font-weight-light">
            If you already have an account, please <a href="javascript:;" @click="gotoLogin">login</a>
          </div>

          <v-expand-transition>
            <v-card
              v-if="reveal"
              class="transition-fast-in-fast-out v-card--reveal fq-popup"
              style="height: 100%; top:70px;"
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
                    :loading="registrationLoading"
                    class="mt-5 mb-7"
                    hide-details="auto"
                    color="secondary"
                    label="Please enter your email address."
                    prepend-icon="mdi-email"
                    @keyup.enter="submit"
                    required
                  />

                  <v-text-field
                    ref="displayname"
                    v-model="form.displayname"
                    :rules="[rules.required]"
                    :loading="authenticating"
                    hide-details="auto"
                    class="mb-5"
                    color="secondary"
                    label="Display Name"
                    prepend-icon="mdi-account"
                    @keyup.enter="submit"
                    required
                  />
                  
                  <v-text-field 
                    v-model="form.password1" 
                    :loading="registrationLoading"
                    :prepend-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'" 
                    :rules="[rules.required, rules.min]" 
                    :type="show1 ? 'text' : 'password'" 
                    name="input-10-1" 
                    label="Password" 
                    hint="At least 8 characters"
                    counter 
                    @click:prepend="show1 = !show1" />

                  <v-text-field 
                    block 
                    v-model="form.password2" 
                    :loading="registrationLoading"
                    :prepend-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'" 
                    :rules="[rules.required, passwordMatch]" 
                    :type="show1 ? 'text' : 'password'" 
                    name="input-10-1" 
                    label="Confirm Password" 
                    @keyup.enter="submit"
                    counter 
                    @click:prepend="show1 = !show1" />

                  <v-btn
                    :loading="registrationLoading"
                    color="primary"
                    class="my-5"
                    :diabled="!valid || registrationLoading"
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
  import { mapActions, mapState } from 'vuex';

  export default {
    name: 'PagesRegister',

    props: ['value'],

    data () {
      const defaultForm = Object.freeze({
        username: '',
        displayname: '',
        email: '',
        password1: '',
        password2: ''
      })

      return {
        reveal: false,
        loading: false,
        valid: true,
        snackbar: {
          snack: false,
          message: '',
          status: 'success',
        },
        defaultForm,
        form: Object.assign({}, defaultForm),
        show1: false,
        rules: {
          required: value => !!value || "Required.",
          min: v => (v && v.length >= 8) || "Min 8 characters",
          counter: value => value.length >= 6 || 'Min 6 characters',
          email: value => {
            const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            return pattern.test(value) || 'Invalid e-mail.'
          },
        },
      }
    },

    computed: {
      ...mapState('signup', [
        'registrationCompleted',
        'registrationError',
        'registrationLoading',
      ]),
      ...mapState('auth', ['authenticating', 'error']),
      propDlg: {
        get () { return this.$store.getters['signup/launchRegister'] },
        set (value) { 
          this.reveal = false
          this.$store.commit('signup/showRegisterDlg', value) 
        },
      },
      passwordMatch() {
        return () => this.form.password1 === this.form.password2 || "Password must match";
      },
      height () {
        return this.reveal ? '470px' : '100%'
      }
    },

    watch: {
      registrationLoading(val) {
        if (!val) {
          if (this.registrationError) {
            this.snackbar.message = this.registrationError
            this.snackbar.status = 'failed'
          } else {
            this.snackbar.message = 'Successfully registered.'
            this.snackbar.status = 'success'
          }
          this.snackbar.snack = true
          
          this.$store.dispatch('snackbar/setSnack', this.snackbar)

          if (!this.registrationError) {
            const data = {
              username: this.form.username,
              password: this.form.password1
            }
            this.$store.dispatch('auth/login', data)
          }
        }
      },
      authenticating (val) {
        if (!val && !this.error) {
          this.$store.commit('auth/showLoginDlg', false)
        }
      },
      registrationCompleted (val) {
        console.log('registrationCompleted')
      }
    },
    methods: {
      gotoLogin () {
        this.$store.commit('signup/showRegisterDlg', false)
        this.$store.commit('auth/showLoginDlg')
      },
      async submit () {
        this.$refs.form.validate(true)
        if (!this.valid) {
          return
        }
        
        if (this.valid) {
          this.form.email = this.form.email.toLowerCase()
          this.form.username = this.form.email
          this.form.referred_by = this.$route.params?.id
          this.$store.dispatch('signup/createAccount', this.form)
        }
      },
      twitterLogin() {
        this.$store.dispatch('auth/twitterLogin')
      }
    },
  }
</script>

<style lang="sass">
  #register
    .v-list-item__subtitle
      -webkic-line-clamp: initial
      -webkit-box-orient: initial
</style>
