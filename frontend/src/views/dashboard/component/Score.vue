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
        class="justify-center font-weight-medium mb-md-3"
      >
        Score By User
        <v-spacer />
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            clearable
            class="mb-5"
            single-line
            hide-details
          ></v-text-field>
      </v-card-title>
      <v-card-text>
        <v-data-table
          :items="scores"
          :loading="loading"
          :headers="headers"
          fixed-header
          :items-per-page="5"
          item-key="username"
          :search="search"
        > 
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
  import session from '@/api/session'

  export default {
    name: 'Contest',

    data () {
      return {
        loading: false,
        search: '',
        scores: [],
        headers: [
          {
            text: 'User',
            value: 'username',
            align: 'center'
          },
          {
            text: 'Surviving Fighters',
            value: 'surviving_fighters',
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
            text: 'Dead',
            value: 'dead',
            align: 'center'
          },
        ]
      }
    },

    mounted() {
      this.getScoresByUser()
    },

    methods: {
      async getScoresByUser() {
        this.loading = true
        const { data } = await session.get('api/entries/score_by_user')
        this.scores = data.scores
        this.loading = false
      }
    }
  }
</script>
