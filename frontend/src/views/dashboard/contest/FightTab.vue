<template>
	<div>
		<v-card
      min-width="50%"
      tile
      class="mt-0"
      style="background: none;"
    >
      <v-card-title class="mb-2">
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
      <!-- </v-img> -->
      <v-data-table
        :items="boutViews"
        :loading="loading"
        :headers="boutHeaders"
        item-key="id"
        height="280px"
        dense
        fixed-header
        disable-pagination
        hide-default-footer
        :search="boutSearch"
        mobile-breakpoint="0"
        :custom-sort="customSort"
      > 
        <template #item.fighter1="{item}">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <win-chip 
                :isWinner="item.fighter1 == item.winner"
                :isLoser="item.fighter1 == item.loser"
                :isDied="item.died && item.died == item.fighter1"
                :fighter="item.fighter1"
                :isDrawn="item.draw"
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
                :isDrawn="item.draw"
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
              <template v-for="user in item.users">
                <v-chip class="mr-1 mb-1 body-1" :key="user.id" :color="{'highlight': diedUsers.includes(user)}" >{{ user }}</v-chip>
              </template>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>
    </v-dialog>
	</div>
</template>
<script>
  import WinChip from '../component/WinChip'

  export default {
    name: 'Contest',

    components: { WinChip },

    props: ['boutViews', 'diedUsers', 'loading'],

    data () {
      return {
        contests: [],
        boutSearch: '',
        entryDlg: false,
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
      }
    },
    methods: {
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
        if (item.draw) {
          text = 'Drawn'
        }
        if (item.method == 'CNC') {
          text = 'No Contest Codes'
        }
        return text
      },
      customSort(items, index, isDesc) {
        items.sort((a, b) => {
          if (isDesc != "false") {
            if (index == "entries_1" || index == "entries_2") {
              return a[index].length < b[index].length ? -1 : 1
            } else {
              return a[index] < b[index] ? -1 : 1
            }
          } else {
            if (index == "entries_1" || index == "entries_2") {
              return b[index].length < a[index].length ? -1 : 1
            } else {
              return b[index] < a[index] ? -1 : 1
            }
          }
        })
        return items
      }
    }
  }
</script>