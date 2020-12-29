<template>
  <v-container
    id="contest"
    fluid
    tag="section"
    class="d-flex justify-center"
  >
    <v-card
      :loading="loading"
      min-width="60%"
      class="px-5"
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
          grow
        >
          <!-- <v-tabs-slider color="yellow"></v-tabs-slider> -->

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
          <v-tab-item
            >
            <v-card
              color="basil"
              flat
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
                  :items="bouts"
                  :loading="loading"
                  :headers="boutHeaders"
                  :items-per-page="5"
                  fixed-header
                  item-key="id"
                  :search="boutSearch"
                > 
                  <template #item.fighter1="{item}">
                    <div 
                      class="contest-item"
                      :class="{'winner-item': item.fighter1 == item.winner, 'loser-item': item.fighter1 == item.loser}"
                    >
                      <b>{{item.fighter1}}</b>
                    </div>
                  </template>
                  <template v-slot:item.entries_1="{ item }">
                    <span><a href="#" @click="gotoEntry(item, item.entries_1)">{{ item.entries_1.length }}</a></span>
                  </template>
                  <template #item.fighter2="{item}">
                    <div 
                      class="contest-item"
                      :class="{'winner-item': item.fighter2 == item.winner, 'loser-item': item.fighter2 == item.loser}"
                    >
                      <b>{{item.fighter2}}</b>
                    </div>
                  </template>
                  <template v-slot:item.entries_2="{ item }">
                    <a v-if="item.entries_2.length" href="" @click="gotoEntry(item, item.entries_2)">{{ item.entries_2.length }}</a>
                    <span v-else>{{ item.entries_2.length }}</span>
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
            value: 'fighter1'
          },
          {
            text: 'Entries',
            value: 'entries_1'
          },
          {
            text: 'Fighter2',
            value: 'fighter2'
          },
          {
            text: 'Entries',
            value: 'entries_2'
          },
          {
            text: 'Method',
            value: 'method'
          },
          {
            text: 'Round',
            value: 'round'
          },
          {
            text: 'Time',
            value: 'time'
          },
        ],
        bouts: [],
        entryDlg: false,
        curBout: '',
        entries: [],
        entrySearch: '',
        entryHeaders: [
          {
            text: 'Event',
            value: 'event'
          },
          {
            text: 'User',
            value: 'user'
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
      async getLatestContest() {
        this.loading = true
        const { data } = await main.getLatestContests()
        this.bouts = data.bouts
        this.event = data.event
        this.loading = false
      },
      async gotoEntry (item, entries) {
        this.entryDlg = true
        this.curBout = `${item.fighter1} vs. ${item.fighter2}`
        const {data} = await main.getEntries(entries)
        this.entries = data.entries
      }
    }
  }
</script>

<style>
  .contest-row {
    display: flex;

    justify-content:space-around;
    margin-bottom: 1.5rem;
    border-radius: 5px;
  }

  .row-inactive {
    background-color: #ECEFF1 !important;
  }

  .contest-item {
    width: 10rem;
    height: 80px;
    border: 1px solid;
    border-radius: 5px;
    margin: 0 .5rem 0 0;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
  }

  .winner-item {
    background-color: #4CAF50;
  }

  .loser-item {
    background-color: #FF5722;
  }

  .contest-column {
    display: flex;
    flex-basis: 100%;
    flex: 1;
  }

  .contest-user {
    font-size: 14px;
    color: #BDBDBD;
    margin-bottom: .5rem;
  }

  .is-active {
    color: #212121;
  }
</style>