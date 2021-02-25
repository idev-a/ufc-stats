<template>
  <div>
    <div
      class="stats-title mt-4"
    >
      Instructions
    </div>
    <v-sheet
      class="pa-2"
      elevation="1"
      max-height="300"
      width="100%"
      style="overflow-y: auto"
    >
      <span v-html="game.instructions.replace(/\n/g, '<br/>')"></span>
    </v-sheet>

    <div
      class="d-flex align-center stats-title mt-4"
    >
      <div>Entrants</div>
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
    </div>
    <v-sheet
      class=" pa-2"
      elevation="1"
      width="100%"
    >
      <v-data-iterator
        :items="game.entrants"
        hide-default-footer
        hide-default-header
      >
        <template v-slot:default="props">
          <v-flex>
              <v-chip 
                v-for="item in props.items" 
                :key="item.id" 
                @click="showProfile(item)"
                class="mr-2"
              >
                {{ item.displayname }}
              </v-chip>
          </v-flex>
        </template>
      </v-data-iterator>
    </v-sheet>
  </div>
</template>
<script>
  export default {
    name: 'ContestDetail',

    props: ['game'],

    data () {
      return {
        search: ''
      }
    },

    methods: {
      showProfile(item) {
        this.$store.dispatch('auth/loadProfile', item.id)
      }
    }
  }
</script>