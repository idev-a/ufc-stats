<template>
  <div
    id="contest-table"
  >
    <v-card
      min-width="50%"
      flat
      class="mt-0"
    >
      <v-card-title class="mb-2">
        <v-text-field
          v-model="search"
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
          :items="views"
          :loading="loading"
          :headers="headers"
          :search="search"
          fixed-header
          :disable-pagination="true"
          item-key="id"
          dense
          height="280px"
          hide-default-footer
          mobile-breakpoint="0"
        > 
          <template v-slot:header.first_place="{ header }">
            <v-icon color="gold">mdi-trophy-outline</v-icon>
          </template>
          <template v-slot:header.second_place="{ header }">
            <v-icon color="silver">mdi-trophy-outline</v-icon>
          </template>
          <template v-slot:header.third_place="{ header }">
            <v-icon color="bronze">mdi-trophy-outline</v-icon>
          </template>

          <template v-slot:item.ranking="{ item }">
            <span :class="highlight(item)">{{item.ranking}}
            </span>
          </template>
          <template v-slot:item.user="{ item }">
            <div
              class="d-flex align-center"
            >
              <v-avatar
                color="brown"
                size="34"
              >
                <v-img 
                  v-if="item.avatar"
                  :src="avatar(item)"
                />
                <span 
                  v-else
                  class="white--text initials"
                >
                  {{ item.initials }}
                </span>
              </v-avatar>
              <div
                class="text-left ml-2"
                style="margin: .2rem 0;"
              >
                <div :class="highlight(item)" class="username" v-html="item.displayname"></div>
                <div :class="highlight(item)" class="subtitle" v-html="item.username"></div>
              </div>
            </div>
          </template>
          <template v-slot:item.first_place="{ item }">
            <span :class="highlight(item)">{{item.first_place}}
            </span>
          </template>
          <template v-slot:item.second_place="{ item }">
            <span :class="highlight(item)">{{item.second_place}}
            </span>
          </template>
          <template v-slot:item.third_place="{ item }">
            <span :class="highlight(item)">{{item.third_place}}
            </span>
          </template>
          <template v-slot:item.fq_points="{ item }">
            <span :class="highlight(item)">{{item.fq_points}}
            </span>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </div>
</template>
<script>
  import main from '@/api/main'
  import { mapState } from 'vuex'

  export default {
    name: 'OverallBoard',

    data () {
      return {
        loading: false,
        search: '',
        views: [],
        headers: [
          {
            text: 'Position',
            value: 'ranking',
            align: 'center'
          },
          {
            text: 'Player',
            value: 'user',
            align: 'center'
          },
          {
            text: '1st Place',
            value: 'first_place',
          },
          {
            text: '2st Place',
            value: 'second_place',
          },
          {
            text: '3rd Place',
            value: 'third_place',
          },
          {
            text: 'Points',
            value: 'fq_points',
          }
        ]
      }
    },

    mounted() {
      this.getLeaderboard()
    },

    methods: {
      async getLeaderboard() {
        this.loading = true
        const { data } = await main.getLeaderboard()
        this.views = data.views
        this.loading = false
      },
      highlight(item) {
        return {'highlight--text font-weight-medium': item.ranking==1}
      },
      avatar(item) {
        return item.avatar ? avatar : 'https://picsum.photos/id/11/500/300'
      }
    }
  }
</script>

<style>
  .username {
    font-size: 15px;
    font-weight: 300;
  }

  .initials {
    font-size: 20px;
    font-weight: 400;
    line-height: 2rem;
    letter-spacing: normal !important;
    font-family: "Roboto", sans-serif !important;
  }

  .subtitle {
    font-size: 12px;
    color: #afafaf;
  }
</style>