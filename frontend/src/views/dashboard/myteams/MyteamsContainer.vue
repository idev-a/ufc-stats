<template>
  <v-container
    tag="section"
    class="d-flex justify-center pa-1"
  >
    <div
      style="width: 100%;"
    >
      <myteams />
    </div>
    <!-- <div
      style="width: 100%"
      v-if="!$vuetify.breakpoint.mobile"
    >
      <myteams />
    </div>
    <dialog-drag 
      v-else
      id="movingMyteamDlg"
      class="w-100"
      @drag-end="dragEnd"
      :options="{
        buttonClose: false,
        left: lastLeft,
        dragCursor: 'move',
        zIndex: 5,
      }"
    >
      <myteams />
    </dialog-drag> -->
  </v-container>
</template>

<script>
  import { mapState } from 'vuex'
  import DialogDrag from 'vue-dialog-drag'
  import Myteams from './Myteams'

  export default {
    name: 'ContestContainer',

    components: { DialogDrag, Myteams },

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

