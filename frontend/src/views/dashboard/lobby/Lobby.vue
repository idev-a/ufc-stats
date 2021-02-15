<template>
  <div id="contest-table">
    <v-card
      max-width="100%"
      class="ma-0 pa-0 pb-3 fq-popup"
      :class="{'y-scroll': !$vuetify.breakpoint.mobile}"
    >
      <v-card-title 
        class="font-weight-medium mb-md-3"
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
            label="Type"
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
          <template v-slot:item.event="{ item }">
            <span>{{ item.event.name }}</span>
          </template>
          <template v-slot:item.entrants="{ item }">
            <span>{{ item.entrants.length }}</span>
          </template>
          <template v-slot:item.date_started="{ item }">
            <span>{{ item.date_started | beautifyDateTimeMin }}</span>
          </template>
          <template v-slot:item.actions="{ item }">
            <v-tooltip right>
              <template  v-slot:activator="{ on }">
                <div v-on="on">
                  <v-btn 
                    class="my-1" 
                    :disabled="!canJoin(item)" 
                    @click.stop="joinContest(item)"
                  >
                    Join
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
        <v-card-title>
          <v-list three-line style="background: none;">
            <v-list-item
            >
              <v-list-item-avatar>
                <v-img :src="gameAvatar"></v-img>
              </v-list-item-avatar>

              <v-list-item-content class="text-left">
                <v-list-item-title class="display-2" v-html="curGame.event.name"></v-list-item-title>
                <v-list-item-subtitle><b>Start at</b> {{ curGame.date_started | beautifyDateTimeMin }}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-tooltip left>
                  <template  v-slot:activator="{ on }">
                    <div v-on="on">
                      <v-btn 
                        class="my-1" 
                        :disabled="!canJoin(curGame)" 
                        @click.stop="joinContest(curGame)"
                      >
                        Join
                      </v-btn>
                    </div>
                  </template>
                  <span>{{ JoinBtnTooltip(curGame) }}</span>
                </v-tooltip>
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
              <contest-detail :game="curGame"/>
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
  import main from '@/api/main'
  import { beautifyDateTimeMin } from '@/util'
  import ContestDetail from './ContestDetail'
  import Rules from './Rules'

  export default {
    name: 'Contest',

    components: { ContestDetail, Rules },

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
        headers: [
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
          {
            text: 'Entrants',
            value: 'entrants',
            align: 'center',
          },
          {
            text: 'When',
            value: 'date_started',
            align: 'center',
          },
          {
            text: '',
            value: 'actions',
            align:'center'
          }
        ],
        tabs: [
          'Contest Details',
          'Rules & Scoring',
        ]
      }
    },

    computed: {
      ...mapState('auth', ['authUser']),
      filteredGames() {
        const temp = []
        this.games.map(game => {
          if (this.type == 'all') {
            temp.push(game)
          } else if (game.type_of_registration == this.type) {
            temp.push(game)
          } 
        })
        return temp
      },
      gameAvatar () {
        return require('@/assets/logo.jpg')
      }
    },

    filters: {
      beautifyDateTimeMin
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
        const myId = this.authUser.id || this.authUser.pk
        let isInvolved = false
        item.entrants.map(user => {
          if (user.id == myId) {
            isInvolved = true
          }
        })
        let isStarted = this.$moment(item.date_started).isBefore(this.$moment())
        if (isStarted) {
          return false
        }
        if (item.type_of_registration == 'public') {
          return true
        } else if (item.type_of_registration == 'private' && isInvolved) {
          return true
        }

        return false
      },
      JoinBtnTooltip(item) {
        if (!this.canJoin(item)) {
          return "Can't Join"
        }
        return 'Join'
      },
      joinContest (item) {

      }
    }
  }
</script>
<style>
  .lobby-table .v-data-table__wrapper td{
    cursor: pointer;
  }
</style>