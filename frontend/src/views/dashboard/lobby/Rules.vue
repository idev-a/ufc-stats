<template>
  <div>
    <v-sheet
      class="pa-2 mt-3"
      elevation="1"
      max-height="300"
      width="100%"
      style="overflow-y: auto"
    >
      <span v-html="game.rules_set.replace(/\n/g, '<br/>')"></span>
    </v-sheet>
  </div>
</template>

<script>
  export default {
    name: 'ContestDetail',

    props: ['game'],
  }
</script>