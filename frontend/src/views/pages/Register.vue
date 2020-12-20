<template>
  <v-container
    id="register"
    class="fill-height justify-center"
    tag="section"
  >
    <v-snackbar v-model="snackbar.snack" :timeout="5000" :color="snackbar.status">
      {{ snackbar.message }}
      <template v-slot:action="{ attrs }">
        <v-btn
          dark
          text
          v-bind="attrs"
          @click="snackbar.snack = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
    <v-row justify="center">
      <v-slide-y-transition appear>
        <base-material-card
          color="light-blue accent-3"
          light
          max-width="100%"
          width="400"
          class="px-5 py-3"
        >
          <template v-slot:heading>
            <div class="text-center">
              <div class="display-2 font-weight-bold">
                Register to UFC Survivor
              </div>
            </div>
          </template>

          <div
            class="text-center"
          >
            <v-form
              ref="form"
              v-model="valid"
              lazy-validation
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
                counter 
                @click:prepend="show1 = !show1" />

              <v-btn
                :loading="registrationLoading"
                color="primary"
                class="display-1"
                :diabled="!valid || registrationLoading"
                @click="submit"
              >
                Submit
              </v-btn>
              <div class="text-center grey--text mt-2 body-1 font-weight-light">
                If you already have an account, please <a href="javascript:;" @click="gotoLogin">login</a>
              </div>
            </v-form>
          </div>
        </base-material-card>
      </v-slide-y-transition>
    </v-row>
  </v-container>
</template>

<script>
  import { mapActions, mapState } from 'vuex';

  export default {
    name: 'PagesRegister',

    data () {
      const defaultForm = Object.freeze({
        username: '',
        email: '',
        password1: '',
        password2: ''
      })

      return {
        loading: false,
        valid: true,
        errorMessages: {
          username: '',
          email: {
            required: false,
            invalid: false,
            business: false
          },
          password: ''
        },
        timeout: 10000,
        multiLine: true,
        snackbar: {
          snack: false,
          message: '',
          status: 'success',
        },
        terms: false,
        defaultForm,
        form: Object.assign({}, defaultForm),
        show1: false,
        rules: {
          required: value => !!value || "Required.",
          min: v => (v && v.length >= 8) || "Min 8 characters",
          counter: value => value.length >= 6 || 'Min 6 characters',
          email: value => {
            const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            this.errorMessages.email.invalid = pattern.test(value)
            return this.errorMessages.email.invalid || 'Invalid e-mail.'
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
      formHasErrors () {
        return  !this.errorMessages.email.required || !this.errorMessages.email.invalid
      },
      passwordMatch() {
        return () => this.form.password1 === this.form.password2 || "Password must match";
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
        }
      }
    },
    methods: {
      gotoLogin () {
        this.$router.push({ name: "Login" });
      },
      resetForm () {
        this.form = Object.assign({}, this.defaultForm)
        this.$refs.form.reset()
        this.formHasErrors = false
      },
      async submit () {
        this.$refs.form.validate(true)
        
        if (this.valid) {
          this.form.username = this.form.email
          this.$store.dispatch('signup/createAccount', this.form)          
        }
      },
    },
  }
</script>

<style lang="sass">
  #register
    .v-list-item__subtitle
      -webkic-line-clamp: initial
      -webkit-box-orient: initial
</style>
