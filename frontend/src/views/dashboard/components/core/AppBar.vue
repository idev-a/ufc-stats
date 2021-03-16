<template>
  <v-app-bar
    id="app-bar"
    absolute
    app
    color="transparent"
    flat
    height="75"
  >
    <v-btn
      v-if="$vuetify.breakpoint.smAndDown"
      class="mr-3"
      elevation="1"
      fab
      small
      @click="$vuetify.breakpoint.smAndDown ? setDrawer(!drawer) : $emit('input', !value)"
    >
      <v-icon v-if="value">
        mdi-view-quilt
      </v-icon>

      <v-icon v-else>
        mdi-dots-vertical
      </v-icon>
    </v-btn>

    <v-toolbar-title
      class="hidden-sm-and-down font-weight-medium white--text"
      v-text="$route.name"
    />

    <v-spacer />

    <div class="mx-3" />

    <template v-for="top in tops">
      <v-tooltip bottom z-index=100>
        <template v-slot:activator="{ on }">
          <v-btn
            v-if="$vuetify.breakpoint.smAndUp"
            v-on="on"
            min-width="0"
            class="fq-btn top-btn"
            exact-active-class="fq-btn-active"
            text
            :to="top.to"
          >
            {{top.name}}
          </v-btn>
        </template>
        <span>{{top.name}}</span>
      </v-tooltip>
    </template>

    <v-tooltip bottom z-index=100>
      <template v-slot:activator="{ on }">
        <v-btn
          v-on="on"
          min-width="0"
          text
          class="fq-btn top-btn"
          exact-active-class="fq-btn-active"
          @click.stop="showInstruction"
        >
          Instructions
        </v-btn>
        </template>
      <span>Instructions</span>
    </v-tooltip>

    <v-menu
      bottom
      left
      min-width="200"
      offset-y
      origin="top right"
      open-on-hover
      transition="scale-transition"
      z-index=100
    >
      <template v-slot:activator="{ attrs, on }">
        <v-btn
          min-width="0"
          class="fq-btn top-btn"
          exact-active-class="fq-btn-active"
          text
          v-bind="attrs"
          v-on="on"
        >
          <v-icon :left="isAuthenticated" color="white">mdi-account</v-icon>
          <span class="white--text" v-if="isAuthenticated && authUser">{{ authBtnLabel }} | <span class="gold--text lighten-1 font-weight-bold">{{myMoney}}</span></span>
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
            v-if="isAuthenticated"
            @click="showProfileDlg"
            class="fq-menu-item"
            block
            plain
          >
            <v-icon color="white" left>mdi-account-box</v-icon>
            View Profile
          </v-btn>
          <v-btn
            text
            v-if="isAuthenticated"
            @click="accountDlg=true"
            class="fq-menu-item"
            block
            plain
          >
            <v-icon color="white" left>mdi-account-circle-outline</v-icon>
            Your Account
          </v-btn>
          <v-divider v-if="isAuthenticated"/>
          <v-btn
            text
            v-if="isAuthenticated"
            class="fq-menu-item"
            @click="referralDlg=true"
            block
            plain
          >
            <v-icon color="white" left>mdi-account-network</v-icon>
            Refer a Friend
          </v-btn>
          <v-divider v-if="isAuthenticated"/>
          <v-btn
            text
            v-if="isAuthenticated"
            class="fq-menu-item"
            to="/history/contest"
            block
            plain
          >
            <v-icon color="white" left>mdi-sofa-outline</v-icon>
            Old Contests
          </v-btn>
          <v-divider v-if="isAuthenticated"/>
          <v-btn
            text
            v-if="isAuthenticated"
            class="fq-menu-item"
            to="/leaderboard"
            block
            plain
          >
            <v-icon color="white" left>mdi-view-dashboard-outline</v-icon>
            Leaderboard
          </v-btn>
          <v-divider v-if="isAuthenticated"/>
          <v-btn
            text
            class="fq-menu-item"
            to="/faq"
            block
            plain
          >
            <v-icon color="white" left>mdi-help-circle-outline</v-icon>
            FAQ
          </v-btn>
          <v-divider />
          <v-btn
            text
            v-if="!isAuthenticated"
            @click="launchLogin"
            class="fq-menu-item"
            block
            plain
          >
            <v-icon color="white" left>mdi-login</v-icon>
            Login
          </v-btn>
          <v-divider v-if="isAuthenticated"/>
          <v-btn
            v-if="isAuthenticated"
            text
            class="fq-menu-item"
            @click="logout"
            block
            plain
          >
            <v-icon color="white" left>mdi-logout</v-icon>
            Logout
          </v-btn>
        </div>
      </v-list>
    </v-menu>

    <!-- Notifications -->
    <v-menu
      bottom
      left
      offset-y
      origin="top right"
      transition="scale-transition"
      z-index=100
    >
      <template v-slot:activator="{ attrs, on }">
        <v-btn
          min-width="0"
          text
          v-bind="attrs"
          v-on="on"
          class="fq-btn top-btn"
          exact-active-class="fq-btn-active"
          style="padding: 10px 10px !important; margin: 0 1px;"
        >
          <v-badge
            :content="notificationLengh"
            :value="notificationLengh"
            color="red lighten-1"
            overlap
            left
            small
          >
            <v-icon>mdi-bell</v-icon>
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
    
    <instruction :value.sync="instructionDlg" @update="instructionDlg=false" />
    <user-profile v-if="isProfileDlg"/>
    <your-account v-if="isAuthenticated" :value.sync="accountDlg" @update="accountDlg=false" />
    <referral :value.sync="referralDlg" @update="referralDlg=false"/>
  </v-app-bar>
</template>

<script>
  // Components
  import { VHover, VListItem } from 'vuetify/lib'

  // Utilities
  import { mapState, mapMutations, mapGetters } from 'vuex'
  import UserProfile from '../../pages/UserProfile'
  import YourAccount from '../../pages/YourAccount'
  import Instruction from '../../instruction/Instruction'
  import Referral from '../../referral/Referral'

  export default {
    name: 'DashboardCoreAppBar',

    components: {
      Instruction,
      UserProfile,
      YourAccount,
      Referral,
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
      profileDlg: false,
      referralDlg: false,
      accountDlg: false,
      tops: [
        { name: 'Lobby', to:'/'},
        { name: 'Selection', to:'/selection'},
        { name: 'Contest', to:'/contest'},
      ]
    }),

    computed: {
      ...mapState(['drawer', 'notifications']),
      ...mapState('auth', ['authUser']),
      ...mapGetters('auth', ['isAuthenticated']),

      notificationLengh () {
        return this.notifications.length < 100 ? this.notifications.length : '99+'
      },
      isProfileDlg () {
        return this.$store.getters['auth/launchProfile']
      },
      authBtnLabel () {
        return this.isAuthenticated && this.authUser.displayname
      },
      myMoney () {
        let coins = this.authUser.coins
        if (coins > 9999) {
          coins = '9999+'
        }
        return this.isAuthenticated && `F${coins}`
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
      },
      showChat () {
        if (this.$route.name == 'Chat') return
        this.$router.push({ name: 'Chat' })
      },
      showProfileDlg () {
        this.$store.dispatch('auth/loadProfile')
        this.$store.commit('auth/showProfileDlg')
      }
    },
  }
</script>
