<template>
  <v-dialog
    v-model="insideValue"
    width="600px"
  >
    <v-card icon="mdi-account-outline">
      <v-card-title>
        <div class="font-weight-light card-title mt-2">
          User Profile
        </div>
      </v-card-title>
      <v-card-text>
        <v-form>
          <v-container class="py-0">
            <v-row>
              <v-col
                cols="12"
                md="4"
              >
                <v-text-field
                  class="purple-input"
                  label="User Name"
                  disabled
                  v-model="authUser.username"
                />
              </v-col>

              <v-col
                cols="12"
                md="4"
              >
                <v-text-field
                  class="purple-input"
                  label="Display Name"
                  v-model="authUser.displayname"
                />
              </v-col>

              <v-col
                cols="12"
                md="4"
              >
                <v-text-field
                  label="Email Address"
                  class="purple-input"
                  v-model="authUser.email"
                  disabled
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
    name: "UserProfile",

    data: () => ({
      loading: false,
    }),

    props: ['value'],

    computed: {
      ...mapState('auth', ['authUser']),
      insideValue: {
        get() {
          return this.value
        },
        set () {
          this.$emit('update');
        }
      }
    },

    methods: {
      async updateProfile() {
        this.$store.dispatch('auth/updateUser', this.authUser)
      }
    }
  }
</script>
