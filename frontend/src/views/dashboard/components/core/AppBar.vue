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
          @click.stop="showInstruction"
        >
          <v-icon color="white">mdi-information-outline</v-icon>
        </v-btn>
        </template>
      <span>Instructions</span>
    </v-tooltip>

    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          v-on="on"
          min-width="0"
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
      transition="scale-transition"
    >
      <template v-slot:activator="{ attrs, on }">
        <v-btn
          min-width="0"
          text
          v-bind="attrs"
          v-on="on"
        >
          <v-icon color="white">mdi-account</v-icon>
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
  import Instruction from '../../component/Instruction'
  import UserProfile from '../../component/UserProfile'

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
      ...mapState(['drawer']),
      ...mapGetters('auth', ['isAuthenticated'])
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