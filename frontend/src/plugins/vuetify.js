import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import i18n from '@/i18n'
import '@/sass/overrides.sass'

Vue.use(Vuetify)

const theme = {
  primary: '#E91E63',
  secondary: '#9C27b0',
  accent: '#9C27b0',
  warning: '#EF5350',
  info: '#00CAE3',
  winner: '#2E7D32',
  loser: '#43A047',
  died: '#B71C1C',
  highlight: '#E65100',
  strike: '#B71C1C',
  twitter: '#1DA1F2',
  gold: '#FFD700',
  silver: '#C0C0C0',
  bronze: '#cd7f32'
}

export default new Vuetify({
  lang: {
    t: (key, ...params) => i18n.t(key, params),
  },
  theme: {
    themes: {
      dark: theme,
      light: theme,
    },
    dark: true
  },
})
