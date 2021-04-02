<template>
  <v-container
    fluid
    tag="section"
    class="d-flex justify-center pa-1"
  >    

    <toggle-inner-container 
      v-if="$vuetify.breakpoint.mobile" 
      @close="$emit('close')"
      @ok="$emit('ok')"
      :bouts="bouts"
      :fighters="fighters"
    />
    <dialog-drag 
      v-else
      id="movingToggleDlg"
      @drag-end="dragEnd"
      :options="{
        buttonClose: false,
        left: lastLeft,
        dragCursor: 'move',
        zIndex: 5,
      }"
    >
      <toggle-inner-container 
        @close="$emit('close')"
        @ok="$emit('ok')"
        :bouts="bouts"
        :fighters="fighters"
      />
    </dialog-drag>
  </v-container>
</template>

<script>
  import { mapState } from 'vuex'
  import DialogDrag from 'vue-dialog-drag'
  import ToggleInnerContainer from "../selection/ToggleInnerContainer";

  export default {
    name: 'ContestContainer',

    components: { DialogDrag, ToggleInnerContainer },

    props: ['bouts', 'fighters'],

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

