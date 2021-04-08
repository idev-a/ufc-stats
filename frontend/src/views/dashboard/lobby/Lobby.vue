<template>
  <div id="contest-table">
    <v-card
      tile
      max-width="100%"
      class="ma-0 pa-0 pb-3 fq-popup"
      :class="{'y-scroll': !$vuetify.breakpoint.mobile}"
    >
      <v-card-title 
        class="font-weight-medium mb-4"
      >
        <div v-if="$vuetify.breakpoint.mobile" class="mr-5">Lobby</div>
        <v-spacer v-if="$vuetify.breakpoint.mobile" />
        <v-btn v-if="$vuetify.breakpoint.mobile" small class="success mr-2" :loading="loading" :disabled="loading || !authUser" @click="loadMyGames"><v-icon left>mdi-filter-variant</v-icon> My Games</v-btn>
        <create-game-btn 
          v-if="$vuetify.breakpoint.mobile"
          :loading="loading"
          :authUser="authUser"
          @create-new-game="newGame"
        />
        <div class="d-flex align-center">
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search games"
            clearable
            class="mb-5"
            single-line
            hide-details
          />
          <v-select
            v-model="type"
            class="ml-2"
            :items="types"
            hint="Public / Private"
            persistent-hint
            label="Type"
          />
          <v-select
            v-model="genre"
            class="ml-2"
            :items="genres"
            label="Genre"
            hint="Free / Paid"
            persistent-hint
          >
          </v-select>
        </div>
        <v-spacer v-if="!$vuetify.breakpoint.mobile" />
        <v-btn v-if="!$vuetify.breakpoint.mobile" small class="success mr-2" :loading="loading" :disabled="loading || !authUser" @click="loadMyGames"><v-icon left>mdi-filter-variant</v-icon> My Games</v-btn>
        <create-game-btn 
          v-if="!$vuetify.breakpoint.mobile"
          :loading="loading"
          :authUser="authUser"
          @create-new-game="newGame"
        />
      </v-card-title>
      <v-card-text
        class="w-100 lobby-table"
        elevation="1"
        outlined
      >
        <v-data-table
          :items="filteredGames"
          :loading="loading"
          :headers="headers"
          :search="search"
          fixed-header
          :disable-pagination="true"
          item-key="id"
          dense
          height="280px"
          hide-default-footer
          mobile-breakpoint="0"
          @click:row="loadGameDetail"
        > 
          <template v-slot:item.name="{ item }">
            <span>{{ item.name | upperFirst }}</span>
          </template>
          <template v-slot:item.event="{ item }">
            <span>{{ item.event.name }}</span>
          </template>
          <template v-slot:item.type_of_registration="{ item }">
            <span>{{ item.type_of_registration | upperFirst }}</span>
          </template>
          <template v-slot:item.genre="{ item }">
            <span>{{ item.genre | upperFirst }}</span>
          </template>
          <template v-slot:item.entrants="{ item }">
            <span v-if="item.type_of_registration == 'private'">{{ item.joined_users.length }} / {{ item.entrants.length }}</span>
            <span v-else>All</span>
          </template>
          <template v-slot:item.teams="{ item }">
            <span>{{ teamInfo(item) }}</span>
          </template>
          <template v-slot:item.date="{ item }">
            <span>{{ item.date | beautifyDateTimeMin }}</span>
          </template>
          <template v-slot:item.actions="{ item }">
            <v-tooltip right>
              <template  v-slot:activator="{ on }">
                <div v-on="on">
                  <v-btn 
                    small
                    class="my-1" 
                    :class="{'success': joinLabel(item).includes('JOIN'), 'highlight': joinLabel(item) == 'LIVE'}"
                    @click.stop="joinContest(item)"
                  >
                    {{joinLabel(item)}}
                  </v-btn>
                </div>
              </template>
              <span>{{ JoinBtnTooltip(item) }}</span>
            </v-tooltip>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Game detail dialog -->
    <v-dialog
      v-model="dlg"
      scrollable
      max-width="800"
    >
      <v-card
        class="fq-popup"
        v-if="curGame && curGame.event"
      >
        <v-card-title :class="{'pa-0': $vuetify.breakpoint.mobile}">
          <v-list three-line style="background: none;">
            <v-list-item
            >
              <v-list-item-avatar>
                <v-img :src="gameAvatar"></v-img>
              </v-list-item-avatar>

              <v-list-item-content class="text-left">
                <v-list-item-title class="display-2" v-html="curGame.name"></v-list-item-title>
                <v-list-item-subtitle><b>Start at</b> {{ curGame.date | beautifyDateTimeMin }}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <div class="d-md-flex">
                  <v-tooltip left>
                    <template  v-slot:activator="{ on }">
                      <div v-on="on">
                        <v-btn 
                          small
                          class="my-1 mr-2" 
                          :class="{'success': joinLabel(curGame).includes('JOIN'), 'highlight': joinLabel(curGame) == 'LIVE'}"
                          @click.stop="joinContest(curGame)"
                        >
                          {{joinLabel(curGame)}}
                        </v-btn>
                      </div>
                    </template>
                    <span>{{ JoinBtnTooltip(curGame) }}</span>
                  </v-tooltip>
                  <v-tooltip left>
                    <template  v-slot:activator="{ on }">
                      <div v-on="on">
                        <v-btn 
                          small
                          v-if="isStartedGame(curGame) && joinLabel(curGame) != 'LIVE'"
                          class="my-1 highlight" 
                          :disabled="canJoin(curGame) == 'No enough coins'" 
                          @click.stop="gotoContest(curGame)"
                        >
                          LIVE
                        </v-btn>
                      </div>
                    </template>
                    <span>Go to Contest</span>
                  </v-tooltip>
                </div>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-card-title>

        <v-card-text class="pt-0">
          <v-tabs
            align-with-title
            v-model="tab"
            background-color="transparent"
            slider-color="highlight"
            color="basil"
          >
            <v-tab
              v-for="item in tabs"
              :key="item"
            >
              {{item}}
            </v-tab>
          </v-tabs>
          <v-tabs-items
            v-model="tab"
            :touchless="$vuetify.breakpoint.mobile"
          >
            <!-- Content Detail -->
            <v-tab-item>
              <game-detail :game="curGame"/>
            </v-tab-item>

            <!-- Rules -->
            <v-tab-item>
              <rules :game="curGame"/>
            </v-tab-item>
          </v-tabs-items>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- New Game Dialog -->
    <v-dialog
      v-model="newDlg"
      max-width=850
    >
      <v-card
        tile
        class="fq-popup"
      >
        <v-card-title>
          <div class="font-weight-medium display-2">{{defaultIndex == -1 ? 'New Game' : 'Update Game'}}</div>
          <div v-if="!isAdmin" class="subtitle">{{latestEvent.name}} ({{latestEvent.date | beautifyDate}})</div>
        </v-card-title>
        <v-card-text>
          <v-form
            ref="form"
            v-model="valid"
            lazy-validation
          >
            <v-row >
              <v-col
                cols=12
                md=4
                sm=6
              >
                <v-text-field
                  v-model="form.name"
                  :rules="[rules.required]"
                  label="Name"
                  clearable
                  single-line
                />
              </v-col>
              <v-col
                cols=12
                md=6
                sm=6
                v-if="isAdmin"
              >
                <v-autocomplete
                  v-model="form.event"
                  :items="upcomingEvents"
                  item-value="id"
                  item-text="name"
                  chips
                  :rules="[rules.required]"
                  label="Upcoming Event"
                >
                  <template v-slot:selection="data">
                    <v-chip
                      v-bind="data.attrs"
                      :input-value="data.selected"
                      @click="data.select"
                    >
                      {{ data.item.name }} ({{data.item.date | beautifyDate}})
                    </v-chip>
                  </template>
                  <template v-slot:item="data">
                    <v-list-item-content>
                      {{ data.item.name }} ({{data.item.date | beautifyDate}})
                    </v-list-item-content>
                  </template>
                </v-autocomplete>
              </v-col>
              <v-col
                cols=12
                md=2
                sm=6
              >
                <v-text-field
                  type=number
                  min=0
                  v-model="form.multientry"
                  label="Multi Entry"
                  hint="Multi Entry"
                  persistent-hint
                  clearable
                  single-line
                />
              </v-col>
              <v-col
                cols=12
                v-if="isAdmin"
              >
                <v-autocomplete
                  v-model="form.bouts"
                  :items="bouts"
                  multiple
                  item-value="id"
                  item-text="name"
                  chips
                  hide-selected
                  :rules="[rules.required]"
                  label="Fight"
                >
                  <template v-slot:selection="data">
                    <v-chip
                      v-bind="data.attrs"
                      :input-value="data.selected"
                      close
                      @click="data.select"
                      @click:close="remove(data.item)"
                    >
                      {{ data.item.fighter1.initials }} <b class="mx-1">vs.</b> {{ data.item.fighter2.initials }}
                    </v-chip>
                  </template>
                  <template v-slot:item="data">
                    <v-list-item-content>
                      {{ data.item.fighter1.initials }} vs. {{ data.item.fighter2.initials }}
                    </v-list-item-content>
                  </template>
                </v-autocomplete>
              </v-col>
              <v-col
                cols=12
                md=4
                sm=6
              >
                <v-text-field
                  type=number
                  min=0
                  v-model="form.buyin"
                  label="Buyin"
                  hint="Buyin"
                  persistent-hint
                  clearable
                  single-line
                />
              </v-col>
              <v-col
                cols=12
                md=4
                sm=6
              >
                <v-text-field
                  type=number
                  min=0
                  v-model="form.added_prizepool"
                  label="Prize Pool"
                  hint="Prize Pool"
                  persistent-hint
                  clearable
                  single-line
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols=12
                sm=6
              >
                <v-textarea
                  outlined
                  v-model="form.instructions"
                  :rules="[rules.required]"
                  label="Instructions"
                  hint="Instructions"
                  persistent-hint
                  rows=2
                  auto-grow
                  clearable
                  single-line
                />
              </v-col>
              <v-col
                cols=12
                sm=6
              >
                <v-textarea
                  outlined
                  v-model="form.summary"
                  :rules="[rules.required]"
                  label="Summary"
                  hint="Summary"
                  persistent-hint
                  rows=2
                  auto-grow
                  clearable
                  single-line
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols=12
              >
                <v-textarea
                  outlined
                  v-model="form.rules_set"
                  :rules="[rules.required]"
                  label="Rules Set"
                  hint="Rules Set"
                  persistent-hint
                  rows=3
                  auto-grow
                  clearable
                  single-line
                />
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn 
                v-on="on"
                :loading="loading"
                :disabled="!game_id"
                @click="copyGameLink('#myGameLink')"
              >
                <v-icon size="24" color="highlight">mdi-google-controller</v-icon>
              </v-btn>
            </template>
            <span>COPY: {{ genGameLink(game_id) }}</span>
          </v-tooltip>
          <v-btn text :loading="loading" @click="newDlg=false">Close</v-btn>
          <v-btn v-if="defaultIndex==-1" text color="success" :loading="loading" :disabled="loading || !valid" @click="createGame">Create</v-btn>
          <v-btn v-else text color="success" :loading="loading" :disabled="loading || !valid" @click="updateGame">Update</v-btn>
        </v-card-actions>
        <input type="hidden" id="myGameLink" :value="genGameLink(game_id)" name="">
      </v-card>
    </v-dialog>

    <!-- My Own Games -->
    <v-dialog
      v-model="newGameDlg"
    >
      <v-card
        id="contest-table"
        class="fq-popup"
      >
        <v-card-title class="d-flex">
          <div>
            <span class="display-2">My Games</span>
            <create-game-btn 
              class="ml-2"
              :loading="loading"
              :authUser="authUser"
              @create-new-game="newGame"
              :icon="true"
            />
          </div>
          <v-spacer />
          <v-text-field
            v-model="ownSearch"
            label="Search games"
            clearable
            class="mb-5"
            single-line
            hide-details
          />
        </v-card-title>
        <v-card-text>
          <v-data-table
            :items="myOwnGames"
            :loading="loading"
            :headers="ownHeaders"
            :search="ownSearch"
            fixed-header
            :disable-pagination="true"
            item-key="id"
            dense
            height="280px"
            hide-default-footer
            mobile-breakpoint="0"
          > 
            <template v-slot:item.name="{ item }">
              <span>{{ item.name | upperFirst }}</span>
            </template>
            <template v-slot:item.event="{ item }">
              <span>{{ item.event.name }}</span>
            </template>
            <template v-slot:item.teams="{ item }">
              <span>{{ teamInfo(item) }}</span>
            </template>
            <template v-slot:item.date="{ item }">
              <span>{{ item.date | beautifyDateTimeMin }}</span>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-tooltip right>
                <template  v-slot:activator="{ on }">
                  <v-btn 
                    small
                    v-on="on"
                    @click.stop="copyGameLink(`#gameLink${item.id}`)"
                    icon
                  >
                    <v-icon size="24" color="success">mdi-google-controller</v-icon>
                  </v-btn>
                  <input type="hidden" :id="`gameLink${item.id}`" :value="genGameLink(item.id)" name="">
                </template>
                <span>Copy Link</span>
              </v-tooltip>
              <v-tooltip right>
                <template v-slot:activator="{ on }">
                  <v-btn 
                    small
                    v-on="on"
                    class="ml-2"
                    :loading="loading"
                    :disabled="item.event.action!=''"
                    @click.stop="updateMyGame(item)"
                    icon
                  >
                    <v-icon size="24" color="info">mdi-pencil-outline</v-icon>
                  </v-btn>
                </template>
                <span>Update Game</span>
              </v-tooltip>
              <v-tooltip right>
                <template  v-slot:activator="{ on }">
                  <v-btn 
                    small
                    v-on="on"
                    class="ml-2"
                    :loading="loading"
                    :disabled="item.event.action!=''"
                    @click.stop="deleteMyGame(item.id)"
                    icon
                  >
                    <v-icon size="24" color="highlight">mdi-delete-outline</v-icon>
                  </v-btn>
                </template>
                <span>Delete Game</span>
              </v-tooltip>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>
    </v-dialog>
    <!-- hidden -->
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import upperFirst from 'lodash/upperFirst'

  import main from '@/api/main'
  import { beautifyDateTimeMin, beautifyDate } from '@/util'
  import GameDetail from './GameDetail'
  import Rules from './Rules'
  import CreateGameBtn from './CreateGameBtn'
  import { 
    DEFAULT_RULES_SET,
    DEFAULT_INSTRUCTIONS,
    DEFAULT_SUMMARY
  } from '@/constants/constant'

  export default {
    name: 'Contest',

    components: { GameDetail, Rules, CreateGameBtn },

    data () {
      return {
        loading: false,
        search: '',
        snackbar: {
          snack: true
        },
        dlg: false,
        tab: null,
        games: [],
        curGame: {},
        type: 'all',
        types:[
          {
            text: 'All',
            value: 'all'
          },
          {
            text: 'Public',
            value: 'public'
          },
          {
            text: 'Private',
            value: 'private'
          }
        ],
        genre: 'all',
        genres: [
          {
            text: 'All',
            value: 'all'
          },
          {
            text: 'Free',
            value: 'free'
          },
          {
            text: 'Paid',
            value: 'paid'
          },
        ],
        headers: [
          {
            text: 'Actions',
            value: 'actions',
            align:'center',
          },
          {
            text: 'Name',
            value: 'name',
            align: 'center',
            width: 120
          },
          {
            text: 'Event',
            value: 'event',
            align: 'center',
            width: 200
          },
          {
            text: 'Type',
            value: 'type_of_registration',
            align: 'center',
          },
          {
            text: 'Buyin',
            value: 'buyin',
            align: 'center',
          },
          {
            text: 'Prize Pool',
            value: 'prize',
            align: 'center',
          },
          {
            text: 'Entrants',
            value: 'entrants',
            align: 'center',
          },
          {
            text: 'Teams',
            value: 'teams',
            align: 'center',
          },
          {
            text: 'When',
            value: 'date',
            align: 'center',
            width: 120
          },
         
        ],
        tabs: [
          'Contest Details',
          'Rules & Scoring',
        ],
        newDlg: false,
        valid: true,
        latestEvent: {},
        defaultIndex: -1,
        defaultForm: {
            name: '',
            event: '',
            instructions: DEFAULT_INSTRUCTIONS.join('\n'),
            rules_set: DEFAULT_RULES_SET.join('\n'),
            summary: DEFAULT_SUMMARY,
            multientry: 0,
            buyin: 0,
            added_prizepool: 100,
            bouts: []
        },
        form: {
          name: '',
          event: '',
          instructions: '',
          rules_set: '',
          summary: '',
          multientry: 0,
          buyin: 0,
          added_prizepool: 100,
          bouts: []
        },
        game_id: '',
        myOwnGames: [],
        ownSearch: '',
        newGameDlg: false,
        upcomingEvents: [],
        bouts: [],
        ownHeaders: [
          {
            text: 'Name',
            value: 'name',
          },
          {
            text: 'Event',
            value: 'event',
          },
          {
            text: 'Buyin',
            value: 'buyin'
          },
          {
            text: 'Prize Pool',
            value: 'prize'
          },
          {
            text: 'Teams',
            value: 'teams'
          },
          {
            text: 'When',
            value: 'date',
            align: 'center',
          },
          {
            text: 'Actions',
            value: 'actions',
            align: 'center',
          },
        ],
        rules: {
          required: value => {
            return !!value || 'This field is required.'
          },
        }
      }
    },

    computed: {
      ...mapState('auth', ['authUser', 'profile']),
      filteredGames() {
        const temp = []
        const temp1 = []
        this.games.map(game => {
          if (this.type == 'all') {
            temp.push(game)
          } else if (game.type_of_registration == this.type) {
            temp.push(game)
          } 
        })
        temp.map(game => {
          if (this.genre == 'all') {
            temp1.push(game)
          } else if (game.genre == this.genre) {
            temp1.push(game)
          } 
        })
        return temp1
      },
      gameAvatar () {
        return require('@/assets/logo.jpg')
      },
      myId () {
        return this.authUser?.id || this.authUser?.pk
      },
      myCoins () {
        return this.authUser?.coins || this.authUser?.fq_points || this.profile?.user?.coins || 0
      },
      isAdmin () {
        return this.authUser?.roles.includes('admin')
      }
    },

    filters: {
      beautifyDateTimeMin,
      beautifyDate,
      upperFirst
    },

    mounted() {
      this.loadGames()
    },

    methods: {
      async loadGames() {
        this.loading = true
        const { data } = await main.loadGames()
        this.games = data.games
        this.latestEvent = data.latest_event
        this.upcomingEvents = data.upcoming_events
        this.bouts = data.bouts
        this.loading = false
      },
      async loadGameDetail (item) {
        this.curGame = item
        this.dlg = true
      },
      canJoin (item) {
        if (item.has_joined) {
          return 'Already Joined'
        }
        let isInvolved = false
        item.entrants && item.entrants.map(user => {
          if (user.id == this.myId) {
            isInvolved = true
          }
        })
        if (this.isStartedGame(item)) {
          return 'Game started'
        }

        if (item.genre != 'free') {
          if (!this.hasEnoughCoins(item)) {
            return 'No enough coins'
          }
        }

        if (item.type_of_registration == 'public') {
          return 'ok'
        } else if (item.type_of_registration == 'private' && isInvolved) {
          return "ok"
        }

        return 'no'
      },
      JoinBtnTooltip(item) {
        let tooltip = ''
        if (item.genre != 'free') {
          if (!this.hasEnoughCoins(item)) {
            tooltip =  'No enough coins'
          }
        }
        const label = this.joinLabel(item)
        if (item.genre != 'free') {
          if (!this.hasEnoughCoins(item)) {
            tooltip = 'No enough coins'
          }
        }
        if (label.includes('JOIN')) {
          tooltip = 'Go to Selection'
        } else if (label == 'VIEW') {
          tooltip = 'Go to Selection'
        } else if (label == 'LIVE') {
          tooltip = 'Go to Contest'
        } 
        return tooltip
      },
      hasEnoughCoins(item) {
        return this.myCoins >= item.buyin
      },
      isStartedGame (item) {
        return this.$moment().isSameOrAfter(this.$moment(item.date))
      },
      joinLabel (item) {
        let label = 'JOIN'
        if (item.has_joined) {
          label = 'VIEW'
        } else {
          if (item.genre != 'free') {
            label += ` | F${item.buyin}`
          }
        }
        if (item.id == -1) {
          label = 'VIEW'
        }
        if (this.isStartedGame(item) && label == 'VIEW') {
          label = 'LIVE'
        }
        return label
      },
      gotoContest (item) {
        this.$router.push({ path: `/contest/${item.id}`, query: {tab: 'standings'}})
      },
      async joinContest (item) {
        if (!this.authUser) {
          localStorage.setItem('returnUrl', this.$route.path)
          return this.$store.commit('auth/showLoginDlg')
        }
        const label = this.joinLabel(item)
        if (label == 'LIVE') {
          return this.$router.push({ path: `/contest/${item.id}`, query: {tab: 'standings'}})
        }
        if (label == 'VIEW') {
          return this.$router.push({ path: `/selection/${item.id}` })
        }
        if (item.id == -1) {
          return this.$router.push({ path: `/selection` })
        }
        let snackbar = {snack: true};
        if (!this.hasEnoughCoins(item)) {
          snackbar = {
            ...snackbar,
            message: "You don't have enough coins",
            status: 'error'
          }
        } else {
          let payload = {
            game_id: item.id,
            user_id: this.myId
          }
          const res = await main.joinGame(payload)
          if (res.status == 200) {
            this.loadGames()
            this.$store.dispatch('auth/loadProfile')

            this.$router.push({ path: `/selection/${item.id}` })
          }
          snackbar = {
            ...snackbar,
            message: res.data.message,
            status: res.status == 200 ? 'success': ''
          }
        }
        this.$store.dispatch('snackbar/setSnack', snackbar)
      },
      teamInfo(item) {
        let info = `${item.engaged_teams}/${item.entry_limit}`
        if (item.type_of_registration == 'public') {
          info = item.engaged_teams
        }
        return info
      },
      newGame () {
        this.form = Object.assign({}, this.defaultForm)
        this.form.event = this.latestEvent.id
        this.form.bouts = this.bouts.map(bout => { return bout.id })
        this.$refs.form?.resetValidation()
        this.newDlg = true
      },
      updateMyGame(game) {
        this.defaultIndex = this.myOwnGames.indexOf(game)
        this.form = Object.assign({}, game)
        this.$refs.form?.resetValidation()
        this.newDlg = true
      },
      async createGame () {
        await this.confirmAction(this._createGame)
      },
      async _createGame () {
        this.loading = true
        try {
          const payload = {
            ...this.form,
          }
          const { data } = await main.createGame(payload)
          this.game_id = data.game.id
          this.myOwnGames.push(data.game)
          this.snackbar = {
            ...data,
            status: 'success',
            snack: true
          }
        } catch (e) {
          this.snackbar = {
            message: e.response.data.message,
            status: 'warning',
            snack: true
          }
        } finally {
          this.loading = false
          this.$store.commit('snackbar/setSnack', this.snackbar)
        }
      },
      async updateGame() {
        await this.confirmAction(this._updateGame)
      },
      async _updateGame() {
        this.loading = true
        try {
          const { data } = await main.updateGame(this.form)
          this.myOwnGames.splice(this.defaultIndex, 1, this.form)
          this.snackbar = {
            ...data,
            status: 'success',
            snack: true
          }
        } catch (e) {
          this.snackbar = {
            message: e.response.data.message,
            status: 'warning',
            snack: true
          }
        }
        this.loading = false
        this.$store.commit('snackbar/setSnack', this.snackbar)
      },
      async confirmAction(callback, param) {
        await this.$dialog.confirm({
          text: 'Are you sure?',
          title: 'Warning',
          actions: {
            false: 'No',
            true: {
              color: 'red',
              text: 'Yes',
              handle: () => {
                if (callback) {
                  callback(param)
                }
              }
            }
          }
        })
      },
      genGameLink (game_id) {
        let link = `${process.env.VUE_APP_URL}/contest`
        if (game_id) {
          link += `/${game_id}`
        }
        return link
      },
      copyGameLink (queryId) {
        let testingCodeToCopy = document.querySelector(queryId)
        testingCodeToCopy.setAttribute('type', 'text')
        testingCodeToCopy.select()

        try {
          var successful = document.execCommand('copy')
          this.snackbar.message = successful ? 'Copied' : 'Cannot copy';
          this.snackbar.status = successful ? 'success' : 'warning';
        } catch (err) {
          this.snackbar.message = 'Oops, unable to copy';
        }

        /* unselect the range */
        testingCodeToCopy.setAttribute('type', 'hidden')
        window.getSelection().removeAllRanges()
        this.$store.commit('snackbar/setSnack', this.snackbar)
      },
      async loadMyGames () {
        this.loading = true
        this.myOwnGames = []
        this.newGameDlg = true
        try {
          const { data } = await main.loadMyGames()
          this.myOwnGames = data.my_own_games
        } catch(e) {
          this.snackbar = {
            snack: true,
            message: e.response.data.message,
            status: 'warning'
          }
          this.$store.commit('snackbar/setSnack', this.snackbar)
        }
        this.loading = false
      },
      async deleteMyGame (game_id) {
        await this.confirmAction(this._deleteMyGame, game_id)
      },
      async _deleteMyGame(game_id) {
        this.loading = true
        try {
          const { data } = await main.deleteGame(game_id)
          this.myOwnGames.forEach((game, i) => {
            if (game.id == game_id) {
              this.myOwnGames.splice(i, 1)
            }
          })
          this.snackbar = {
            snack: true,
            message: data.message,
            status: 'success'
          }
        } catch(e) {
          this.snackbar = {
            snack: true,
            message: e.response.data.message,
            status: 'warning'
          }
        }
        this.$store.commit('snackbar/setSnack', this.snackbar)
        this.loading = false
      },
      remove (item) {
        this.form.bouts.map((bout, i) => {
          if (bout == item.id) {
            this.form.bouts.splice(i, 1)
          }
        })
      },
    }
  }
</script>
<style>
  .lobby-table .v-data-table__wrapper td {
    cursor: pointer;
  }
</style>