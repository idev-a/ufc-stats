<template>
  <div id="contest-table">
    <v-card
      min-width="100%"
      tile
      class="my-0 fq-popup"
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
      <v-card-text
        class="w-100 history-table"
      >
        <v-data-table
          :items="games"
          :loading="loading"
          :headers="headers"
          item-key="id"
          height="280px"
          dense
          fixed-header
          disable-pagination
          hide-default-footer
          :search="search"
          mobile-breakpoint="0"
          @click:row="showDetail"
        > 
          <template v-slot:item.date="{ item }">
            {{ beautifyDate(item.date)}}
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
  import main from '@/api/main'
  import { beautifyDate } from '@/util'

  export default {
    name: 'ContestHistory',

    data: () => ({
      search: '',
      loading: false,
      games: [],
      headers: [
        {
          text: 'Contest Name',
          value: 'name'
        },
        {
          text: 'Started',
          value: 'date'
        },
        {
          text: 'Ranking',
          value: 'ranking'
        }
      ]
    }),

    mounted() {
      this.getMyContestHistory()
    },

    methods: {
      beautifyDate,
      async getMyContestHistory() {
        this.loading = true
        const { data } = await main.getMyContestHistory()
        this.games = data.games
        this.loading = false
      },
      showDetail (item) {
        this.$router.push({path: `/history/contest/${item.id}`})
      }
    }
  }
</script>
<style>
  .history-table .v-data-table__wrapper td{
    cursor: pointer;
  }
</style>