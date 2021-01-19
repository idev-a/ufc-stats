<template>
  <div>
    <v-card
      class="ma-0 pa-0"
      :class="{'max-60': !$vuetify.breakpoint.mobile}"
    >
      <v-card-title 
        class="justify-center font-weight-medium mb-md-3"
      >
        <div class="text-center">
          <div>{{ this.event.name }}</div>
          <div class="subtitle-1">
            {{ this.event.date | beautifyDate }}
            <span v-if="eventStarted" class="red--text h6">(Started)</span>
          </div>
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
              <div class="mb-2">
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
              </div>
              <v-data-table
                :items="boutViews"
                :loading="loading"
                :headers="boutHeaders"
                fixed-header
                item-key="id"
                :height="`${$vuetify.breakpoint.mobile ? 'calc(100vh - 200px)': '280px'}`"
                dense
                fixed-header
                disable-pagination
                hide-default-footer
                :search="boutSearch"
              > 
                <template #item.fighter1="{item}">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <win-chip 
                        :isWinner="item.fighter1 == item.winner"
                        :isLoser="item.fighter1 == item.loser"
                        :isDied="item.died && item.died == item.fighter1"
                        :fighter="item.fighter1"
                        v-bind="attrs"
                        v-on="on"
                        >
                      </win-chip>
                      </template>
                    <span>{{ fighterTooltip(item.fighter1, item) }}</span>
                  </v-tooltip>
                </template>
                <template v-slot:item.entries_1="{ item }">
                  <a v-if="item.entries_1.length" href="#" @click="gotoEntry(item, item.entries_1, item.fighter1)">{{ item.entries_1.length }}</a>
                  <span v-else>{{item.entries_1.length}}</span>
                </template>
                <template #item.fighter2="{item}">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <win-chip 
                        :isWinner="item.fighter2 == item.winner"
                        :isLoser="item.fighter2 == item.loser"
                        :isDied="item.died && item.died == item.fighter2"
                        :fighter="item.fighter2"
                        v-bind="attrs"
                        v-on="on"
                        >
                      </win-chip>
                    </template>
                    <span>{{ fighterTooltip(item.fighter2, item) }}</span>
                  </v-tooltip>
                </template>
                <template v-slot:item.entries_2="{ item }">
                  <a v-if="item.entries_2.length" href="#" @click="gotoEntry(item, item.entries_2, item.fighter2)">{{ item.entries_2.length }}</a>
                  <span v-else>{{ item.entries_2.length }}</span>
                </template>

                <template v-slot:item.round="{ item }">
                  <span>{{item.round == 0 ? '' : item.round}}
                  </span>
                </template>
              </v-data-table>
            </v-card>
          </v-tab-item>

          <!-- Entry view -->
          <v-tab-item>
            <v-card
              min-width="50%"
              flat
              class="mt-0"
            >
              <div class="mb-2">
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
              </div>
              <v-data-table
                :items="entryViews"
                :loading="loading"
                :headers="entryViewHeaders"
                :search="entryViewSearch"
                fixed-header
                :disable-pagination="true"
                item-key="id"
                dense
                :height="`${$vuetify.breakpoint.mobile ? 'calc(100vh - 200px)': '280px'}`"
                hide-default-footer
                show-expand
                :expanded.sync="expanded"
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
                <!-- <template v-slot:item.losses="{ item }">
                  <span :class="highlight(item)" class="font-weight-bold">{{item.losses}}
                  </span>
                </template> -->
                <template v-slot:item.died="{ item }">
                  <span :class="highlight(item)" class="font-weight-bold">{{item.died.length}}
                  </span>
                </template>
                <template v-slot:item.remainings="{ item }">
                  <span :class="highlight(item)" class="font-weight-bold">{{item.remainings}}
                  </span>
                </template>
                <template v-slot:item.fighters="{ item }">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on }">
                      <v-btn 
                        text 
                        icon 
                        v-on="on"
                        @click.stop="showFighters(item)"
                      >
                        <v-icon>{{ fighterIcon }}</v-icon>
                      </v-btn>
                    </template>
                    <span>{{ fighterIconTooltip }}</span>
                  </v-tooltip>
                </template>
                <template v-slot:item.data-table-expand="{ item, isExpanded, expand }">
                  <v-tooltip v-if="isExpanded" bottom>
                    <template v-slot:activator="{ on }">
                      <v-btn v-on="on" icon text @click="expand(false)" >
                        <v-icon>mdi-account-multiple-minus</v-icon>
                      </v-btn>
                    </template>
                    <span>Hide Fighters</span>
                  </v-tooltip>
                  <v-tooltip v-else bottom>
                    <template v-slot:activator="{ on }">
                      <v-btn v-on="on" icon text @click="expand(true)">
                        <v-icon>mdi-account-multiple-plus</v-icon>
                      </v-btn>
                    </template>
                    <span>Show Fighters</span>
                  </v-tooltip>
                </template>
                <template v-slot:expanded-item="{ headers, item }">
                  <td :colspan="headers.length">
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
                  </td>
                </template>
              </v-data-table>
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
          class="display-2 font-weight-medium"
        >
          Contest Users for <span class="red--text lighten-1">{{curBout.fighter}}</span>
        </v-card-title>
        <div class="text-center subtitle-1">({{curBout.name}})</div>
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
  </div>
</template>

<script>
  import main from '@/api/main'
  import { beautifyDate } from '@/util'
  import WinChip from '../component/WinChip'
  import { mapState } from 'vuex'

  export default {
    name: 'Contest',

    components: { WinChip },

    data () {
      return {
        loading: false,
        contests: [],
        event: '',
        boutSearch: '',
        entrySearch: '',
        tab: null,
        curFighters: [],
        expanded: [],
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
        curBout: {
          name: '',
          fighter: ''
        },
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
          // {
          //   text: 'Losses',
          //   value: 'losses',
          //   align: 'center'
          // },
          {
            text: 'Quaked',
            value: 'died',
            align: 'center'
          },
          {
            text: 'Remainings',
            value: 'remainings',
            align: 'center'
          },
          // {
          //   text: 'Fighters',
          //   value: 'fighters',
          //   align: 'center',
          // },
        ]
      }
    },

    filters: {
      beautifyDate,
    },

    computed: {
      ...mapState('auth', ['authUser']),

      eventStarted () {
        return this.event && this.event.action == 'started'
      },
      fighterIcon () {
        return this.expanded.length == 0 ? 'mdi-account-multiple-plus' : 'mdi-account-multiple-minus'
      },
      fighterIconTooltip () {
        return this.expanded.length == 0 ? 'Show Fighters' : 'Hide Fighters'
      }
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
      async gotoEntry (item, entries, fighter) {
        this.entryDlg = true
        this.curBout = {
          name: `${item.fighter1} vs. ${item.fighter2}`,
          fighter
        }
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
      fighterTooltip (fighter, item) {
        let text = 'Not started yet'
        if (fighter == item.winner) {
          text = 'Winner'
        }
        if (fighter == item.loser) {
          text = 'Loser'
        }
        if (item.died && item.died == fighter) {
          text = 'Not survived'
        }
        return text
      },

      showFighters (item) {
        if (this.expanded.includes(item.rank)) {
          const index = this.expanded.indexOf(item);
          this.expanded.splice(index, 1);
        } else {
          this.expanded = []
          this.expanded.push(item.rank)
          this.curFighters = item.fighters
        }
      }
    }
  }
</script>

<style lang="scss">
  #contest {
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