<template>
  <v-card
    class="fq-popup"
  >
    <v-card-title>
      <b class="display-2">Instructions</b>
    </v-card-title>
    <v-card-text>
      <ul class="instruction-list">
        <li v-for="(ins, x) in instructions" :key="x">{{x+1}}. {{ins}}</li>
      </ul>
    </v-card-text>

    <v-card-title>
      <b class="display-2">Rules</b>
    </v-card-title>
    <v-card-text>
      <ul class="instruction-list">
        <li v-for="(rule, x) in rulesSet" :key="x">{{x+1}}. {{rule}}</li>
      </ul>
    </v-card-text>
  </v-card>
</template> 

<script>
  export default {
    name: "InstructionBody",

    props: ['instructions', 'rulesSet'],

    data: () => ({   
    }),
  }
</script>