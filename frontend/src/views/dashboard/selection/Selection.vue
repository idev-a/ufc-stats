<template>
  <div 
    id="selection"
    :style="`height: ${height}`" 
  >
    <v-card
      tile
      :loading="loading"
      class="lighten-4 ma-0 pa-0 selection-card fq-popup"
    >
      <v-row dense no-gutters>
        <v-col cols=12 md=6>
          <v-card-title 
            v-if="curContest" 
            class="font-weight-medium mb-0"
          >
            <div class="text-center w-100">
              <div class="d-flex justify-center relative">
                <div class="font-weight-medium text-uppercase">{{ contestName }}</div>
                <money :curContest="curContest" />
              </div>
              <div class="subtitle-2 ">
                <span>{{ contestDate }}</span>
                <v-tooltip right>
                  <template v-slot:activator="{ on }">
                    <v-icon v-on="on" v-if="isTournament" color="info" size=22> mdi-tournament mdi-rotate-270</v-icon>
                  </template>
                  <span>Tournament Type</span>
                </v-tooltip>
              </div>
              <div v-if="eventStarted" class="red--text lighten-1 h6">({{curContest.action}})</div>
              <flip-countdown :showDays="false" @stopTimer="disableSelection" v-if="countable" :deadline="deadline2"></flip-countdown>
              <div class="overline">{{totalFighters}} FIGHTERS ( <b class="silver--text">SQUAD SIZE: {{squadSize}}</b> )</div>
            </div>
          </v-card-title>
          <v-card-text
            class="py-3 relative"
          >
            <v-icon v-if="_down" class="arrow-down" color="red">mdi-arrow-down-drop-circle-outline</v-icon>
            <v-btn v-if="_side" class="arrow-side" :class="sideCollapseClass" @click="collapseSide" fab small color="#eeea"><v-icon color="red">mdi-arrow-collapse-right</v-icon></v-btn>
            <div
              id="scrollContainer"
              @scroll="onScroll"
            >
              <template v-for="item in bouts">
                <v-btn-toggle
                  v-model="item.survivors"
                  :disabled="loading"
                  :key="item.id"
                  dense
                  multiple
                  class="justify-space-between mb-2 mx-1"
                  tile
                  @change="changeContests"
                >
                  <fighter 
                    :id="item.fighter1"
                    :fighters="fighters"
                    :eventStarted="eventStarted"
                    :firstName="true"
                  />

                  <div 
                    class="between-fighters"
                  >
                    ({{ item.division }})
                  </div>

                  <fighter 
                    :id="item.fighter2"
                    :fighters="fighters"
                    :eventStarted="eventStarted"
                    :firstName="true"
                  />

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
              <span>Submit & Go Contest</span>
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
            <v-tooltip
              v-if="isTournament"
              bottom
            >
              <template v-slot:activator="{ on }">
                <v-btn 
                  class="info mr-2" 
                  :disabled="!hasPrevRetryNumber" 
                  :loading="loading"
                  small 
                  v-on="on"
                  @click="gotoPrevEntry"
                >
                  <v-icon small>mdi-step-backward</v-icon>
                </v-btn>
              </template>
              <span>Sumbit & Go Prev Entry</span>
            </v-tooltip>
            <v-tooltip
              v-if="isTournament"
              bottom
            >
              <template v-slot:activator="{ on }">
                <v-btn 
                  class="info mr-2" 
                  :disabled="!hasNextRetryNumber" 
                  :loading="loading"
                  small 
                  v-on="on"
                  @click="gotoNextEntry"
                >
                  <v-icon small>mdi-step-forward</v-icon>
                </v-btn>
              </template>
              <span>Sumbit & Go Next Entry</span>
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
              label="Select Entry"
              class="mx-5"
              return-object
              @change="changeGame"
            >
              <template v-slot:selection="data">
                <v-chip
                  v-bind="data.attrs"
                  :input-value="data.selected"
                  @click="data.select"
                >
                  {{ gameName(data.item) }}
                </v-chip>
              </template>
              <template v-slot:item="data">
                <template v-if="typeof data.item !== 'object'">
                  <v-list-item-content v-text="data.item"></v-list-item-content>
                </template>
                <template v-else>
                  <v-list-item-content>
                    <v-list-item-title v-html="gameName(data.item)"></v-list-item-title>
                  </v-list-item-content>
                </template>
              </template>
            </v-autocomplete>
          </v-card-title>
          <contest-summary :key="key" :rulesSet="rulesSet" :summary="summary" v-if="needsInstruction" />
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
  import { DEFAULT_INSTRUCTIONS, DEFAULT_RULES_SET, DEFAULT_SUMMARY } from '@/constants/constant'
  import { mapState, mapGetters } from 'vuex'
  import FlipCountdown from "./Countdown";
  import Money from "./Money";
  import Fighter from "./Fighter";
  import ContestSummary from "./ContestSummary";

  const fmt = "YYYY-MM-DD HH:mm:ss";
  export default {
    name: 'Selection',

    components: {
      FlipCountdown,
      ContestSummary,
      Money,
      Fighter
    },

    props: ['game_id', 'entry_number'],

    watch: {
      isTournament (val) {
        this.key++
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
        curGame: this.game_id  || -1,
        instructions: [],
        rulesSet: [],
        summary: '',
        key: 0,
        side: true
      }
    },

    computed: {
      ...mapState(['event']),
      ...mapState('auth', ['authUser']),
      ...mapGetters('auth', ['isAuthenticated']),
      submitDisabled() {
        return this.loading || !this.event || this.eventStarted || this.bouts.length < 1 || this.event.started || !this._validRetryNumber()
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
      contestName () {
        return this.curContest?.name || ""
      },
      isTournament () {
        return this.curContest?.re_entry || false
      },
      hasPrevRetryNumber () {
        return this.isTournament && this.entry_number > 1 && this.curContest.multientry >= this.entry_number
      },
      hasNextRetryNumber () {
        return this.isTournament && this.entry_number > 0 && this.entry_number < this.curContest.multientry
      },
      leftMargin () {
        return this.$vuetify.breakpoint.mobile ? 5 : 50
      },
      contestDate () {
        return beautifyDate(this.curContest.date)
      },
      eventStarted () {
        return this.curContest?.action != '' || this.countdownEnd
      },
      countable () {
        const diff = this.$moment(this.deadline2).diff(this.$moment(), 'days')
        return this.deadline2 && !this.eventStarted && diff == 0
      },
      totalFighters () {
        return this.fighters?.length || 0
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
      defaultInstructions () {
        return DEFAULT_INSTRUCTIONS
      },
      defaultRulesSet () {
        return DEFAULT_RULES_SET
      },
      defaultSummary () {
        return DEFAULT_SUMMARY
      },
      tweetShareLink () {
        let link = `${process.env.VUE_APP_URL}/contest/${this.game_id}`
        if (this.game_id == -1) {
          link = `${process.env.VUE_APP_URL}/contest`
        }
        if (this._validRetryNumber()) {
          link += `/${this.entry_number}`
        }
        return link
      }
    },

    async mounted () {
      this.curGame = `${this.game_id||-1}_${this.entry_number||1}`

      this.loading = true
      this.rulesSet = this.defaultRulesSet
      this.instructions = this.defaultInstructions
      this.summary = this.defaultSummary
      await this.getLatestData()
      this.loading = false
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
      async getLatestData() {
        await this.getLatestEvent()
        this.changeContests()
      },
      async getLatestEvent () {
        const { data } = await main.getLatestEvent(this.curGame, +this.entry_number)
        this.bouts = data.bouts
        this.fighters = data.fighters
        this.games = data.games
        if (data.games.length > 0 && this.curGame == '-1_1') {
          this.curGame = data.games[0].value
          data.games.forEach(game => {
            if (game.name.trim().toLowerCase() == 'main contest') {
              this.curGame = game.value
            }
          })
          this.startCountDown(this.curContest.event.date)
        }
      },
      gameName (item) {
        let name = item.name
        if (item.re_entry) {
          name += ` (${item.entry_number})`
        }
        return name
      },
      _validRetryNumber() {
        if (this.isTournament) {
          return this.entry_number > 0 && this.entry_number <= this.curContest.multientry
        } else {
          return true
        }
      },
      async _submit (callback) {
        if (!this.isAuthenticated) {
          this.$store.commit('auth/showLoginDlg')
          return
        }
        if (!this._validRetryNumber()) {
          return
        }
        const payload = {
          entry: {
            entry_number: this.entry_number,
            game: this.curGame.split('_')[0],
            event: this.curContest.event.id,
          },
          selections: []
        }
        let selected = false
        this.bouts.forEach(bout => {
          if (bout.survivors.length) {
            selected = true
          }
          payload.selections.push({
            bout: bout.id,
            survivor1: bout.survivors?.[0] || null,
            survivor2: bout.survivors?.[1] || null,
          })
        })

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
        try {
          const { data } = await main.createEntries(payload)
          this.snackbar = {
            ...data,
            snack: true
          }
          if (callback) {
            if (data.status == 'success'){
              callback(data)
            }
          }
        } catch (e) {
          this.snackbar = {
            message: e.response.data.message,
            status: 'dark',
            snack: true
          }
        }
        this.loading = false
        this.$store.commit('snackbar/setSnack', this.snackbar)
      },

      async submit (data) {
        const self = this
        await this._submit((data) => {
          setTimeout(function(){ self.$router.push({'path': `/contest/${self.game_id}`}); }, 1200);
        })
      },
      clearSelection () {
        this.squadSize = 0
      },
      changeContests() {
        this.squadSize = 0
        for (const bout in this.survivors) {
          this.squadSize += bout.survivors.length
        }
      },
      async gotoPrevEntry () {
        await this._submit((data) => {
          this.$router.push({ path: `/selection/${this.game_id}/${this.entry_number-1}`})
        })
      },
      async gotoNextEntry () {
        await this._submit((data) => {
          this.$router.push({ path: `/selection/${this.game_id}/${this.entry_number+1}`})
        })
      },
      disableSelection () {
        this.countdownEnd = true
      },
      async changeGame (item) {
        let path = `/selection/${item.id}`
        if (item.re_entry) {
          path += `/${item.entry_number}`
        }
        return this.$router.push({ path })
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
</style>
