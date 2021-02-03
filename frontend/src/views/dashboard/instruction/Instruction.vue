<template>
  <v-dialog 
    v-model="insideValue"
    width="600px"
  >
    <InstructionBody  />
  </v-dialog>
</template>

<script>
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
      }
    },
  }
</script>
