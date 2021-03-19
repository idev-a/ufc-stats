<template>
  <div id="contest-table">
    <v-card
      tile
      max-width="100%"
      style="min-height: calc(100vh - 140px)"
      class="ma-0 pa-0 pb-3 fq-popup"
      :class="{'y-scroll': !$vuetify.breakpoint.mobile}"
    >
      <v-card-title 
        class="font-weight-medium"
      >
        <div v-if="$vuetify.breakpoint.mobile" class="mr-5">My Teams</div>
        <v-radio-group
          v-model="option"
          row
        >
          <v-radio
            color="red--text lighten-1"
            v-for="item in options"
            :value="item.value"
            :key="item.value"
          >
            <template v-slot:label>
              <div class="display-1" :class="{'red--text lighten-1 font-weight-bold': item.value == option}">{{item.label}}</div>
           
            </template>
          </v-radio>
        </v-radio-group>
      </v-card-title>

      <v-card-text
        v-if="curData.teams"
      >
        <v-data-iterator
          :items="curData.teams"
          item-key="key"
          :items-per-page="4"
          hide-default-footer
          hide-default-header
        >
          <template v-slot:default="{ items, isExpanded, expand }">
            <v-row>
              <v-col
                v-for="item in items"
                :key="item.id"
                cols="12"
                sm="4"
                md="3"
                lg="3"
              >
                <v-card
                  outlined
                  class="pa-2 mt-0"
                >
                  <div class="font-weight-medium display-1 text-center pt-2 text-uppercase">{{contestName(item.game)}}</div>
                  <div class="subtitle-2 text-center">{{ item.game.event.date | beautifyDateTimeMin }}
                    <money  />
                  </div>

                  <v-list 
                    dense
                    class="team-list"
                   
                  >
                    <v-list-item
                      class="border item-header"
                      color="darken-4"
                      :input-value="true"
                      dense
                      inactive
                      disabled
                    >
                      <v-list-item-avatar>
                        No.
                      </v-list-item-avatar>
                      <v-list-item-content>
                        <span>Name</span>
                      </v-list-item-content>
                      <v-list-item-icon>
                        Gender
                      </v-list-item-icon>
                      <v-list-item-icon></v-list-item-icon>
                    </v-list-item>
                    <v-list-item-group 
                      style="overflow-y: auto; height: 250px;"
                      dense>
                      <v-list-item
                        v-for="(fighter, i) in item.fighters"
                        :key="i"
                        dense
                      >
                        <v-list-item-avatar>
                          {{i+1}}
                        </v-list-item-avatar>
                        <v-list-item-content>
                          <v-list-item-title v-text="fighter.initials"></v-list-item-title>
                        </v-list-item-content>
                        <v-list-item-icon>
                          {{fighter.gender}}
                        </v-list-item-icon>
                        <v-list-item-icon>
                          <v-btn small icon><v-icon color="red lighten-1">mdi-close</v-icon></v-btn>
                        </v-list-item-icon>
                      </v-list-item>
                    </v-list-item-group>
                  </v-list>
                  <v-card-actions>
                    <div class="red--text lighten-1 subtitle-2"><span>Total</span>&nbsp;{{item.fighters.length}}</div>
                    <v-spacer />
                    <v-tooltip left>
                      <template v-slot:activator="{ on }">
                        <v-btn fab x-small class="mr-2" v-on="on"><v-icon color="gold">mdi-pencil-outline</v-icon></v-btn>
                      </template>
                      <span>Edit</span>
                    </v-tooltip>
                    <v-tooltip right>
                      <template v-slot:activator="{ on }">
                        <v-btn fab x-small class="mr-2" v-on="on"><v-icon color="gold">mdi-plus</v-icon></v-btn>
                      </template>
                      <span>Add Fighters</span>
                    </v-tooltip>
                    <v-tooltip right>
                      <template v-slot:activator="{ on }">
                        <v-btn fab x-small v-on="on" to="/contest"><v-icon color="gold">mdi-send</v-icon></v-btn>
                      </template>
                      <span>Go to Contest</span>
                    </v-tooltip>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </template>
        </v-data-iterator>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
  import main from '@/api/main'
  import { beautifyDateTimeMin, genderIcon } from '@/util'

  import Money from "../selection/Money";
  export default {
    name: 'MyTeams',

    components: { Money },

    data() {
      return  {
        option: 'live',
        options: [
          {
            label: 'Live',
            value: 'live'
          },
          {
            label: 'Recent',
            value: 'recent'
          }
        ],
        fighters: [],
        liveData: {},
        recentData: {},
      }
    },

    computed: {
      curData () {
        return this.option == 'live' ? this.liveData : this.recentData
      },
    },

    filters: { beautifyDateTimeMin },

    mounted () {
      this.getMyTeams()
    },

    methods: {
      genderIcon,

      contestName(game) {
        let name = game.name
        if (game.retry_number) {
          name += ` (${game.retry_number})`
        }
        return name
      },
      async getMyTeams () {
        this.loading = true
        const  { data } = await main.getMyTeams()
        this.liveData = data.live_data
        this.recentData = data.recent_data
        this.loading = false
      }
    }
  }
</script>

<style lang="scss">
  .team-list {
    .v-list-item {
      height: 30px !important;
      padding: 0 !important;
    }

    .v-list-item:nth-of-type(odd)::before {
      opacity: 0.08;
    }

    .item-header {
      background: #121212dd;
      -webkit-box-shadow: 0px 1px 1px 0px #000000e8;
      box-shadow: 0px 1px 1px 0px #000000e8;
    }

    .v-list-item__icon {
      margin: 0 !important;
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
      -ms-flex-item-align: center;
      align-self: center;
      height: inherit;
    }
  }
</style>