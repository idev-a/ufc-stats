<template>
  <div id="contest-table">
    <v-card
      tile
      max-width="100%"
      :loading="loading"
      style="min-height: calc(100vh - 140px)"
      class="mx-auto my-0 pa-0 pb-3 fq-popup"
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
              <div class="display-1" :class="{'red--text lighten-1 font-weight-bold': item.value == option}">
                {{item.label}}
              </div>
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
                <team-card 
                  :loading="loading"
                  :item="item"
                  :fighters="curData.fighters"
                />
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
  import TeamCard from "./TeamCard";

  export default {
    name: 'MyTeams',

    components: { TeamCard },

    data() {
      return  {
        loading: false,
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
        liveData: {},
        recentData: {},
      }
    },

    computed: {
      curData () {
        return this.option == 'live' ? this.liveData : this.recentData
      },
    },

    mounted () {
      this.getMyTeams()
    },

    methods: {
      async getMyTeams () {
        this.loading = true
        const  { data } = await main.getMyTeams()
        this.liveData = data.live_data
        this.recentData = data.recent_data
        this.fighters = data.fighters
        this.loading = false
      },
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