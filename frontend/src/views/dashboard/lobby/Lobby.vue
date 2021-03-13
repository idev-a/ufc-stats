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
        <div class="d-flex align-center">
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search games"
            clearable
            class="mb-5"
            single-line
            hide-details
          ></v-text-field>
          <v-spacer />
          <v-select
            v-model="type"
            class="ml-2"
            :items="types"
            hint="Public / Private"
            persistent-hint
            label="Type"
          >
          </v-select>
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
          <template v-slot:item.date="{ item }">
            <span>{{ item.date | beautifyDateTimeMin }}</span>
          </template>
          <!-- :disabled="canJoin(item) != 'ok'"  -->
          <template v-slot:item.actions="{ item }">
            <v-tooltip right>
              <template  v-slot:activator="{ on }">
                <div v-on="on">
                  <v-btn 
                    fab
                    x-small
                    class="my-1" 
                    :class="{'success': joinLabel(item).includes('JOIN'), 'red lighten-1': joinLabel(curGame) == 'LIVE'}"
                    :disabled="canJoin(item) == 'No enough coins'" 
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
                <v-list-item-title class="display-2" v-html="curGame.event.name"></v-list-item-title>
                <v-list-item-subtitle><b>Start at</b> {{ curGame.date | beautifyDateTimeMin }}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <div class="d-md-flex">
                  <v-tooltip left>
                    <template  v-slot:activator="{ on }">
                      <div v-on="on">
                        <v-btn 
                          small
                          class="my-1 mr-md-2" 
                          :class="{'red lighten-1': joinLabel(curGame) == 'LIVE'}"
                          :disabled="canJoin(curGame) == 'No enough coins'" 
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
                          v-if="joinLabel(curGame) != 'LIVE'"
                          class="my-1 red lighten-1" 
                          :disabled="canJoin(curGame) == 'No enough coins'" 
                          @click.stop="gotoContest"
                        >
                          Live
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
            slider-color="red lighten-1"
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
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import upperFirst from 'lodash/upperFirst'

  import main from '@/api/main'
  import { beautifyDateTimeMin } from '@/util'
  import GameDetail from './GameDetail'
  import Rules from './Rules'

  export default {
    name: 'Contest',

    components: { GameDetail, Rules },

    data () {
      return {
        loading: false,
        search: '',
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
            align:'center'
          },
          {
            text: 'Name',
            value: 'name',
            align: 'center',
          },
          {
            text: 'Event',
            value: 'event',
            align: 'center',
          },
          {
            text: 'Type',
            value: 'type_of_registration',
            align: 'center',
          },
          // {
          //   text: 'Genre',
          //   value: 'genre',
          //   align: 'center',
          // },
          {
            text: 'Buyin',
            value: 'buyin',
            align: 'center',
          },
          // {
          //   text: 'Bonus',
          //   value: 'buyin_bonus',
          //   align: 'center',
          // },
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
            text: 'When',
            value: 'date',
            align: 'center',
            width: '100'
          },
         
        ],
        tabs: [
          'Contest Details',
          'Rules & Scoring',
        ]
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
        return this.authUser && (this.authUser.id || this.authUser.pk)
      },
      myCoins () {
        return this.authUser && (this.authUser.coins || this.authUser.fq_points || this.profile.user.coins)
      }
    },

    filters: {
      beautifyDateTimeMin,
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
        this.loading = false
      },
      async loadGameDetail (item) {
        this.curGame = item
        this.dlg = true
      },
      canJoin (item) {
        if (this.hasJoined(item)) {
          return 'Already Joined'
        }
        let isInvolved = false
        item.entrants && item.entrants.map(user => {
          if (user.id == this.myId) {
            isInvolved = true
          }
        })
        let isStarted = this.$moment(item.date).isBefore(this.$moment())
        if (isStarted) {
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
        const label = this.joinLabel(item)
        if (label.includes('JOIN')) {
          tooltip = 'Go to Selection'
        } else if (label == 'EDIT') {
          tooltip = 'Go to Selection'
        } else if (label == 'LIVE') {
          tooltip = 'Go to Contest'
        } 
        return tooltip
      },
      hasJoined(item) {
        let joined = false
        item.joined_users != null && item.joined_users.map(user => {
          if (user.id == this.myId) {
            joined = true
          }
        })
        return joined
      },
      hasEnoughCoins(item) {
        return this.myCoins >= item.buyin
      },
      joinLabel (item) {
        let label = 'JOIN'
        if (this.hasJoined(item)) {
          label = 'EDIT'
        } else {
          if (item.genre != 'free') {
            label += ` | F${item.buyin}`
          }
        }
        if (item.id == -1) {
          label = 'EDIT'
        }
        let isStarted = this.$moment(item.date).isBefore(this.$moment())
        if (isStarted && label == 'EDIT') {
          label = 'LIVE'
        }
        return label
      },
      gotoContest () {
        this.$router.push({ name: 'Contest', query: {tab: 'standings'}})
      },
      async joinContest (item) {
        const label = this.joinLabel(item)
        if (label == 'LIVE') {
          return this.$router.push({ name: 'Contest', query: {tab: 'standings'}})
        }
        if (label == 'EDIT') {
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
      }
    }
  }
</script>
<style>
  .lobby-table .v-data-table__wrapper td {
    cursor: pointer;
  }
</style>