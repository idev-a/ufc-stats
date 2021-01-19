<template>
  <v-container
    id="contest"
    fluid
    tag="section"
    class="pa-0"
  >
    <div v-if="$vuetify.breakpoint.mobile">
      <selection />
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
        width: _width
      }"
    >
      <selection />
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
    },

    methods: {
      dragEnd (val) {
        this.$store.commit('SET_LASTLEFT', val.left)
      },
    }
  }
</script>
