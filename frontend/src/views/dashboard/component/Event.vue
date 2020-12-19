<template>
  <v-container
    id="event"
    fluid
    tag="section"
  >
    <v-card
    >
      <v-card-title
      >
        Events & Fights
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
        <v-spacer></v-spacer>
      </v-card-title>
      <v-card-text>
        <v-data-table
          :items="items"
          :loading="loading"
          :headers="headers"
          fixed-header
          :items-per-page="page"
          item-key="id"
          :search="search"
          @click:row="moveTo"
        > 
          <template v-slot:item.date="{ item }">
            <span>{{ beautifyDate(item.date) }}</span>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
  import { Post, Get } from '@/api'
  import { beautifyDate } from '@/util'
  import { mapState } from 'vuex'

  export default {
    name: 'Event',
    data () {
      return {
        loading: false,
        snackbar: false,
        message: '',
        color: 'success',
        search: '',
        items: [],
        headers: [
          {
            text: 'NAME',
            value: 'name'
          },
          {
            text: 'Date',
            value: 'date'
          },
          {
            text: 'Location',
            value: 'location'
          },
        ]
      }
    },
    mounted () {
      this.readEvents()
    },
    computed: {
      ...mapState(['page']),
    },
    methods: {
      beautifyDate,
      async readEvents () {
        const res = await Get('events')
        this.items = res.results
      },
      moveTo(item) {
        this.$router.push({'path': `contest/${item.id}`})
      }
    },
  }
</script>

<style lang="scss">
  #event table {
    thead th {
      background: #242b31;
      font-family: 'Robotobold', Arial, sans-serif;
      text-transform: uppercase;
      line-height: 10px;
      font-size: 14px;
      color: white;
    }

    tbody tr {
      cursor: pointer;
    }
  }
</style>