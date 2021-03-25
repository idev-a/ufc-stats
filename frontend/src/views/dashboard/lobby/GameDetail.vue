<template>
  <div>
    <div
      class="stats-title mt-4"
    >
      Summary
    </div>
    <v-card
      tile
      max-height="300"
      width="100%"
      class="mt-4"
      style="overflow-y: auto"
    >
      <v-card-text>
        <span>{{summary}}</span>
        <!-- <ul class="instruction-list">
          <li v-for="(ins, x) in instructions">{{x+1}}. {{ins}}</li>
        </ul> -->
      </v-card-text>
    </v-card>

    <div
      class="d-flex align-center stats-title mt-6"
    >
      <div>Entrants</div>
      <v-spacer />
      <v-text-field
        v-if="game.entrants"
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        clearable
        class="mb-5"
        single-line
        hide-details
      ></v-text-field>
    </div>
    <v-card
      tile
      class="mt-4"
    >
      <v-card-text
        tile
        v-if="game.joined_users"
        width="100%"
      >
        <v-data-iterator
          :items="game.joined_users"
          hide-default-footer
          hide-default-header
        >
          <template v-slot:default="props">
            <v-flex>
                <v-chip 
                  v-for="item in props.items" 
                  :key="item.id" 
                  @click="showProfile(item)"
                  class="mr-2 mb-1"
                >
                  {{ item.displayname }}
                </v-chip>
            </v-flex>
          </template>
        </v-data-iterator>
      </v-card-text>
      <v-card-text
        v-else
      >
        This is default contest.
      </v-card-text>
    </v-card>
  </div>
</template>
<script>
  import { DEFAULT_INSTRUCTIONS, DEFAULT_SUMMARY } from '@/constants/constant'

  export default {
    name: 'GameDetail',

    props: ['game'],

    data () {
      return {
        search: ''
      }
    },

    computed: {
      instructions () {
        return this.game.instructions && this.game.instructions.split('\n') || DEFAULT_INSTRUCTIONS
      },
      summary () {
        return this.game.summary || DEFAULT_SUMMARY
      }
    },

    methods: {
      showProfile(item) {
        this.$store.dispatch('auth/loadProfile', item.id)
        this.$store.commit('auth/showProfileDlg')
      }
    }
  }
</script>