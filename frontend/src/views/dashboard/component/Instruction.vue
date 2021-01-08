<template>
  <v-dialog 
    v-model="insideValue"
    width="600px"
  >
    <v-card>
      <v-card-title>
        <b>Instructions</b>
      </v-card-title>
      <v-card-text>
        <ul class="instruction-list">
          <li v-for="(ins, x) in instructions">{{x+1}}. {{ins}}</li>
        </ul>
      </v-card-text>

      <v-card-title>
        <b>Rules</b>
      </v-card-title>
      <v-card-text>
        <ul class="instruction-list">
          <li v-for="(rule, x) in rules">{{x+1}}. {{rule}}</li>
        </ul>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
    name: "",

    props: ['value'],

    computed: {
      insideValue: {
        get() {
          return this.value
        },
        set () {
          this.$emit('update');
        }
      }
    },

    data: () => ({
      instructions: [
        'Choose fighters',
        'Hope they all survive'
      ],
      rules: [
        'User can pick any number of fighters. If any of them get finished, user is eliminated.',
        'Out of all surviving entries, the user with the most surviving fighters, wins the contest.',
        'If there is a tie, the winner is the entry with the most winning fighters.',
        'If there is still a tie, the winner is the user who entered the contest first.'
      ]
    }),
  }
</script>