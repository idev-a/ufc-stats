<template>
  <v-btn 
    small 
    class="success"
    :loading="loading"
    :disabled="loading || !authUser"
    @click="$emit('create-new-game')"
  >
    <v-icon v-if="!icon" :left="!icon">mdi-plus</v-icon> 
    <span>New Game</span>
  </v-btn>
</template>

<script>
  export default {
    name: 'CreateGameBtn',

    props: ['loading', 'authUser', 'icon'],
  }
</script>