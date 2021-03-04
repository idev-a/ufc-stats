<template>
  <v-dialog
    v-model="insideValue"
    width="600px"
  >
  <div id="contest-table">
    <v-sheet
      tile
      class="fq-popup pa-3"
      icon="mdi-account-outline"
      :loading="loading"
      id="profile-card"
    >
      <v-card-title>
        <div
          class="d-flex align-center w-100"
        >
          <v-avatar
            color="brown"
            size="84"
          >
            <v-img 
              v-if="userAvatar"
              :src="userAvatar"
            />
            <span 
              v-else
              class="white--text initials"
            >
              {{ userInitials }}
            </span>
            <!-- <v-icon
              class="lock-icon"
            > 
              mdi-lock
            </v-icon> -->
          </v-avatar>
          <div
            class="display-box"
          >
            <div class="displayname" v-html="userDisplayname"></div>
            <div class="subtitle">Member since {{ userJoinedDate }}</div>
          </div>
          <div
            class="d-flex align-baseline ml-auto ml-4"
          >
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon size=24 v-on="on" color="gold">mdi-crown-outline</v-icon>
              </template>
              <span>Total Wins</span>
            </v-tooltip>
            <span class="ml-1 display-1">{{profile.total_wins}}</span>
          </div>

          <div
            class="d-flex align-end ml-3"
            v-if="mine"
          >
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon size=26 color="gold">mdi-cash</v-icon>
              </template>
              <span>Coins</span>
            </v-tooltip>
            <span class="ml-1 display-1">{{profile.user.coins}}</span>
          </div>
        </div>
      </v-card-title>
      <v-card-text 
        class="profile-table"
      >
      <v-divider class="my-2"/>
          
        <div
          class="stats-title"
        >
          Overview
        </div>
        <div
          class="stats-blocks"
        > 
          <v-card
            class="well"
            :loading="loading"
          >
            <div
              class="stats-value"
            >
              {{profile.total_contests}}
            </div>
            <div>
              Total Contests
            </div>
          </v-card>
          <v-card
            class="well"
            :loading="loading"
          >
            <div
              class="stats-value"
            >
              {{profile.completed_contests}}
            </div>
            <div>
              Completed Contests
            </div>
          </v-card>
          <v-card
            class="well"
            :loading="loading"
          >
            <div
              class="stats-value"
            >
              {{profile.total_win_p}}
            </div>
            <div>
              Win Rate(%)
            </div>
          </v-card>
        </div>
        
        <div
          class="stats-title mt-5"
        >
          Contest History
        </div>
        <v-data-table
          :items="profile.contest_history"
          :loading="loading"
          :headers="headers"
          fixed-header
          item-key="id"
          dense
          item-class="contest-history-tb-row"
          @click:row="showHistory"
        > 
          <template v-slot:item.date="{ item }">
            {{ beautifyDate(item.date)}}
          </template>
          <template v-slot:item.status="{ item }">
            {{ item.status ? upperFirst(item.status) : '-' }}
          </template>
        </v-data-table>
      </v-card-text>
    </v-sheet>
  </div>
  </v-dialog>
</template>

<script>
  import { mapState } from 'vuex'
  import auth from '@/api/auth'
  import { beautifyDate } from '@/util'
  import upperFirst from 'lodash/upperFirst'

  export default {
    name: "UserProfile",

    data: () => ({
      valid: true,
      headers: [
        {
          text: 'Event',
          value: 'event'
        },
        {
          text: 'Started at',
          value: 'date'
        },
        {
          text: 'Status',
          value: 'status'
        },
        {
          text: 'Ranking',
          value: 'ranking'
        },
      ],
      rules: {
        required: v => {
          return !!v || 'This field is required.'
        },
      }
    }),

    computed: {
      ...mapState('auth', ['authUser', 'loading', 'profile']),
      insideValue: {
        get() {
          return this.$store.getters['auth/selectedUserId']
        },
        set (val) {
          this.$store.commit('auth/setUserId', val)
        }
      },
      userAvatar () {
        return this.profile.user && this.profile.user.avatar
      },
      userInitials () {
        return this.profile.user && this.profile.user.initials
      },
      userDisplayname () {
        return this.profile.user && this.profile.user.displayname || 'Unknown'
      },
      userJoinedDate () {
        return this.profile.user && this.beautifyDate(this.profile.user.date_joined)
      },
      mine () {
        return this.profile.user.id == (this.authUser.id || this.authUser.pk)
      }
    },

    methods: {
      beautifyDate,
      upperFirst,

      async updateProfile() {
        this.$store.dispatch('auth/updateUser', this.authUser)
      },
      showHistory (item) {
        this.$store.commit('auth/setUserId', 0)
        this.$router.push({path: `/history/contest/${item.event_id}/${item.game_id}`})
      }
    }
  }
</script>

<style lang="scss">
  
  .profile-table .v-data-table__wrapper td{
    cursor: pointer;
  }

  .display-box {
    text-align: left !important;
    margin: .5rem 0 0 1rem;
  }

  .displayname {
    font-size: 24px;
    font-weight: 500;
    text-transform: capitalize;
  }

  .subtitle {
    font-size: 14px;
    font-weight: 500;
  }

  .initials {
    font-size: 36px;
    font-weight: 400;
    line-height: 2rem;
    letter-spacing: normal !important;
    font-family: "Roboto", sans-serif !important;
  }

  .lock-icon {
    position: absolute;
    bottom: 0px;
    left: 0px;
    width: 100%;
  }

  .stats-blocks {
    display: flex;
    
    .well {
      padding: 19px 10px;
      font-size: 12px;
      text-align: center;
      background-color: #181818c0;
      height: 100%;
      border-radius: 3px;
      margin-right: 1.5rem;
      min-width: 100px;

      .stats-value {
        font-size: 18px;
        font-weight: 700;
      }
    }
  }

</style>
