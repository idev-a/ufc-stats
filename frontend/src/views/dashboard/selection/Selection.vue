<template>
  <div id="selection">
    <v-card
      :loading="loading"
      class="lighten-4 ma-0 pa-0"
    >
      <v-card-title 
        v-if="event" 
        class="popup-header grab text-center ustify-center font-weight-medium mb-md-3"
      >
        <div style="width: 100%">
          <div class="grab">{{ this.event.name }}</div>
          <div class="grab subtitle-2">
            <span>{{ this.event.date | beautifyDate }}</span>
            <span v-if="eventStarted" class="red--text lighten-1 h6">({{(event.action || 'started').toUpperCase()}})</span>
            <flip-countdown @stopTimer="disableSelection" v-if="countable" :deadline="deadline2"></flip-countdown>
          </div>
          <div class="grab overline">{{totalFighters}} FIGHTERS</div>
          <div class="grab overline">SQUAD SIZE: <b>{{squadSize}}</b></div>
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
                :disabled="eventStarted"
                small
                :width="152"
              >
                {{_fighter(item.fighter1).name}}
              </v-btn>

              <v-btn
                :value="item.fighter2"
                :disabled="eventStarted"
                small
                :width="152"
              >
                {{_fighter(item.fighter2).name}}
              </v-btn>
            </v-btn-toggle>
          </template>
        </v-virtual-scroll>
        <div class="d-flex justify-center">
          <v-btn class="success mt-2 mb-2 mr-2" :disabled="submitDisabled" small @click="submit">Submit</v-btn>
          <v-btn class="grey darken-2 mt-2 mb-2" :disabled="!squadSize || eventStarted" small @click="clearSelection">Clear</v-btn>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
  let ROOT_PATH = 'http://localhost:8085'
  import main from '@/api/main'
  import { beautifyDate } from '@/util'
  import { mapState, mapGetters } from 'vuex'
  import FlipCountdown from "./Countdown";

  const fmt = "YYYY-MM-DD HH:mm:ss";

  export default {
    name: 'Selection',

    components: {
      FlipCountdown
    },

    watch: {
      event: {
        handler(val) {
          if (val) {
            this.startCountDown(val)
          }
        },
        deep: true
      }
    },

    data () {
      return {
        logo: 'https://vuejs.org/images/logo.png',
        deadline2: '',
        dlg: true,
        loading: false,
        countdownEnd: false,
        bouts: [],
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
        cntdownInstance: null
      }
    },

    metaInfo() {
      return {
        title: 'FightQuake',
        meta: [
            // Twitter Card
            {name: 'twitter:card', content: 'summary'},
            {name: 'twitter:title', content: 'Vue Social Cards Example'},
            {name: 'twitter:description', content: 'Vue sample site showing off Twitter and Facebook Cards.'},
            // image must be an absolute path
            {name: 'twitter:image', content: this.logo},
            // Facebook OpenGraph
            // {property: 'og:title', content: 'Vue Social Cards Example'},
            // {property: 'og:site_name', content: 'Vue Example'},
            // {property: 'og:type', content: 'website'},
            // {property: 'og:image', content:  this.logo},
            // {property: 'og:locale', content:  'en_US'},
            // {property: 'og:description', content: 'Vue sample site showing off Twitter and Facebook Cards.'}
        ]
      }
    },

    computed: {
      ...mapState(['event']),
      ...mapState('auth', ['authUser']),
      ...mapGetters('auth', ['isAuthenticated']),
      submitDisabled() {
        return this.loading || !this.event || this.eventStarted || this.bouts.length < 1 || this.event.started
      },
      leftMargin () {
        return this.$vuetify.breakpoint.mobile ? 5 : 50
      },
      eventStarted () {
        return this.event && this.event.action != '' || this.countdownEnd
      },
      countable () {
        return this.deadline2 && !this.eventStarted
      },
      totalFighters () {
        return this.bouts && this.bouts.length * 2 || 0
      }
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
      startCountDown(val) {
        this.deadline2 = this.$moment(`${val.date}`).format(fmt)
      },
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
        this.$store.commit('SET_EVENT', data.event)
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
          this.$store.commit('snackbar/setSnack', this.snackbar)
          return
        }

        const { data } = await main.createEntries(payload)
        this.snackbar = {
          ...data,
          snack: true
        }
        this.$store.commit('snackbar/setSnack', this.snackbar)

        if (data.status == 'success') {
          const self = this
          setTimeout(function(){ self.$router.push('Contest'); }, 1200);
        }
      },
      clearSelection () {
        this.contests = {}
        this.squadSize = 0
      },
      changeContests() {
        this.squadSize = 0
        for (const bout in this.contests) {
          const survivors = this.contests[bout]
          this.squadSize += survivors.length
        }
      },
      disableSelection () {
        this.countdownEnd = true
      }
    }
  }
</script>

<style lang="scss">
  #selection {
    backdrop-filter: blur(30px) contrast(.9);

    * {
      background-color: transparent;
    }

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

    .v-btn.v-btn--disabled {
      color: rgba(255, 255, 255, 0.26) !important;
    }
  }
</style>
