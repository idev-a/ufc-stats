<template>
  <v-dialog
    v-model="insideValue"
    width="600px"
  >
    <v-card
      class="fq-popup"
      icon="mdi-account-outline"
      :loading="loading"
      id="profile-card"
    >
      <v-card-title>
        <div
          class="d-flex align-center"
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
        </div>
      </v-card-title>
      <v-card-text 
      >
        <v-divider />
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
              Contests
            </div>
          </v-card>
          <v-card
            class="well"
            :loading="loading"
          >
            <div
              class="stats-value"
            >
              {{profile.total_wins}}
            </div>
            <div>
              Win Rate %
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
        > 
          <template v-slot:item.date="{ item }">
            {{ beautifyDate(item.date)}}
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
  import { mapState } from 'vuex'
  import auth from '@/api/auth'
  import { beautifyDate } from '@/util'

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
          text: 'Date',
          value: 'date'
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
          this.$store.commit('auth/setUserId', val);
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
      }
    },

    methods: {
      beautifyDate,
      async updateProfile() {
        this.$store.dispatch('auth/updateUser', this.authUser)
      }
    }
  }
</script>

<style lang="scss" scoped>

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
      background-color: #181818;
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