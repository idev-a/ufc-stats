<template>
  <div 
    id="selection"
    :style="`height: ${height}`" 
  >
    <v-card
      :loading="loading"
      class="lighten-4 ma-0 pa-0 selection-card fq-popup"
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
          <div class="grab overline">{{totalFighters}} FIGHTERS ( <b style="color:#fffd">SQUAD SIZE: {{squadSize}}</b> )</div>
        </div>
      </v-card-title>
      <v-card-text
        class="pb-0"
        style="position: relative;"
      >
        <v-icon v-if="_down" class="arrow-down" color="red">mdi-arrow-down-drop-circle-outline</v-icon>
        <div
          id="scrollContainer"
          style="height: 300px; overflow-y: scroll; -webkit-overflow-scrolling: touch; -webkit-overflow-scrolling: scroll; position: relative;"
          @scroll="onScroll"
        >
          <template v-for="item in bouts">
            <v-btn-toggle
              v-model="contests[item.id]"
              :key="item.id"
              dense
              multiple
              class="justify-space-between mb-2 mx-1"
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
        </div>
        <v-icon v-if="_up" class="arrow-up" color="red">mdi-arrow-up-drop-circle-outline</v-icon>
        <div class="d-flex justify-center">
          <v-btn class="success my-2 mr-2" :disabled="submitDisabled" small @click="submit">Submit</v-btn>
          <v-btn class="grey darken-2 my-2" :disabled="!squadSize || eventStarted" small @click="clearSelection"><v-icon small left>mdi-cancel</v-icon>Clear</v-btn>
        </div>
      </v-card-text>
    </v-card>

    <instruction-body v-if="needsInstruction" />
  </div>
</template>

<script>
  let ROOT_PATH = 'http://localhost:8085'
  import main from '@/api/main'
  import { beautifyDate } from '@/util'
  import { mapState, mapGetters } from 'vuex'
  import FlipCountdown from "./Countdown";
  import InstructionBody from "../instruction/InstructionBody";

  const fmt = "YYYY-MM-DD HH:mm:ss";
  export default {
    name: 'Selection',

    components: {
      FlipCountdown,
      InstructionBody
    },

    watch: {
      event: {
        handler(val) {
          if (val) {
            this.startCountDown(val)
          }
        },
        deep: true
      },
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
        cntdownInstance: null,
        top: 0,
        sHeight: -1,
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
      },
      needsInstruction () {
        return this.$vuetify.breakpoint.smAndDown
      },
      height () {
        return this.$vuetify.breakpoint.smAndDown ? 'calc(100vh + 210px)' : 'inherit'
      },
      _up() {
        return this.top > 0 
              && this.$vuetify.breakpoint.mobile
      },
      _down() {
        return (this.top == 0 || (this.top + 300) < this.sHeight) && 
              this.$vuetify.breakpoint.mobile
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
      onScroll ({ target: { scrollTop, clientHeight, scrollHeight }}) {
        this.top = scrollTop
        this.sHeight = scrollHeight
        if (scrollTop + clientHeight >= scrollHeight) {
        }
      },
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
    
  //  .selection-card, .selection-card * {
  //    background-color: transparent;
  //    backdrop-filter: blur(30px) contrast(.9);
  //  }

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

    .arrow-up {
      position: absolute;
      bottom: 44px;
      left: calc(50% - 17px);
      z-index: 10;
    }

    .arrow-down {
      position: absolute;
      top: 0;
      left: calc(50% - 11px);
      z-index: 10;
    }
  }
</style>
