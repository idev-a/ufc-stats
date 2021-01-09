<template>
  <v-container
    id="contest"
    fluid
    tag="section"
    class="d-flex justify-center"
  >
    <v-card
      class="mt-0"
      :class="{'max-60': !$vuetify.breakpoint.mobile}"
    >
      <v-card-title 
        class="justify-center font-weight-medium mb-md-3 mt-5"
      >
        <div class="text-center">
          <div>{{ this.event.name }}</div>
          <div class="subtitle-2">{{ this.event.date | beautifyDate }}</div>
        </div>
      </v-card-title>
      <v-card-text>
        <v-tabs
          align-with-title
          v-model="tab"
          background-color="transparent"
          color="basil"
        >
          <v-tabs-slider color="black"></v-tabs-slider>

          <v-tab
          >
            Fights
          </v-tab>
          <v-tab
          >
            Entries
          </v-tab>
        </v-tabs>
        <v-tabs-items
          v-model="tab"
        >
          <!-- fight/bout view -->
          <v-tab-item>
            <v-card
              min-width="50%"
              flat
              class="mt-0"
            >
              <v-card-title
              >
                <v-text-field
                  v-model="boutSearch"
                  append-icon="mdi-magnify"
                  label="Search"
                  clearable
                  class="mb-5"
                  single-line
                  hide-details
                ></v-text-field>
                <v-spacer />
              </v-card-title>
              <v-card-text>
                <v-data-table
                  :items="boutViews"
                  :loading="loading"
                  :headers="boutHeaders"
                  fixed-header
                  item-key="id"
                  height="280px"
                  dense
                  fixed-header
                  :disable-pagination="true"
                  hide-default-footer
                  :search="boutSearch"
                > 
                  <template #item.fighter1="{item}">
                    <v-chip 
                      small
                      :class="{'winner': item.fighter1 == item.winner, 'loser': item.fighter1 == item.loser}"
                    >
                      <b>{{item.fighter1}}</b>
                    </v-chip>
                  </template>
                  <template v-slot:item.entries_1="{ item }">
                    <a v-if="item.entries_1.length" href="#" @click="gotoEntry(item, item.entries_1)">{{ item.entries_1.length }}</a>
                    <span v-else>{{item.entries_1.length}}</span>
                  </template>
                  <template #item.fighter2="{item}">
                    <v-chip 
                      small
                      :class="{'winner': item.fighter2 == item.winner, 'loser': item.fighter2 == item.loser}"
                    >
                      <b>{{item.fighter2}}</b>
                    </v-chip>
                  </template>
                  <template v-slot:item.entries_2="{ item }">
                    <a v-if="item.entries_2.length" href="#" @click="gotoEntry(item, item.entries_2)">{{ item.entries_2.length }}</a>
                    <span v-else>{{ item.entries_2.length }}</span>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-tab-item>

          <!-- Entry view -->
          <v-tab-item>
            <v-card
              min-width="50%"
              flat
              class="mt-0"
            >
              <v-card-title
              >
                <v-text-field
                  v-model="entryViewSearch"
                  append-icon="mdi-magnify"
                  label="Search"
                  clearable
                  class="mb-5"
                  single-line
                  hide-details
                ></v-text-field>
                <v-spacer />
              </v-card-title>
              <v-card-text>
                <v-data-table
                  :items="entryViews"
                  :loading="loading"
                  :headers="entryViewHeaders"
                  fixed-header
                  :disable-pagination="true"
                  item-key="id"
                  dense
                  height="280px"
                  fixed-header
                  hide-default-footer
                  :search="entryViewSearch"
                  :item-class="entryItemClass"
                > 
                  <template v-slot:item.rank="{ item }">
                    <span :class="highlight(item)" class="font-weight-bold">{{item.rank}}</span>
                  </template>
                  <template v-slot:item.entry="{ item }">
                    <span :class="highlight(item)" class="font-weight-bold">{{item.entry}}</span>
                  </template>
                  <template v-slot:item.survived="{ item }">
                    <span :class="highlight(item)" class="font-weight-bold">{{item.survived}}</span>
                  </template>
                  <template v-slot:item.wins="{ item }">
                    <span :class="highlight(item)" class="font-weight-bold">{{item.wins}}</span>
                  </template>
                  <template v-slot:item.losses="{ item }">
                    <span :class="highlight(item)" class="font-weight-bold">{{item.losses}}</span>
                  </template>
                  <template v-slot:item.remainings="{ item }">
                    <span :class="highlight(item)" class="font-weight-bold">{{item.remainings}}</span>
                  </template>
                  <template v-slot:item.fighters="{ item }">
                    <div class="d-flex flex-wrap">
                      <template v-for="fighter in item.fighters">
                        <v-tooltip bottom>
                          <template v-slot:activator="{ on, attrs }">
                            <v-chip 
                              v-bind="attrs"
                              v-on="on"
                              small
                              class="mr-1 mb-1" 
                              :class="{'winner': fighter.win, 'loser': fighter.lose, 'died': fighter.died}" >
                              <span>{{fighter.name}}</span>
                            </v-chip>
                          </template>
                          <span>{{ fighter.entry_cnt }}</span>
                        </v-tooltip>
                      </template>
                    </div>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </v-card-text>
    </v-card>

    <!-- Entry dlg -->
    <v-dialog
      v-model="entryDlg"
      max-width="680"
    >
      <v-card
        color="basil"
        flat
      >
        <v-card-title
        >
          {{curBout}}
        </v-card-title>
        <v-card-text>
          <div class="d-flex">
            <v-text-field
              v-model="entrySearch"
              append-icon="mdi-magnify"
              label="Search"
              clearable
              class="mb-5"
              single-line
              hide-details
            ></v-text-field>
            <v-spacer />
          </div>
          <v-data-table
            :items="entries"
            :loading="loading"
            :headers="entryHeaders"
            :items-per-page="5"
            fixed-header
            item-key="id"
            :search="entrySearch"
          > 
          </v-data-table>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
  import main from '@/api/main'
  import { beautifyDate } from '@/util'

  export default {
    name: 'Contest',

    data () {
      return {
        loading: false,
        contests: [],
        event: '',
        boutSearch: '',
        entrySearch: '',
        tab: null,
        boutHeaders: [
          {
            text: 'Fighter1',
            value: 'fighter1',
            align: 'center'
          },
          {
            text: 'Entries',
            value: 'entries_1',
            align: 'center'
          },
          {
            text: 'Fighter2',
            value: 'fighter2',
            align: 'center'
          },
          {
            text: 'Entries',
            value: 'entries_2',
            align: 'center'
          },
          {
            text: 'Method',
            value: 'method',
            align: 'center'
          },
          {
            text: 'Round',
            value: 'round',
            align: 'center'
          },
          {
            text: 'Time',
            value: 'time',
            align: 'center'
          },
        ],
        boutViews: [],
        entryDlg: false,
        curBout: '',
        entries: [],
        entrySearch: '',
        entryHeaders: [
          {
            text: 'Event',
            value: 'event',
            align: 'center'
          },
          {
            text: 'User',
            value: 'user',
            align: 'center'
          },
        ],
        entryViewSearch: '',
        entryViews: [],
        entryViewHeaders: [
          {
            text: 'Rank',
            value: 'rank',
            align: 'center',
          },
          {
            text: 'Entry',
            value: 'entry',
            align: 'center'
          },
          {
            text: 'Survived',
            value: 'survived',
            align: 'center'
          },
          {
            text: 'Wins',
            value: 'wins',
            align: 'center'
          },
          {
            text: 'Losses',
            value: 'losses',
            align: 'center'
          },
          {
            text: 'Remainings',
            value: 'remainings',
            align: 'center'
          },
          {
            text: 'Fighters',
            value: 'fighters',
            align: 'center'
          },
        ]
      }
    },

    filters: {
      beautifyDate,
    },

    mounted() {
      this.getLatestContest()
    },

    methods: {
      highlight(item) {
        return {'highlight--text': item.rank==1}
      },
      async getLatestContest() {
        this.loading = true
        const { data } = await main.getLatestContest()
        this.boutViews = data.bout_views
        this.entryViews = data.entry_views
        this.event = data.event
        this.loading = false
      },
      async gotoEntry (item, entries) {
        this.entryDlg = true
        this.curBout = `${item.fighter1} vs. ${item.fighter2}`
        const {data} = await main.getEntries(entries)
        this.entries = data.entries
      },
      entryItemClass (item) {
        return item.died.length ? 'strike-through' : ''
      }
    }
  }
</script>

<style>
  .contest-item {
    width: 110px;
    height: 38px;
    border: 1px solid;
    border-radius: 10px;
    line-height: 17px;
    margin: 0 .5rem 0 0;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
  }

  table { border-collapse: collapse; empty-cells: show; }

  td { position: relative; }

  tr.strike-through td:before {
    content: " ";
    position: absolute;
    top: 50%;
    left: 0;
    border-bottom: 1px solid #B71C1C;
    width: 100%;
  }

  tr.strike-through td:after {
    content: "\00B7";
    font-size: 1px;
  }


  .v-chip__content {
    font-size: 12px;
    font-weight: 400;
  }

  .max-60 {
    max-width: 60%;
  }

</style>