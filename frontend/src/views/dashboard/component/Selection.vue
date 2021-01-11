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
          <div class="overline">SQUAD SIZE: <b>{{squadSize}}</b></div>
        </div>
      </v-card-title>
      <v-card-text
        class="pb-0"
      >
        <v-virtual-scroll
          :items="bouts"
          :item-height="45"
          height="300"
          :key="key"
        >
          <template v-slot:default="{ item }">
            <!-- <toggle-switch v-model="contests[item.id]" :key="item.id" :options="myOptions(item)" /> -->
            <v-btn-toggle
              v-model="contests[item.id]"
              :key="item.id"
              dense
              multiple
              class="justify-space-between"
              tile
              @change="changeContests"
            >
              <v-btn
                :value="item.fighter1"
                small
                :width="112"
              >
                {{_fighter(item.fighter1).name}}
              </v-btn>

              <v-btn
                :value="item.fighter2"
                small
                :width="112"
              >
                {{_fighter(item.fighter2).name}}
              </v-btn>
            </v-btn-toggle>
          </template>
        </v-virtual-scroll>
        <div class="d-flex justify-center w-100">
          <v-btn class="grey darken-4 mt-2 mb-2" :disabled="submitDisabled" small @click="submit">Submit</v-btn>
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
  import main from '@/api/main'
  import { beautifyDate } from '@/util'
  import ToggleSwitch from './ToggleSwitch.vue'
  import { mapState, mapGetters } from 'vuex'

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
        key: 1,
        snackbar: {
          snack: false,
          message: '',
          status: 'success'
        },
        toggle_multiple: [0, 1],
        squadSize: 0,
      }
    },

    watch: {
      contests: {
        handler (val) {
          console.log(val)
        },
        deep: true
      }
    },

    computed: {
      ...mapState('auth', ['authUser']),
      ...mapGetters('auth', ['isAuthenticated']),
      bgHeight() {
        return this.$vuetify.breakpoint.height - 147
      },
      submitDisabled() {
        let selected = false
        for (const bout in this.contests) {
          const survivors = this.contests[bout]
          if (survivors.length) {
            selected = true
          }
        }
        return this.loading || !this.event || this.bouts.length < 1
      },
    },

    filters: {
      beautifyDate,
    },

    async mounted () {
      this.loading = true
      await this.getFighters()
      await this.getLatestBouts()
      this.preselectFighters()
      this.changeContests()
      this.loading = false
    },

    methods: {
      preselectFighters() {
        this.bouts.map(bout => {
          this.contests[bout.id] = []
          if (bout.survivors) {
            this.contests[bout.id] = bout.survivors
          }
        })
        this.key++
      },
      async getLatestBouts () {
        const { data } = await main.getLatestEvent()
        this.bouts = data.bouts
        this.event = data.event
      },
      async getFighters () {
        const { data } = await main.getFighters()
        this.fighters = data.results
      },
      _fighter (id) {
        const fighters = this.fighters.filter(fighter => fighter.id == id)
        return fighters[0]
      },
      // myOptions (item) {
      //   const fighter1 = this._fighter(item.fighter1)
      //   const fighter2 = this._fighter(item.fighter2)
      //   return {
      //     items: {
      //       delay: .4,
      //       preSelected: 'unknown',
      //       disabled: false,
      //       labels: [
      //         {name: fighter1.name, id: fighter1.id, color: 'white', backgroundColor: 'green'}, 
      //         {name: fighter2.name, id: fighter2.id, color: 'white', backgroundColor: 'green'}
      //       ]
      //     }
      //   }
      // },
      async submit () {
        if (!this.isAuthenticated) {
          this.$store.commit('auth/showLoginDlg')
          return
        }
        const event_id = this.bouts[0].event
        const payload = {
          entry: {
            event: event_id,
            user: this.authUser.pk || this.authUser.id,
          },
          selections: []
        }
        let selected = false
        for (const bout in this.contests) {
          const survivors = this.contests[bout]
          if (survivors.length) {
            selected = true
          }
          payload.selections.push({
            bout: bout,
            survivor1: survivors?.[0] || null,
            survivor2: survivors?.[1] || null,
          })
        }

        if (!selected) {
          this.snackbar = {
            snack: true,
            message: 'Please select at least one entry to submit',
            status: 'dark'
          }
          return
        }

        const { data } = await main.createEntries(payload)
        this.snackbar = {
          ...data,
          snack: true
        }

        if (data.status == 'success') {
          const self = this
          setTimeout(function(){ self.$router.push('Contest'); }, 1200);
        }
      },
      changeContests() {
        this.squadSize = 0
        for (const bout in this.contests) {
          const survivors = this.contests[bout]
          if (survivors.length) {
            this.squadSize++
          }
        }
      }
    }
  }
</script>

<style lang="scss">
  #contest {
    .v-btn-toggle {
      display: flex;

      .v-btn {
        border-radius: 5px;
        background-color: #d3d3d3;
        color: black;
      }
    }
   
    .v-item--active {
      color: white !important;
      background-color: #008000 !important;
    }

    .theme--light.v-btn.v-btn--disabled {
      color: rgba(255, 255, 255, 0.26) !important;
    }
  }

</style>