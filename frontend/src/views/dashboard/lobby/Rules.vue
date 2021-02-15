<template>
  <div>
    <v-sheet
      class="pa-2 mt-3"
      elevation="1"
      height="100"
      width="100%"
    >
      {{ game.rules_set }}
    </v-sheet>
  </div>
</template>

<script>
  export default {
    name: 'ContestDetail',

    props: ['game'],
  }
</script>