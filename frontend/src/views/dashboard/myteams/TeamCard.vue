<template>
  <v-card
    outlined
    :loading="loading"
    class="pa-2 mt-0"
  >
    <div class="font-weight-medium display-1 text-center pt-2 text-uppercase">{{contestName(oldItem.game)}}</div>
    <div class="subtitle-2 text-center">{{ oldItem.game.event.date | beautifyDateTimeMin }}
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
          <transition-group :duration="1000">
          <v-list-item
            v-for="(fighter, i) in oldItem.fighters"
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
              <v-btn @click="removeFighter(fighter, i)" small icon><v-icon color="red lighten-1">mdi-close</v-icon></v-btn>
            </v-list-item-icon>
          </v-list-item>
        </transition-group>
      </v-list-item-group>
    </v-list>
    <v-card-actions>
      <div class="red--text lighten-1 subtitle-2"><span>Total</span>&nbsp;{{oldItem.fighters.length}}</div>
      <v-spacer />
      <v-tooltip left>
        <template v-slot:activator="{ on }">
          <v-btn fab x-small class="mr-2" v-on="on"><v-icon color="gold">mdi-pencil-outline</v-icon></v-btn>
        </template>
        <span>Edit</span>
      </v-tooltip>
      <v-tooltip right>
        <template v-slot:activator="{ on }">
          <v-btn fab x-small class="mr-2" v-on="on" @click="addFighters"><v-icon color="gold">mdi-plus</v-icon></v-btn>
        </template>
        <span>Add Fighters</span>
      </v-tooltip>
      <v-tooltip right>
        <template v-slot:activator="{ on }">
          <v-btn fab x-small class="mr-2" v-on="on" @click="confirmTeam"><v-icon color="gold">mdi-send</v-icon></v-btn>
        </template>
        <span>Confirm</span>
      </v-tooltip>
      <v-tooltip right>
        <template v-slot:activator="{ on }">
          <v-btn fab x-small v-on="on" @click="refreshTeam"><v-icon color="gold">mdi-refresh</v-icon></v-btn>
        </template>
        <span>Refresh</span>
      </v-tooltip>
    </v-card-actions>
  </v-card>
</template>

<script>
  import { beautifyDateTimeMin } from '@/util'
  import Money from "../selection/Money";

  export default {
    name: 'TeamCard',

    props: ['loading', 'item', 'fighters'],

    data () {
      return {
        oldItem: JSON.parse(JSON.stringify(this.item))
      }
    },

    components: { Money },

    filters: { beautifyDateTimeMin },

    methods: {
      contestName(game) {
        let name = game.name
        if (game.retry_number) {
          name += ` (${game.retry_number})`
        }
        return name
      },
      async confirmTeam () {

      },
      refreshTeam () {
        this.oldItem = JSON.parse(JSON.stringify(this.item))
      },
      removeFighter (fighter, i) {
        this.oldItem.fighters.splice(i, 1)
      },
      addFighters () {

      }
    }
  }
</script>