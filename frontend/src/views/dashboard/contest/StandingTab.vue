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
      <v-data-table
        :items="entryViews"
        :loading="loading"
        :headers="entryViewHeaders"
        :search="entryViewSearch"
        fixed-header
        :disable-pagination="true"
        item-key="id"
        dense
        height="280px"
        hide-default-footer
        show-expand
        :expanded.sync="expanded"
        :item-class="entryItemClass"
        mobile-breakpoint="0"
       
      > 
        <template v-slot:item.ranking="{ item }">
          <span :class="highlight(item)" class="font-weight-bold">{{item.ranking}}
          </span>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-icon v-bind="attrs" v-on="on" v-if="isMine(item)">mdi-account-tie</v-icon>
            </template>
            <span>Me</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-icon v-bind="attrs" v-on="on" v-if="isDied(item)">mdi-skull-outline</v-icon>
              </template>
            <span>Dead</span>
          </v-tooltip>
        </template>
        <template v-slot:item.entry="{ item }">
          <v-chip  @click="showUserProfile(item)"><span :class="highlight(item)" class="font-weight-bold">{{item.entry}}
          </span></v-chip>
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
  </div>
</template>

<script>
  import WinChip from '../component/WinChip'
  import { mapState } from 'vuex'

  export default {
    name: 'Contest',

    components: { WinChip },

    props: ['entryViews', 'loading'],

    data () {
      return {
        curFighters: [],
        expanded: [],
        entryViewSearch: '',
        entryViewHeaders: [
          {
            text: 'Ranking',
            value: 'ranking',
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
            text: 'Quaked',
            value: 'died',
            align: 'center'
          },
          {
            text: 'Remainings',
            value: 'remainings',
            align: 'center'
          },
        ]
      }
    },

    computed: {
      ...mapState('auth', ['authUser']),

      fighterIcon () {
        return this.expanded.length == 0 ? 'mdi-account-multiple-plus' : 'mdi-account-multiple-minus'
      },
      fighterIconTooltip () {
        return this.expanded.length == 0 ? 'Show Fighters' : 'Hide Fighters'
      }
    },

    methods: {
      highlight(item) {
        return {'highlight--text': item.ranking==1}
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
        return item.entry == this.authUser.displayname
      },
      showFighters (item) {
        if (this.expanded.includes(item.ranking)) {
          const index = this.expanded.indexOf(item);
          this.expanded.splice(index, 1);
        } else {
          this.expanded = []
          this.expanded.push(item.ranking)
          this.curFighters = item.fighters
        }
      },
      showUserProfile (item) {
        this.$store.dispatch('auth/loadProfile', item.user_id)
        this.$store.commit('auth/showProfileDlg')
      }
    }
  }
</script>