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
      <contest-history-detail :entry_id="entry_id" />
    </div>
    <dialog-drag 
      v-else
      id="movingContestHistoryDetailDlg"
      @drag-end="dragEnd"
      :options="{
        buttonClose: false,
        left: lastLeft,
        dragCursor: 'move',
        zIndex: 5,
      }"
    >
      <contest-history-detail :entry_id="entry_id" />
    </dialog-drag>
  </v-container>
</template>

<script>
  import { mapState } from 'vuex'
  import DialogDrag from 'vue-dialog-drag'
  import ContestHistoryDetail from './ContestHistoryDetail'

  export default {
    name: 'ContestContainer',

    components: { DialogDrag, ContestHistoryDetail },

    computed: {
      ...mapState(['lastLeft']),
      entry_id () {
        return this.$route.params.entry_id
      }
    },

    methods: {
      dragEnd (val) {
        this.$store.commit('SET_LASTLEFT', val.left)
      },
    }
  }
</script>

