<template>
  <v-container
    id="contest"
    fluid
    tag="section"
    class="d-flex justify-center"
  >
    <dialog-drag 
      id="movingContestDlg"
      @drag-end="dragEnd"
      :options="{
        buttonClose: false,
        left: lastLeft,
        dragCursor: 'move',
        zIndex: 5,
      }"
    >
      <v-card
        class="ma-0 pa-0"
        :class="{'max-60': !$vuetify.breakpoint.mobile}"
      >
        <v-card-title 
          class="justify-center font-weight-medium mb-md-3"
        >
          <div class="text-center">
            <div>{{ this.event.name }}</div>
            <div class="subtitle-1">{{ this.event.date | beautifyDate }}</div>
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
                    disable-pagination
                    hide-default-footer
                    :search="boutSearch"
                  > 
                    <template #item.fighter1="{item}">
                      <win-chip 
                        :isWinner="item.fighter1 == item.winner"
                        :isLoser="item.fighter1 == item.loser"
                        :isDied="item.died && item.died == item.fighter1"
                        :fighter="item.fighter1"
                        >
                      </win-chip>
                    </template>
                    <template v-slot:item.entries_1="{ item }">
                      <a v-if="item.entries_1.length" href="#" @click="gotoEntry(item, item.entries_1)">{{ item.entries_1.length }}</a>
                      <span v-else>{{item.entries_1.length}}</span>
                    </template>
                    <template #item.fighter2="{item}">
                      <win-chip 
                        :isWinner="item.fighter2 == item.winner"
                        :isLoser="item.fighter2 == item.loser"
                        :isDied="item.died && item.died == item.fighter2"
                        :fighter="item.fighter2"
                        >
                      </win-chip>
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
                      <span :class="highlight(item)" class="font-weight-bold">{{item.rank}}
                      </span>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-icon v-bind="attrs" v-on="on" v-if="isMine(item)">mdi-account-tie</v-icon>
                        </template>
                        <span>My Entry</span>
                      </v-tooltip>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-icon v-bind="attrs" v-on="on" v-if="isDied(item)">mdi-skull-outline</v-icon>
                          </template>
                        <span>Dead</span>
                      </v-tooltip>
                    </template>
                    <template v-slot:item.entry="{ item }">
                      <span :class="highlight(item)" class="font-weight-bold">{{item.entry}}
                      </span>
                    </template>
                    <template v-slot:item.survived="{ item }">
                      <span :class="highlight(item)" class="font-weight-bold">{{item.survived}}
                      </span>
                    </template>
                    <template v-slot:item.wins="{ item }">
                      <span :class="highlight(item)" class="font-weight-bold">{{item.wins}}
                      </span>
                    </template>
                    <template v-slot:item.losses="{ item }">
                      <span :class="highlight(item)" class="font-weight-bold">{{item.losses}}
                      </span>
                    </template>
                    <template v-slot:item.remainings="{ item }">
                      <span :class="highlight(item)" class="font-weight-bold">{{item.remainings}}
                      </span>
                    </template>
                    <template v-slot:item.fighters="{ item }">
                      <div class="d-flex flex-wrap">
                        <template v-for="fighter in item.fighters">
                          <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                              <win-chip 
                                :isWinner="fighter.win"
                                :isLoser="fighter.lose"
                                :isDied="fighter.died"
                                :fighter="fighter.name"
                                v-bind="attrs"
                                v-on="on"
                                class="mr-1 mb-1"
                                >
                              </win-chip>
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
    </dialog-drag>

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
          class="display-2 font-weight-medium"
        >
          Contest Users
        </v-card-title>
        <div class="text-center subtitle-1">{{curBout}}</div>
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
            disable-pagination
            hide-default-header
            hide-default-footer
          > 
            <template v-slot:item.users="{ item }">
              <v-chip class="mr-1 mb-1 body-1" v-for="user in item.users">{{ user }}</v-chip>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
  import main from '@/api/main'
  import { beautifyDate } from '@/util'
  import WinChip from './WinChip'
  import { mapState } from 'vuex'
  import DialogDrag from 'vue-dialog-drag'

  export default {
    name: 'Contest',

    components: { WinChip, DialogDrag },

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
          },
          {
            text: 'Entries',
            value: 'entries_1',
            align: 'center'
          },
          {
            text: 'Fighter2',
            value: 'fighter2',
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
            text: 'Users',
            value: 'users',
            sortable: false,
            class: 'survivor-header'
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
            align: 'center',
          },
        ]
      }
    },

    filters: {
      beautifyDate,
    },

    computed: {
      ...mapState(['lastLeft']),
      ...mapState('auth', ['authUser'])
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
        const users = []
        entries.map(entry => { users.push(entry[1])})
        this.entries = [{users}]
      },
      entryItemClass (item) {
        return item.died.length ? 'strike-through' : ''
      },
      isDied (item) {
        let died = false
        item.fighters.map(fighter => {
          if (fighter.died) {
            died = true
          }
        })
        return died
      },
      isMine (item) {
        return item.entry.split('-')[0] == this.authUser.displayname
      },
      dragEnd (val) {
        this.$store.commit('SET_LASTLEFT', val.left)
      }
    }
  }
</script>

<style lang="scss">
  #contest {
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