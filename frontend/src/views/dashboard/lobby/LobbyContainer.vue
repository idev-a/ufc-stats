<template>
  <v-container
    fluid
    tag="section"
    class="d-flex justify-center pa-1"
  >
    <div style="width: 100%" v-if="$vuetify.breakpoint.mobile">
      <lobby />
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
      }"
    >
      <lobby />
    </dialog-drag>
  </v-container>
</template>

<script>
  import { mapState, mapGetters } from 'vuex'
  import DialogDrag from 'vue-dialog-drag'
  import Lobby from './Lobby'

  export default {
    name: 'LobbyContainer',

    components: {
      DialogDrag,
      Lobby
    },

    computed: {
      ...mapState(['lastLeft']),
    },

    methods: {
      dragEnd (val) {
        this.$store.commit('SET_LASTLEFT', val.left)
      },
    }
  }
</script>
