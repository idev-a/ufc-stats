<template>
  <v-card
    tile
    width="320"
    class="ma-0 pa-0 fq-popup"
  >
    <v-card-title
      class="pt-3"
    >
      Add Fighters
    </v-card-title>
    <v-card-text>
      <toggle-box
        :bouts="bouts"
        :initial="true"
      />
    </v-card-text>
    <v-card-actions class="pt-0">
      <v-spacer/>
      <v-btn small  @click="$emit('close')">Close</v-btn> 
      <v-btn small  class="success" @click="$emit('ok')">Ok</v-btn> 
    </v-card-actions>
  </v-card>
</template>

<script>
  import ToggleBox from "./ToggleBox";

  export default {
    name: "ToggleInnerContrainer",

    props: ['bouts'],

    components: {ToggleBox},
  }
</script>