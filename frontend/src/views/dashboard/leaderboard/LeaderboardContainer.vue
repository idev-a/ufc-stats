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
      <overall-board />
    </div>
    <dialog-drag 
      v-else
      id="movingLeaderboardDlg"
      @drag-end="dragEnd"
      :options="{
        buttonClose: false,
        left: lastLeft,
        dragCursor: 'move',
        zIndex: 5,
      }"
    >
      <overall-board />
    </dialog-drag>
  </v-container>
</template>

<script>
  import { mapState } from 'vuex'
  import DialogDrag from 'vue-dialog-drag'
  import OverallBoard from './OverallBoard'

  export default {
    name: 'LeaderboardContainer',

    components: { DialogDrag, OverallBoard },

    computed: {
      ...mapState(['lastLeft'])
    },

    methods: {
      dragEnd (val) {
        this.$store.commit('SET_LASTLEFT', val.left)
      },
    }
  }
</script>