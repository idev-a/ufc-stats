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
      <contest-history  />
    </div>
    <dialog-drag 
      v-else
      id="movingContestHistoryDlg"
      @drag-end="dragEnd"
      :options="{
        buttonClose: false,
        left: lastLeft,
        dragCursor: 'move',
        zIndex: 5,
      }"
    >
      <contest-history  />
    </dialog-drag>
  </v-container>
</template>

<script>
  import { mapState } from 'vuex'
  import DialogDrag from 'vue-dialog-drag'
  import ContestHistory from './ContestHistory'

  export default {
    name: 'ContestContainer',

    components: { DialogDrag, ContestHistory },

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

