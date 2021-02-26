<template>
  <div id="contest-table">
    <v-card
      max-width="100%"
      class="ma-0 pa-0 pb-3 fq-popup"
      :class="{'y-scroll': !$vuetify.breakpoint.mobile}"
    >
      <v-card-title 
        class="font-weight-medium mb-3 ml-md-5"
      >
        <div class="text-center mr-10">
          <div>{{ contestName }}</div>
          <div class="subtitle-1">
            {{ contestDate }}
            <span v-if="eventStarted" class="red--text h6">({{curContest.action}})</span>
          </div>
        </div>
        <v-autocomplete 
          v-if="!isHistory"
          :loading="loading"
          v-model="curGame"
          :items="games"
          chips
          label="Select Contest"
          class="mt-2 mr-4"
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
        <v-card-text
          class="w-100"
        >
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
            <!-- fight/bout view -->
            <v-tab-item>
              <fight-tab :boutViews="boutViews" :loading="loading"/>
            </v-tab-item>

            <!-- Entry view -->
            <v-tab-item>
              <standing-tab :entryViews="entryViews" :loading="loading"/>
            </v-tab-item>

            <!-- Chat -->
            <v-tab-item v-if="!isHistory">
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
  import Chat from './Chat'
  import { mapState } from 'vuex'

  export default {
    name: 'Contest',

    components: { FightTab, StandingTab, Chat },

    props: ['isHistory', 'entry_id'],

    data () {
      return {
        loading: false,
        tab: null,
        boutViews: [],
        entryViews: [],
        tabs: [
          'Fights',
          'Standings',
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
        return this.curContest.name
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
        console.log(contest.name)
        return contest
      },
      contestDate () {
        return beautifyDate(this.curContest.date)
      },
      eventStarted () {
        return this.curContest && this.curContest.action != ''
      },
    },

    mounted() {
      if (!this.isHistory) {
        this.getLatestContest()
        this.tabs.push('Chat')
      } else {
        this.getHistoryContest()
      }
    },

    methods: {
      async getHistoryContest() {
        this.loading = true
        const { data } = await main.getContestHistory(this.entry_id)
        this.boutViews = data.bout_views
        this.entryViews = data.entry_views
        this.loading = false
      },
      async getLatestContest(game_id=-1) {
        this.loading = true
        const { data } = await main.getLatestContest(game_id)
        this.boutViews = data.bout_views
        this.entryViews = data.entry_views
        this.games = data.games
        this.$store.commit('SET_EVENT', data.event)
        this.loading = false
      },
      async changeGame (item) {
        this.loading = true
        await this.getLatestContest(item)
        this.loading = false
      }
    }
  }
</script>
