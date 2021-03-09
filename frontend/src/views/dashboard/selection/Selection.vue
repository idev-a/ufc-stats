<template>
  <div 
    id="selection"
    :style="`height: ${height}`" 
  >
    <v-card
      :loading="loading"
      class="lighten-4 ma-0 pa-0 selection-card fq-popup"
    >
      <v-row dense>
        <v-col cols=12 md=6 >
          <v-card-title 
            v-if="curContest" 
            class="font-weight-medium mb-0"
          >
            <div class="text-center w-100">
              <div class="d-flex justify-center" style="position: relative;">
                <div class="font-weight-medium text-uppercase">{{ contestName }}</div>
                <money :curContest="curContest" />
              </div>
              <div class="subtitle-2 ">
                <span>{{ contestDate }}</span>
              </div>
              <div v-if="eventStarted" class="red--text lighten-1 h6">({{curContest.action}})</div>
              <flip-countdown @stopTimer="disableSelection" v-if="countable" :deadline="deadline2"></flip-countdown>
              <div class="overline">{{totalFighters}} FIGHTERS ( <b style="color:#fffd">SQUAD SIZE: {{squadSize}}</b> )</div>
            </div>
          </v-card-title>
          <v-card-text
            class="pb-0"
            style="position: relative;"
          >
            <v-icon v-if="_down" class="arrow-down" color="red">mdi-arrow-down-drop-circle-outline</v-icon>
            <v-btn v-if="_side" class="arrow-side" :class="sideCollapseClass" @click="collapseSide" fab small color="#eeea"><v-icon color="red">mdi-arrow-collapse-right</v-icon></v-btn>
            <div
              id="scrollContainer"
              style="height: 300px; overflow-y: scroll; -webkit-overflow-scrolling: touch; -webkit-overflow-scrolling: scroll; position: relative;"
              @scroll="onScroll"
            >
              <template v-for="item in bouts">
                <v-btn-toggle
                  v-model="contests[item.id]"
                  :disabled="loading"
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
          </v-card-text>
          <div class="d-flex justify-center my-2 mr-2">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn 
                  class="success mr-2" 
                  :disabled="submitDisabled"
                  :loading="loading"
                  small
                  v-on="on"
                  @click="submit"
                >
                  Submit
                </v-btn>
              </template>
              <span>Submit Selection</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn 
                  class="grey darken-2 mr-2" 
                  :disabled="!squadSize || eventStarted" 
                  :loading="loading"
                  small 
                  v-on="on"
                  @click="clearSelection"
                >
                  <v-icon small left>mdi-cancel</v-icon>Clear
                </v-btn>
              </template>
              <span>Clear Selection</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn 
                  small
                  v-on="on"
                  @click="copyLink"
                >
                  <v-icon size="24" color="twitter">mdi-twitter</v-icon>
                </v-btn>
              </template>
              <span>COPY: {{tweetShareLink}}</span>
            </v-tooltip>
          </div>
          
        </v-col>
        <v-col cols=12 md=6>
          <v-card-title 
          >
            <v-autocomplete 
              :loading="loading"
              v-model="curGame"
              :items="games"
              chips
              label="Select Contest"
              class="mx-5"
              @change="changeGame"
            >
              <template v-slot:selection="data">
                <v-chip
                  v-bind="data.attrs"
                  :input-value="data.selected"
                  @click="data.select"
                >
                  {{ data.item.name }}
                </v-chip>
              </template>
              <template v-slot:item="data">
                <template v-if="typeof data.item !== 'object'">
                  <v-list-item-content v-text="data.item"></v-list-item-content>
                </template>
                <template v-else>
                  <v-list-item-content>
                    <v-list-item-title v-html="data.item.name"></v-list-item-title>
                  </v-list-item-content>
                </template>
              </template>
            </v-autocomplete>
          </v-card-title>
          <instruction-body :key="key" :rulesSet="rulesSet" :instructions="instructions" v-if="needsInstruction" />
        </v-col>
      </v-row>
    </v-card>

    <!-- hidden -->
    <input type="hidden" id="twitterLink" :value="tweetShareLink" name="">
  </div>
</template>

<script>
  let ROOT_PATH = 'http://localhost:8085'
  import main from '@/api/main'
  import { beautifyDate, equals } from '@/util'
  import { DEFAULT_INSTRUCTIONS, DEFAULT_RULES_SET } from '@/constants/constant'
  import { mapState, mapGetters } from 'vuex'
  import FlipCountdown from "./Countdown";
  import Money from "./Money";
  import InstructionBody from "../instruction/InstructionBody";

  const fmt = "YYYY-MM-DD HH:mm:ss";
  export default {
    name: 'Selection',

    components: {
      FlipCountdown,
      InstructionBody,
      Money
    },

    props: ['game_id'],

    watch: {
      event: {
        handler(val) {
          if (val) {
            this.startCountDown(val.date)
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
        snackbar: {
          snack: true,
          message: '',
          status: 'success'
        },
        toggle_multiple: [0, 1],
        squadSize: 0,
        cntdownInstance: null,
        top: 0,
        sHeight: -1,
        games: [],
        curGame: -1,
        instructions: [],
        rulesSet: [],
        key: 0,
        side: true
      }
    },

    computed: {
      ...mapState(['event']),
      ...mapState('auth', ['authUser']),
      ...mapGetters('auth', ['isAuthenticated']),
      submitDisabled() {
        return this.loading || !this.event || this.eventStarted || this.bouts.length < 1 || this.event.started
      },
      contestName () {
        return this.curContest && this.curContest.name || ""
      },
      isPaidContest () {
        return this.curContest && this.curContest.genre == 'paid'
      },
      curContest () {
        let contest = undefined
        if (this.curGame == -1) {
          contest = this.event
        } else {
          this.games.map(game => {
            if (game.value == this.curGame) {
              contest = game
            }
          })
        }
        return contest
      },
      leftMargin () {
        return this.$vuetify.breakpoint.mobile ? 5 : 50
      },
      contestDate () {
        return beautifyDate(this.curContest.date)
      },
      eventStarted () {
        return this.curContest && this.curContest.action != '' || this.countdownEnd
      },
      countable () {
        return this.deadline2 && !this.eventStarted
      },
      totalFighters () {
        return this.bouts && this.bouts.length * 2 || 0
      },
      needsInstruction () {
        return true
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
      },
      _side() {
        return !this.$vuetify.breakpoint.mobile && false
      },
      sideCollapseClass () {
        return ''
      },
      defaultInstructions () {
        return DEFAULT_INSTRUCTIONS
      },
      defaultRulesSet () {
        return DEFAULT_RULES_SET
      },
      tweetShareLink () {
        let link = `${process.env.VUE_APP_URL}/contest/${this.curGame}`
        if (this.curGame == -1) {
          link = `${process.env.VUE_APP_URL}/contest`
        }
        return link
      }
    },

    async mounted () {
      this.curGame = +this.game_id || -1

      this.loading = true
      await this.getFighters()
      this.rulesSet = this.defaultRulesSet
      this.instructions = this.defaultInstructions
      await this.getLatestData(this.game_id || -1)
      this.loading = false

      // return login
    },
    methods: {
      beautifyDate,
      onScroll ({ target: { scrollTop, clientHeight, scrollHeight }}) {
        this.top = scrollTop
        this.sHeight = scrollHeight
        if (scrollTop + clientHeight >= scrollHeight) {
        }
      },
      startCountDown(val) {
        this.deadline2 = this.$moment(`${val}`).format(fmt)
      },
      preselectFighters() {
        this.bouts.map(bout => {
          this.contests[bout.id] = []
          if (bout.survivors) {
            this.contests[bout.id] = bout.survivors
          }
        })
      },
      async getLatestData(game_id=-1) {
        await this.getLatestEvent(game_id)
        this.preselectFighters()
        this.changeContests()
      },
      async getLatestEvent (game_id=-1) {
        const { data } = await main.getLatestEvent(game_id)
        this.bouts = data.bouts
        this.$store.commit('SET_EVENT', data.event)
        this.games = data.games
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
        const event_id = this.curContest.id || this.curContest.event_id
        const payload = {
          entry: {
            game: this.curGame,
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
        this.loading = true
        const { data } = await main.createEntries(payload)
        this.snackbar = {
          ...data,
          snack: true
        }
        this.loading = false
        this.$store.commit('snackbar/setSnack', this.snackbar)

        if (data.status == 'success') {
          const self = this
          setTimeout(function(){ self.$router.push({'path': `/contest/${self.curGame}`}); }, 1200);
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
      },
      async changeGame (item) {
        this.loading = true
        await this.getLatestData(item)
        if (item == -1) {
          this.instructions = this.defaultInstructions
          this.rulesSet = this.defaultRulesSet
        } else {
          this.instructions = this.curContest.instructions.split('\n')
          this.rulesSet = this.curContest.rules_set.split('\n')
          this.key++
        }
        this.startCountDown(this.curContest.date)
        this.loading = false
      },
      collapseSide () {
        this.side = !this.side
      },
      copyLink () {
        let testingCodeToCopy = document.querySelector('#twitterLink')
        testingCodeToCopy.setAttribute('type', 'text')
        testingCodeToCopy.select()

        try {
          var successful = document.execCommand('copy');
          this.snackbar.message = successful ? 'Copied' : 'Cannot copy';
          this.snackbar.status = successful ? 'success' : 'warning';
        } catch (err) {
          this.snackbar.message = 'Oops, unable to copy';
        }

        /* unselect the range */
        testingCodeToCopy.setAttribute('type', 'hidden')
        window.getSelection().removeAllRanges()
        this.$store.commit('snackbar/setSnack', this.snackbar)
      }
    }
  }
</script>

<style lang="scss">
  .v-list .v-subheader{
    height: 15px;
    color: #008000;
  }

  #selection {
    
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
      bottom: 6px;
      left: calc(50% - 17px);
      z-index: 2;
    }

    .arrow-down {
      position: absolute;
      top: 0;
      left: calc(50% - 11px);
      z-index: 2;
    }

    .arrow-side {
      position: absolute;
      top: 50%;
      right: 0;
      z-index: 2;
    }
  }
</style>
