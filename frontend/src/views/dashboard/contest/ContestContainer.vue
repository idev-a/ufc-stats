<template>
  <v-container
    fluid
    tag="section"
    class="d-flex justify-center pa-1"
  >
    <div
      style="width: 100%"
      v-if="$vuetify.breakpoint.mobile"
    >
      <contest :game_id="game_id" />
    </div>
    <dialog-drag 
      v-else
      id="movingContestDlg"
      @drag-end="dragEnd"
      :options="{
        buttonClose: false,
        left: lastLeft,
        dragCursor: 'move',
        zIndex: 5,
      }"
    >
      <contest :game_id="game_id" />
    </dialog-drag>
  </v-container>
</template>

<script>
  import { mapState } from 'vuex'
  import DialogDrag from 'vue-dialog-drag'
  import Contest from './Contest'

  export default {
    name: 'ContestContainer',

    components: { DialogDrag, Contest },

    computed: {
      ...mapState(['lastLeft']),
      game_id () {
        return this.$route.params.game_id
      }
    },

    methods: {
      dragEnd (val) {
        this.$store.commit('SET_LASTLEFT', val.left)
      },
    }
  }
</script>

