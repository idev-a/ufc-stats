<template>
  <v-card
    class="fq-popup mt-0"
  >
    <v-card-title>
      <b class="display-2">Summary</b>
    </v-card-title>
    <v-card-text>
      <span>{{ summary }}</span>
    </v-card-text>

    <v-card-title>
      <b class="display-2">Rules</b>
    </v-card-title>
    <v-card-text>
      <ul class="instruction-list">
        <li v-for="(rule, x) in rulesSet">{{x+1}}. {{rule}}</li>
      </ul>
    </v-card-text>
  </v-card>
</template> 

<script>
  export default {
    name: "ContestSummary",

    props: ['summary', 'rulesSet'],

    data: () => ({   
    }),
  }
</script>