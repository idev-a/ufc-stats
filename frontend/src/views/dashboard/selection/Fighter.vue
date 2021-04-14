<template>
  <v-tooltip top>
    <template v-slot:activator="{ on }">
      <v-btn
        :value="item.id"
        :disabled="eventStarted"
        small
        text
        :class="{'initial': initial, 'first-name': firstName}"
      >
        {{_fighterName()}}
        <v-icon 
          v-if="false"
          right
          :color="_color()"
        >
          {{_fighterGenderIcon()}}
        </v-icon>
      </v-btn>
    </template>
    <span>{{_fightFullGender()}}</span>
  </v-tooltip>
</template>

<script>
  export default {
    name: 'Fighter',

    props: ['item', 'eventStarted', 'initial', 'firstName'],

    methods: {
      _fighterName () {
        let name = this.initial ? this.item.initials : this.item.name 
        const _split = this.item.name.trim().split(' ')
        return this.firstName ? _split[_split.length-1] : name
      },
      _color () {
        return this.item.gender == 'F' ? 'pink' : 'teal darken-4'
      },
      _fightFullGender() {
        return this.item.gender == 'M' ? 'Male' : 'Female'
      },
      _fighterGenderIcon () {
        let gender = 'mdi-human-male'
        if (this.item.gender == 'F') {
          gender = 'mdi-human-female'
        }
        return gender
      },
    }
  }
</script>