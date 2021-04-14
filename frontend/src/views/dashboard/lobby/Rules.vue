<template>
  <div>
    <v-card
      max-height="300"
      style="overflow-y: auto"
    >
      <v-card-text>
        <ul class="instruction-list">
          <li v-for="(rule, x) in rules_set" :key="x">{{x+1}}. {{rule}}</li>
        </ul>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
  import { DEFAULT_RULES_SET } from '@/constants/constant'

  export default {
    name: 'GameRules',

    props: ['game'],

    computed: {
      rules_set () {
        return this.game.rules_set && this.game.rules_set.split('\n') || DEFAULT_RULES_SET
      },
    },
  }
</script>