<template>
  <div id="contest-table">
    <v-card
      max-width="100%"
      tile
      class="fq-popup ma-0 pa-0 pb-3"
      :class="{'y-scroll': !$vuetify.breakpoint.mobile}"
    >
      <v-card-title 
        v-if="curContest"
        class="font-weight-medium pt-3 mb-3 ml-md-5 justify-center"
      >
        <div class="text-center mr-10">
          <div>{{ contestName }}</div>
          <div class="subtitle-1">
            {{ contestDate }}
            <span v-if="eventStarted" class="red--text h6">({{curContest.action}})</span>
          </div>
        </div>
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

        </v-tabs-items>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
  import main from '@/api/main'
  import { beautifyDate } from '@/util'
  import FightTab from '../contest/FightTab'
  import StandingTab from '../contest/StandingTab'
  import { mapState } from 'vuex'

  export default {
    name: 'ContestDetail',

    components: { FightTab, StandingTab },

    props: ['entry_id'],

    data () {
      return {
        loading: false,
        tab: null,
        curContest: null,
        boutViews: [],
        entryViews: [],
        tabs: [
          'Fights',
          'Standings'
        ],
        games: [],
        curGame: -1,
      }
    },

    computed: {
      insideValue: {
        get() {
          return this.$store.getters['game/selectedContestId']
        },
        set (val) {
          this.$store.commit('game/setContestId', val);
        }
      },
      contestName () {
        return this.curContest.name
      },
      contestDate () {
        return beautifyDate(this.curContest.date)
      },
      eventStarted () {
        return this.curContest && this.curContest.action != ''
      },
    },

    mounted() {
      this.getContestHistoryDetail()
    },

    methods: {
      async getContestHistoryDetail() {
        this.loading = true
        try {
          const { data } = await main.getContestHistoryDetail(this.entry_id)
          this.boutViews = data.bout_views
          this.entryViews = data.entry_views
          this.curContest = data.event
        } catch (err) {
        }
        this.loading = false
      }
    }
  }
</script>
