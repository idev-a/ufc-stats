<template>
  <v-dialog 
    v-model="insideValue"
    width="600px"
  >
    <instruction-body :instructions="instructions" :rulesSet="rulesSet" />
  </v-dialog>
</template>

<script>
  import { DEFAULT_INSTRUCTIONS, DEFAULT_RULES_SET } from '@/constants/constant'
  import InstructionBody from './InstructionBody'

  export default {
    name: "Instruction",

    props: ['value'],

    components: {
      InstructionBody
    },

    computed: {
      insideValue: {
        get() {
          return this.value
        },
        set () {
          this.$emit('update');
        }
      },
      instructions () {
        return DEFAULT_INSTRUCTIONS
      },
      rulesSet () {
        return DEFAULT_RULES_SET
      }
    },
  }
</script>
