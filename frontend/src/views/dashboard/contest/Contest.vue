<template>
  <div id="contest-table">
    <v-card
      tile
      max-width="100%"
      class="ma-0 pb-3 fq-popup"
      :class="{'y-scroll': !$vuetify.breakpoint.mobile}"
    >
      <v-card-title 
        class="font-weight-medium mb-0 ml-md-5"
      >
        <div class="text-center w-100 mr-10">
          <div class="d-flex justify-center" style="position: relative;">
            <div class="font-weight-medium text-uppercase">{{ contestName }}</div>
            <!-- <money :curContest="curContest" /> -->
          </div>
          <div class="subtitle-1">
            {{ contestDate }}
            <span v-if="eventStarted" class="red--text h6">({{curContest.action}})</span>
          </div>
        </div>
        <v-row no-gutters class="align-center">
          <v-col class="py-0">
            <v-autocomplete 
              :loading="loading"
              v-model="curGame"
              :items="games"
              chips
              dense
              item-value="id"
              item-text="name"
              label="Select Contest"
              class="mt-2 mr-4 hidden-detail"
              @change="changeGame"
            >
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
          </v-col>
          <v-spacer />
          <div v-if="curContest" class="d-flex align-center">
            <v-btn 
              class="mr-2"
              :class="{'success': joinLabel.includes('JOIN'), 'highlight': joinLabel=='LIVE' }"
              small
              :loading="loading"
              @click="joinContest"
            >
              {{joinLabel}}
            </v-btn>
            <div v-if="isPrivateContest" class="mr-2">
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-icon v-on="on" color="highlight">mdi-account-group-outline</v-icon> 
                </template>
                <span>Entrants</span>
              </v-tooltip>
              <span class="highlight--text ml-1">{{_entrants}}</span>
            </div>
            <div 
              class="d-flex"
            >
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-icon v-on="on" size=18 color="gold">mdi-medal-outline</v-icon>
                </template>
                <span>Prize Pool</span>
              </v-tooltip>
              <span class="gold--text ml-1">{{_prize}}</span>
            </div>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn @click="instructionDlg=true" color="warning" icon v-on="on"><v-icon>mdi-dots-vertical</v-icon></v-btn>
              </template>
              <span>More</span>
            </v-tooltip>
          </div>
        </v-row>
      </v-card-title>
      <v-card-text
        class="w-100"
      >
        <v-tabs
          grow
          centered
          hide-slider
          v-model="tab"
          background-color="transparent"
          slider-color="red lighten-1"
          color="basil"
        >
          <v-tab
            v-for="item in tabs"
            :key="item.text"
            :title="item.text"
            :href='`#${item.text}`'
            active-class="winner"
          >
            {{item.text}}
            <v-icon right>{{item.icon}}</v-icon>
          </v-tab>
        </v-tabs>
        <v-tabs-items
          v-model="tab"
          :touchless="$vuetify.breakpoint.mobile"
        >
          <!-- fight/bout view -->
          <v-tab-item value="fights">
            <fight-tab :boutViews="boutViews" :diedUsers="diedUsers" :loading="loading"/>
          </v-tab-item>

          <!-- Entry view -->
          <v-tab-item value="standings">
            <standing-tab :entryViews="entryViews" :loading="loading"/>
          </v-tab-item>

          <!-- Chat -->
          <v-tab-item value="chat">
            <chat />
          </v-tab-item>
        </v-tabs-items>
      </v-card-text>
    </v-card>

    <v-dialog 
      v-model="instructionDlg"
      width="600px"
    >
      <instruction-body :instructions="curInstructions" :rulesSet="curRulesSet" />
    </v-dialog>
  </div>
</template>

<script>
  import main from '@/api/main'
  import { beautifyDate } from '@/util'
  import FightTab from './FightTab'
  import StandingTab from './StandingTab'
  import Money from '../selection/Money'
  import InstructionBody from '../instruction/InstructionBody'
  import Chat from './Chat'
  import { mapState } from 'vuex'

  export default {
    name: 'Contest',

    components: { 
      FightTab,
      StandingTab,
      Chat,
      Money,
      InstructionBody
    },

    props: ['game_id'],

    data () {
      return {
        loading: false,
        instructionDlg: false,
        tab: 'standings',
        boutViews: [],
        entryViews: [],
        diedUsers: [],
        tabs: [
          {
            text: 'fights',
            icon: 'mdi-fencing'
          },
          {
            text: 'standings',
            icon: 'mdi-view-list-outline'
          },
          {
            text: 'chat',
            icon: 'mdi-chat-outline'
          }
        ],
        games: [],
        curGame: -1,
      }
    },

    filters: {
      beautifyDate
    },

    computed: {
      ...mapState(['event']),
      ...mapState('auth', ['authUser', 'profile']),

      contestName () {
        return this.curContest && this.curContest.name || ""
      },
      curContest () {
        let contest = undefined
        this.games.map(game => {
          if (game.id == this.curGame) {
            contest = game
          }
        })
        return contest
      },
      contestDate () {
        return this.curContest && beautifyDate(this.curContest.date) || ""
      },
      curInstructions () {
        return this.curContest && this.curContest.instructions.split('\n') || []
      },
      curRulesSet () {
        return this.curContest && this.curContest.rules_set.split('\n') || []
      },
      joinLabel () {
        let label = 'JOIN'
        if (this.curContest.can_have_entry) {
          label = 'JOIN AGAIN'
        } 
        if (this.curContest.genre != 'free') {
          label += ` | F${this.curContest.buyin}`
        }
        if (this.isStartedGame) {
          label = 'LIVE'
        }
        if (this.curContest.has_joined && !this.isStartedGame) {
          label = 'EDIT'
        } 
        return label
      },
      isStartedGame () {
        return this.$moment().isSameOrAfter(this.$moment(this.curContest.date))
      },
      isPrivateContest () {
        return this.curContest?.type_of_registration == 'private'
      },
      eventStarted () {
        if (!this.curContest) {
          return false
        }
        let val = '';
        if (this.curContest.owner == 'admin') {
          val = this.curContest.event.date
        } else {
          const date = this.$moment(this.curContest.event.date).format('YYYY-MM-DD')
          val = `${date} ${this.curContest.custom_date}`
        }
        const diff = this.$moment(val).diff(this.$moment(), 'seconds')
        return diff <= 0
      },
      _entrants () {
        const val = this.curContest?.joined_users?.length || 0
        return val
      },
      _prize () {
        const val = this.curContest?.prize || 0
        return val
      }
    },

    mounted() {
      this.curGame = +this.game_id || -1
      this.getLatestContest(this.curGame)
      
      // preselect tab
      const tabParam = this.$route.query.tab
      if (this.tabs.includes(tabParam)) {
        this.tab = tabParam
      }
    },

    methods: {
      async getLatestContest(game_id=-1) {
        this.loading = true
        const { data } = await main.getLatestContest(game_id)
        this.boutViews = data.bout_views
        this.entryViews = data.entry_views
        this.diedUsers = data.died_users
        this.games = data.games
        if (data.games.length > 0 && this.curGame == -1) {
          this.curGame = data.games[0].id
          data.games.forEach(game => {
            if (game.name.trim().toLowerCase() == 'main contest') {
              this.curGame = game.id
            }
          })
        }
        this.$store.commit('SET_EVENT', data.event)
        this.loading = false
      },
      async joinContest () {
        let snackbar = {snack: true};
        if (!this.authUser) {
          localStorage.setItem('returnUrl', this.$route.path)
          return this.$store.commit('auth/showLoginDlg')
        }
        if (this.joinLabel == 'EDIT' || this.joinLabel == 'LIVE') {
          return this.$router.push({ path: `/selection/${this.curContest.id}` })
        }
        if (this.curContest.buyin) {
            if (this.authUser?.coins < this.curContest.buyin) {
            snackbar = {
              ...snackbar,
              message: "You don't have enough coins",
              status: 'error'
            }
            return this.$store.dispatch('snackbar/setSnack', snackbar)
          } 
        }
        let payload = {
          game_id: this.curContest.id,
        }
        this.loading = true
        const { data } = await main.joinGame(payload)
        if (data.status == 200) {
          this.$store.dispatch('auth/loadProfile')
          this.$router.push({ path: `/selection/${this.curContest.id}/${data.entry_number}` })
        }
        snackbar = {
          ...snackbar,
          message: data.message,
          status: data.status == 200 ? 'success': ''
        }
        this.loading = false
        this.$store.dispatch('snackbar/setSnack', snackbar)
      },
      async changeGame (item) {
        this.$router.push({'path': `/contest/${item}`})
        // this.loading = true
        // await this.getLatestContest(item)
        // this.loading = false
      },
    }
  }
</script>
