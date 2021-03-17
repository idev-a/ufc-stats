<template>
  <v-container
    fluid
    tag="section"
    class="d-flex justify-center pa-1"
  >
    <div style="width: 100%" v-if="$vuetify.breakpoint.mobile">
      <selection :game_id="game_id" :retry_number="retry_number" />
    </div>
    <dialog-drag
      v-else
      id="movingSelectionDlg"
      @drag-end="dragEnd"
      :options="{
        buttonClose: false,
        left: lastLeft,
        dragCursor: 'move',
        zIndex: 5,
        width: 800
      }"
    >
      <selection :game_id="game_id" :retry_number="retry_number" />
    </dialog-drag>
  </v-container>
</template>

<script>
  import { mapState, mapGetters } from 'vuex'
  import DialogDrag from 'vue-dialog-drag'
  import Selection from './Selection'

  export default {
    name: 'SelectionContainer',

    components: {
      DialogDrag,
      Selection
    },

    computed: {
      ...mapState(['lastLeft']),
      _width () {
        return this.$vuetify.breakpoint.mobile ? 340 : 370
      },
      game_id () {
        return +this.$route.params.game_id
      },
      retry_number () {
        return +this.$route.params.retry_number || 1
      }
    },

    methods: {
      dragEnd (val) {
        this.$store.commit('SET_LASTLEFT', val.left)
      },
    }
  }
</script>
