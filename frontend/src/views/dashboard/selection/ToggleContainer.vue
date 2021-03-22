<template>
  <v-container
    fluid
    tag="section"
    class="d-flex justify-center pa-1"
  >    
    <div
      v-if="$vuetify.breakpoint.mobile"
    >
      <v-card
        tile
        width="320"
        class="ma-0 pa-0 fq-popup"
      >
        <v-card-title
        >
          Add Fighters
        </v-card-title>
        <v-card-text>
          <toggle-box
            :fighters="fighters"
            :bouts="bouts"
            :initial="true"
          />
        </v-card-text>
        <v-card-actions class="pt-0">
          <v-spacer/>
          <v-btn small  @click="closeDlg">Close</v-btn> 
          <v-btn small  class="success" @click="okDlg">Ok</v-btn> 
        </v-card-actions>
      </v-card>
    </div>
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
      <div
      >
        <v-card
          tile
          width="320"
          class="ma-0 pa-0 fq-popup"
        >
          <v-card-title
          >
            ADD FIGHTERS
          </v-card-title>
          <v-card-text>
            <toggle-box
              :fighters="fighters"
              :bouts="bouts"
              :initial="true"
            />
          </v-card-text>
          <v-card-actions class="pt-0">
            <v-spacer/>
            <v-btn small  @click="closeDlg">Close</v-btn> 
            <v-btn small  class="success" @click="okDlg">Ok</v-btn> 
          </v-card-actions>
        </v-card>
      </div>
    </dialog-drag>
  </v-container>
</template>

<script>
  import { mapState } from 'vuex'
  import DialogDrag from 'vue-dialog-drag'
  import ToggleBox from "../selection/ToggleBox";

  export default {
    name: 'ContestContainer',

    components: { DialogDrag, ToggleBox },

    props: ['bouts', 'fighters'],

    computed: {
      ...mapState(['lastLeft']),
    },

    methods: {
      dragEnd (val) {
        this.$store.commit('SET_LASTLEFT', val.left)
      },
      closeDlg () {
        this.$emit('close')
      },
      okDlg () {
        this.$emit('ok')
      }
    }
  }
</script>

