<template>
  <v-container
    id="contest"
    fluid
    tag="section"
    class="pa-0"
  >
    <!-- <v-btn @click="authenticate('twitter')">auth Twitter</v-btn> -->
    <v-card
      :class="{'fixed-card': $vuetify.breakpoint.smAndUp}"
      :loading="loading"
      class="grey lighten-4 mt-0 pa-0"
    >
      <v-card-title 
        class="justify-center font-weight-medium mb-md-3"
      >
        <div v-if="event" class="text-center">
          <div>{{ this.event.name }}</div>
          <div class="subtitle-2">{{ this.event.date | beautifyDate }}</div>
        </div>
      </v-card-title>
      <v-card-text
        class="pb-0"
      >
        <v-virtual-scroll
          :items="bouts"
          :item-height="50"
          height="300"
        >
          <template v-slot:default="{ item }">
            <toggle-switch v-model="contests[item.id]" :key="item.id" :options="myOptions(item)" />
          </template>
        </v-virtual-scroll>
        <div class="d-flex justify-center w-100">
          <v-btn class="grey darken-4 mt-2 mb-2" small @click="submit">Submit</v-btn>
        </div>
      </v-card-text>
    </v-card>

    <v-snackbar v-model="snackbar.snack" :timeout="3000" :color="snackbar.status">
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
  </v-container>
</template>

<script>
  import session from '@/api/session'
  import { beautifyDate } from '@/util'
  import ToggleSwitch from './ToggleSwitch.vue'
  import { mapState } from 'vuex'

  export default {
    name: 'Selection',

    components: {
      ToggleSwitch
    },

    data () {
      return {
        loading: false,
        bouts: [],
        event: null,
        fighters: [],
        selectedItem: -1,
        contests: {},
        snackbar: {
          snack: false,
          message: '',
          status: 'success'
        }
      }
    },

    watch: {
      contests: {
        handler (val) {
          // console.log(val)
        },
        deep: true
      }
    },

    computed: {
      ...mapState('auth', ['authUser']),
      bgHeight() {
        return this.$vuetify.breakpoint.height - 147
      }
    },

    filters: {
      beautifyDate,
    },

    async mounted () {
      this.loading = true
      await this.getFighters()
      await this.getLatestBouts()
      this.loading = false
    },

    methods: {
      authenticate: function (provider) {
        // if (this.$auth.isAuthenticated()) {
        //   this.$auth.logout()
        // }
        this.response = null
        var this_ = this;
        this.$auth.authenticate(provider).then(function (authResponse) {
          this_.isAuthenticated = this_.$auth.isAuthenticated();
          this_.response = authResponse.body.profile
          // Execute application logic after successful social authentication
        }).catch(function (err) {
          this_.isAuthenticated = this_.$auth.isAuthenticated()
          this_.response = err
        })
      },
      async getLatestBouts () {
        const { data } = await session.get(`api/latest_event`)
        this.bouts = data.bouts
        this.event = data.event
      },
      async getFighters () {
        const { data } = await session.get('api/fighters')
        this.fighters = data.results
      },
      _fighter (id) {
        const fighters = this.fighters.filter(fighter => fighter.id == id)
        return fighters[0]
      },
      myOptions (item) {
        const fighter1 = this._fighter(item.fighter1)
        const fighter2 = this._fighter(item.fighter2)
        return {
          items: {
            delay: .4,
            preSelected: 'unknown',
            disabled: false,
            labels: [
              {name: fighter1.name, id: fighter1.id, color: 'white', backgroundColor: 'green'}, 
              {name: fighter2.name, id: fighter2.id, color: 'white', backgroundColor: 'green'}
            ]
          }
        }
      },
      async submit () {
        const event_id = this.bouts[0].event
        const payload = []
        for (const bout in this.contests) {
          payload.push({
            event: event_id,
            user: this.authUser.pk,
            bout: bout,
            fighter: this.contests[bout]
          })
        }
        const { data } = await session.post('api/entries/', payload)
        this.snackbar = {
          ...data,
          snack: true
        }
      }
    }
  }
</script>

<style>
  .fixed-card {
    padding: .5rem 0;
    position: fixed;
    right: 10px;
  }

  .v-item--active {
    color: red;
  }
</style>