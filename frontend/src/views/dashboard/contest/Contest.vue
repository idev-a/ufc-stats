<template>
  <div id="contest">
    <v-card
      max-width="100%"
      class="ma-0 pa-0 pb-3"
      :class="{'max-60': !$vuetify.breakpoint.mobile}"
    >
      
        <v-card-title 
          class="justify-center font-weight-medium mb-md-3"
        >
          <div class="text-center">
            <div>{{ event.name }}</div>
            <div class="subtitle-1">
              {{ event.date | beautifyDate }}
              <span v-if="eventStarted" class="red--text h6">({{(event.action || 'started').toUpperCase()}})</span>
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

            <!-- Chat -->
            <v-tab-item>
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

    data () {
      return {
        loading: false,
        tab: null,
        boutViews: [],
        entryViews: [],
        tabs: [
          'Fights',
          'Standings',
          'Chat'
        ]
      }
    },

    filters: {
      beautifyDate
    },

    computed: {
      ...mapState(['event']),

      eventStarted () {
        return this.event && this.event.action != ''
      },
    },

    mounted() {
      this.getLatestContest()
    },

    methods: {
      async getLatestContest() {
        this.loading = true
        const { data } = await main.getLatestContest()
        this.boutViews = data.bout_views
        this.entryViews = data.entry_views
        this.$store.commit('SET_EVENT', data.event)
        this.loading = false
      },
    }
  }
</script>

<style lang="scss">
  #contest {
    backdrop-filter: blur(30px) contrast(1.0);

    * {
      background-color: transparent;
    }

    .v-data-table { 
      overflow-x: auto !important;

      tr:hover {
        background: url('../../../assets/bg.jpg');
        background-size: cover;
        background-attachment: fixed;
        backdrop-filter: blur(40px);
      }

      thead > tr > th {
        background-color: #808080db;
        backdrop-filter: blur(40px);
      }
    }

    table { border-collapse: collapse; empty-cells: show; }

    td { position: relative; }

    tr.strike-through td {
      background-color: #B71C1C;
      opacity: 0.9;
      color: #EEEEEE;
      
      &:first-child {
        border-top-left-radius: 6px;
        border-bottom-left-radius: 6px;
      }
      
      &:last-child {
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
      }
    }
    .v-application .survivor-header {
      text-align: center !important;
    }

    .v-chip__content {
      font-size: 12px;
      font-weight: 400;
    }

    .max-60 {
      max-width: 800px;
    }
  }
</style>