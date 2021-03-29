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
            <money :curContest="curContest" />
          </div>
          <div class="subtitle-1">
            {{ contestDate }}
            <span v-if="eventStarted" class="red--text h6">({{curContest.action}})</span>
          </div>
        </div>
        <v-col cols="auto" class="py-0">
          <v-autocomplete 
            :loading="loading"
            v-model="curGame"
            :items="games"
            chips
            item-value="value"
            item-text="name"
            label="Select Entry"
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
              <fight-tab :boutViews="boutViews" :loading="loading"/>
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
  </div>
</template>

<script>
  import main from '@/api/main'
  import { beautifyDate } from '@/util'
  import FightTab from './FightTab'
  import StandingTab from './StandingTab'
  import Money from '../selection/Money'
  import Chat from './Chat'
  import { mapState } from 'vuex'

  export default {
    name: 'Contest',

    components: { 
      FightTab,
      StandingTab,
      Chat,
      Money
    },

    props: ['game_id'],

    data () {
      return {
        loading: false,
        tab: 'standings',
        boutViews: [],
        entryViews: [],
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
            icon: 'mdi-message'
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

      contestName () {
        return this.curContest && this.curContest.name || ""
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
      contestDate () {
        return this.curContest && beautifyDate(this.curContest.date) || ""
      },
      eventStarted () {
        return this.curContest && this.curContest.action != ''
      },
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
      async changeGame (item) {
        this.$router.push({'path': `/contest/${item}`})
        // this.loading = true
        // await this.getLatestContest(item)
        // this.loading = false
      },
    }
  }
</script>
