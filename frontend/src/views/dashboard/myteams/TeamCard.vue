<template>
  <div>
    <v-card
      outlined
      :loading="loading"
      class="pa-2 mt-0"
    >
      <div class="font-weight-medium display-1  text-center text-center mt-2 text-uppercase">
        <span>{{contestName(item.game)}}</span>
        <v-tooltip  top>
          <template v-slot:activator="{ on }">
            <v-btn v-if="false" fab x-small v-on="on" @click="unregister" class="ml-auto" ><v-icon color="warning">mdi-delete-outline</v-icon></v-btn>
          </template>
          <span>Unregister Entry</span>
        </v-tooltip>
      </div>
      <div class="subtitle-2 text-center">
        {{ item.game.event.date | beautifyDateTimeMin }}
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
              v-for="(id, i) in item.fighters"
              :key="i"
              dense
            >
              <v-list-item-avatar>
                {{i+1}}
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title v-text="_fighter(id).initials"></v-list-item-title>
              </v-list-item-content>
              <v-list-item-icon>
                {{_fighter(id).gender}}
              </v-list-item-icon>
              <v-list-item-icon>
                <v-btn @click="removeFighter(id, i)" small icon><v-icon color="warning">mdi-close</v-icon></v-btn>
              </v-list-item-icon>
            </v-list-item>
        </v-list-item-group>
      </v-list>
      <v-card-actions>
        <div class="warning--text subtitle-2"><span>Total</span>&nbsp;{{item.fighters.length}}</div>
        <v-spacer />
        <v-tooltip left>
          <template v-slot:activator="{ on }">
            <v-btn fab x-small disabled class="mr-2" v-on="on"><v-icon color="gold">mdi-pencil-outline</v-icon></v-btn>
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
            <v-btn fab x-small class="mr-2" v-on="on" :disabled="noChangeFighters" @click="confirmTeam"><v-icon color="success">mdi-database-outline</v-icon></v-btn>
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
    <v-dialog
      v-model="editDlg"
      @click:outside="closeDlg(item)"
    >
      <toggle-container
        :fighters="fighters"
        :bouts="item.bouts"
        @close="closeDlg(item)"
        @ok="okDlg"
      />
    </v-dialog>
  </div>
</template>

<script>
  import main from '@/api/main'
  import { beautifyDateTimeMin, equalsIgnoreOrder } from '@/util'
  import { mapState } from 'vuex'
  import Money from "../selection/Money";
  import ToggleContainer from "../selection/ToggleContainer";

  export default {
    name: 'TeamCard',

    props: ['loading', 'item', 'fighters', 'item_index'],

    data () {
      return {
        editDlg: false,
        oldItem: JSON.parse(JSON.stringify(this.item))
      }
    },

    components: { Money, ToggleContainer },

    filters: { 
      beautifyDateTimeMin
    },

    computed: {
      ...mapState('auth', ['authUser']),
      noChangeFighters () {

        return equalsIgnoreOrder(this.item.fighters, this.oldItem.fighters)
      }
    },

    methods: {
      _fighter (id) {
        const fighters = this.fighters.filter(fighter => fighter.id == id)
        return fighters[0] || {}
      },
      contestName(game) {
        let name = game.name
        if (game.entry_number) {
          name += ` (${game.entry_number})`
        }
        return name
      },
      async confirmAction(callback) {
        await this.$dialog.confirm({
          text: 'Are you sure?',
          title: 'Warning',
          actions: {
            false: 'No',
            true: {
              color: 'red',
              text: 'Yes',
              handle: () => {
                if (callback) {
                  callback()
                }
              }
            }
          }
        })
      },
      async confirmTeam () {
        await this.confirmAction(this._confirmTeam)
      },
      async _confirmTeam () {
        const payload = {
          entry: {
            game: this.item.game.id,
            event: this.item.game.event.id,
            user: this.authUser.pk || this.authUser.id,
            entry_number: this.item.game.entry_number
          },
          selections: []
        }
        this.item.bouts.forEach(bout => {
          payload.selections.push({
            bout: bout.id,
            survivor1: bout.survivors?.[0] || null,
            survivor2: bout.survivors?.[1] || null,
          })
        })

        this.$emit('updateLoading', true)
        const { data } = await main.createEntries(payload)
        this.snackbar = {
          ...data,
          snack: true
        }
        this.$emit('updateLoading', false)
        this.$store.commit('snackbar/setSnack', this.snackbar)

        if (data.status == 'success'){
          this.$emit('updateTeams', this.item, this.item_index)
          this.oldItem = JSON.parse(JSON.stringify(this.item))
        }
      },
      refreshTeam () {
        this.item.fighters = JSON.parse(JSON.stringify(this.oldItem.fighters))
        this.item.bouts = JSON.parse(JSON.stringify(this.oldItem.bouts))
      },
      removeFighter (id, i) {
        this.item.fighters.splice(i, 1)
        this.item.bouts.forEach(bout => {
          const index = bout.survivors.indexOf(id)
          if (index > -1) {
            bout.survivors.splice(bout.survivors.indexOf(id), 1)
          }
        })
      },
      addFighters () {
        this.editDlg = true
      },
      closeDlg (item) {
        item.bouts.forEach(bout => {
          bout.survivors = bout.contests_orig
        })
        this.editDlg = false
      },
      okDlg () {
        this.editDlg = false
        this.item.bouts.forEach(bout => {
          if (bout.survivors.length == 1) {
            if (!this.item.fighters.includes(bout.survivors[0])) {
              this.item.fighters.push(bout.survivors[0])
            }
          }
          if (bout.survivors.length == 2) {
            if (!this.item.fighters.includes(bout.survivors[1])) {
              this.item.fighters.push(bout.survivors[1])
            }
          }
        })
      },
      async unregister () {
        await this.confirmAction(this._unregister)
      },
      async _unregister () {

      }
    }
  }
</script>

<style>
/* Enter and leave animations can use different */
/* durations and timing functions.              */
.slide-fade-enter-active {
  transition: all .3s ease;
}
.slide-fade-leave-active {
  transition: all .8s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
  transform: translateX(10px);
  opacity: 0;
}
</style>