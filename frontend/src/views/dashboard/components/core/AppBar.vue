<template>
  <v-app-bar
    id="app-bar"
    absolute
    app
    color="transparent"
    flat
    height="75"
  >
    <v-toolbar-title
      class="hidden-sm-and-down font-weight-medium white--text"
      v-text="$route.name"
    />

    <v-spacer />

    <div class="mx-3" />

    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          v-on="on"
          min-width="0"
          text
          style="padding: 10px 10px !important; margin: 0 1px;"
          @click.stop="showInstruction"
        >
          <v-icon color="white">mdi-information-outline</v-icon>
        </v-btn>
        </template>
      <span>Instructions</span>
    </v-tooltip>

    <!-- Notifications -->
    <v-menu
      bottom
      left
      offset-y
      origin="top right"
      transition="scale-transition"
    >
      <template v-slot:activator="{ attrs, on }">
        <v-btn
          min-width="0"
          text
          v-bind="attrs"
          v-on="on"
          style="padding: 10px 10px !important; margin: 0 1px;"
        >
          <v-badge
            color="red lighten-1"
            overlap
            left
            small
          >
            <template v-slot:badge>
              <span>{{ notificationLengh }}</span>
            </template>

            <v-icon color="white">mdi-bell</v-icon>
          </v-badge>
        </v-btn>
      </template>
      <v-list
        :tile="false"
        nav
        two-line
        dense
        min-height="50"
        min-width="350"
        light
        style="max-height: 300px"
        class="overflow-y-auto"
      >
        <v-list-item-group >
          <template v-for="(item, index) in notifications">
            <v-list-item :key="index" dense>
              <v-list-item-content>
                <!-- <v-list-item-title v-text="item.title"></v-list-item-title> -->
                <v-list-item-subtitle class="text--primary" v-text="item.msg"></v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-icon class="mb-2">mdi-clock</v-icon>
                <v-list-item-action-text v-text="item.time"></v-list-item-action-text>
              </v-list-item-action>
            </v-list-item>
          </template>
        </v-list-item-group>
      </v-list>
    </v-menu>

    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          v-on="on"
          min-width="0"
          style="padding: 10px 10px !important; margin: 0 1px;"
          text
          to="/"
        >
          <v-icon color="white">mdi-view-dashboard</v-icon>
        </v-btn>
        </template>
      <span>Selection</span>
    </v-tooltip>

    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          v-if="isAuthenticated"
          v-on="on"
          min-width="0"
          style="padding: 10px 10px !important; margin: 0 1px;"
          text
          to="/contest"
        >
          <v-icon color="white">mdi-lock-open-outline</v-icon>
        </v-btn>
      </template>
      <span>Contest</span>
    </v-tooltip>
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          v-if="isAuthenticated && false"
          v-on="on"
          min-width="0"
          style="padding: 10px 10px !important; margin: 0 1px;"
          text
          to="/score"
        >
          <v-icon color="white">mdi-application</v-icon>
        </v-btn>
      </template>
      <span>Live Score By User</span>
    </v-tooltip>

    <v-menu
      bottom
      left
      min-width="200"
      offset-y
      origin="top right"
      open-on-hover
      transition="scale-transition"
    >
      <template v-slot:activator="{ attrs, on }">
        <v-btn
          min-width="0"
          style="padding: 10px 10px !important; margin: 0 1px;"
          text
          v-bind="attrs"
          v-on="on"
        >
          <v-icon :left="isAuthenticated" color="white">mdi-account</v-icon>
          <span class="white--text" v-if="isAuthenticated && authUser">{{authUser.displayname}}</span>
        </v-btn>
      </template>

      <v-list
        :tile="false"
        flat
        nav
      >
        <div>
          <v-btn
            text
            v-if="!isAuthenticated"
            @click="launchLogin"
            block
            plain
          >
            Login
          </v-btn>
          <v-btn
            v-else
            text
            @click="logout"
            block
            plain
          >
            Logout
          </v-btn>
          <v-divider v-if="isAuthenticated" />
          <v-btn
            text
            v-if="isAuthenticated"
            @click="profileDlg=true"
            block
            plain
          >
            Profile
          </v-btn>
        </div>
      </v-list>
    </v-menu>

    <instruction :value.sync="instructionDlg" @update="instructionDlg=false" />
    <user-profile v-if="isAuthenticated" :value.sync="profileDlg" @update="profileDlg=false" />
  </v-app-bar>
</template>

<script>
  // Components
  import { VHover, VListItem } from 'vuetify/lib'

  // Utilities
  import { mapState, mapMutations, mapGetters } from 'vuex'
  import UserProfile from '../../pages/UserProfile'
  import Instruction from '../../instruction/Instruction'

  export default {
    name: 'DashboardCoreAppBar',

    components: {
      Instruction,
      UserProfile,
      AppBarItem: {
        render (h) {
          return h(VHover, {
            scopedSlots: {
              default: ({ hover }) => {
                return h(VListItem, {
                  attrs: this.$attrs,
                  class: {
                    'black--text': !hover,
                    'white--text secondary elevation-12': hover,
                  },
                  props: {
                    activeClass: '',
                    dark: hover,
                    link: true,
                    ...this.$attrs,
                  },
                }, this.$slots.default)
              },
            },
          })
        },
      },
    },

    props: {
      value: {
        type: Boolean,
        default: false,
      },
    },

    data: () => ({
      instructionDlg: false,
      profileDlg: false
    }),

    computed: {
      ...mapState(['drawer', 'notifications']),
      ...mapState('auth', ['authUser']),
      ...mapGetters('auth', ['isAuthenticated']),

      notificationLengh () {
        return this.notifications.length < 100 ? this.notifications.length : '99+'
      }
    },

    mounted() {
    },

    methods: {
      ...mapMutations({
        setDrawer: 'SET_DRAWER',
      }),

      goTo (name) {
        if (name === 'Logout') {
          window.location.href = '/pages/logout'
          return
        } 
        
        this.$router.push({ name })
      },
      launchLogin () {
        this.$store.commit('auth/showLoginDlg')
      },
      logout () {
        this.$store.dispatch('auth/logout')
      },
      showInstruction () {
        this.instructionDlg = true
      }
    },
  }
</script>

<style>
  .instruction-list {
    list-style: none;
  }
</style>