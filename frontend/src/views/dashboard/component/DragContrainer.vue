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
      <slot name="child-component" :item="item"></slot>
    </div>
    <dialog-drag 
      v-else
      id="uniqueid"
      @drag-end="dragEnd"
      :options="{
        buttonClose: false,
        left: lastLeft,
        dragCursor: 'move',
        zIndex: 5,
      }"
    >
      <slot name="child-component" :item="item"></slot>
    </dialog-drag>
  </v-container>
</template>

<script>
  import { mapState } from 'vuex'
  import DialogDrag from 'vue-dialog-drag'

  export default {
    name: 'ContestContainer',

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

