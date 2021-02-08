<template>
  <v-dialog
    v-model="insideValue"
    width="600px"
  >
    <v-card
      class="fq-popup"
      icon="mdi-account-outline"
    >
      <v-card-title>
        <div class="font-weight-light card-title mt-2">
          Account Information
        </div>
      </v-card-title>
      <v-card-text 
        v-if="user"
      >
        <v-form
          ref="form"
          v-model="valid"
        >
          <v-container class="py-0">
            <v-row>
              <v-col
                cols="12"
                md="4"
              >
                <v-text-field
                  class="purple-input"
                  label="User Name"
                  v-model="user.username"
                  @keyup.enter="updateProfile"
                />
              </v-col>

              <v-col
                cols="12"
                md="4"
              >
                <v-text-field
                  class="purple-input"
                  label="Display Name"
                  v-model="user.displayname"
                  required
                  counter
                  minlength="3"
                  :rules="[rules.required, rules.min3]"
                  @keyup.enter="updateProfile"
                />
              </v-col>

              <v-col
                cols="12"
                md="4"
              >
                <v-text-field
                  label="Email Address"
                  class="purple-input"
                  v-model="user.email"
                  @keyup.enter="updateProfile"
                />
              </v-col>

              <!-- <v-col
                cols="12"
                md="6"
              >
                <v-text-field
                  label="First Name"
                  class="purple-input"
                  v-model="authUser.first_name"
                />
              </v-col>

              <v-col
                cols="12"
                md="6"
              >
                <v-text-field
                  label="Last Name"
                  class="purple-input"
                  v-model="authUser.last_name"
                />
              </v-col> -->

              <v-col
                cols="12"
                class="text-right"
              >
                <v-btn
                  color="success"
                  class="mr-0"
                  @click.stop="updateProfile"
                  :disabled="!valid || loading"
                >
                  Update
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
  import { mapState } from 'vuex'
  import auth from '@/api/auth'

  export default {
    name: "Player",

    data: () => ({
      loading: false,
      valid: true,
      user: null,
      rules: {
        required: v => {
          return !!v || 'This field is required.'
        },
        min3: v => {
          return v.length >= 3 || 'Minimum length is 3'
        }
      }
    }),

    props: ['value'],

    computed: {
      ...mapState('auth', ['authUser', 'error']),
      insideValue: {
        get() {
          return this.value
        },
        set () {
          this.$emit('update');
        }
      },
    },

    watch: {
      insideValue (val) {
        if (val) {
          this.user = {...this.authUser}
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
      async updateProfile() {
        this.$store.dispatch('auth/updateUser', this.user)
      }
    }
  }
</script>
