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
      <span>Live Contest</span>
    </v-tooltip>
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          v-if="isAuthenticated"
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
          <app-bar-item
            v-if="!isAuthenticated"
          >
            <v-list-item-title 
              v-text="`Login`" 
              @click="goTo('Login')"
            />
          </app-bar-item>
          <app-bar-item
            v-else
          >
            <v-list-item-title 
              v-text="`Logout`" 
              @click="goTo('Logout')"
            />
          </app-bar-item>
        </div>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
  // Components
  import { VHover, VListItem } from 'vuetify/lib'

  // Utilities
  import { mapState, mapMutations, mapGetters } from 'vuex'

  export default {
    name: 'DashboardCoreAppBar',

    components: {
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
      notifications: [
        'Mike John Responded to your email',
        'You have 5 new tasks',
        'You\'re now friends with Andrew',
        'Another Notification',
        'Another one',
      ],
      profile: [
        // { title: 'Profile', name: 'My Profile' },
        // { title: 'Settings', name: 'Settings' },
        // { divider: true },
        { title: 'Log out', name: 'Login' },
      ],
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
      }
    },
  }
</script>
