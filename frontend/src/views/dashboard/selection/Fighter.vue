<template>
  <v-tooltip top>
    <template v-slot:activator="{ on }">
      <v-btn
        :value="id"
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

    props: ['fighters', 'id', 'eventStarted', 'initial', 'firstName'],

    methods: {
      _fighter () {
        const fighters = this.fighters.filter(fighter => fighter.id == this.id)
        return fighters[0]
      },
      _fighterName () {
        const fighter = this._fighter()
        let name = this.initial ? fighter.initials : fighter.name 
        const _split = fighter.name.trim().split(' ')
        return this.firstName ? _split[_split.length-1] : name
      },
      _color () {
        return this._fighter().gender == 'F' ? 'pink' : 'teal darken-4'
      },
      _fightFullGender() {
        return this._fighter().gender == 'M' ? 'Male' : 'Female'
      },
      _fighterGenderIcon () {
        const fighter = this._fighter(this.id)
        let gender = 'mdi-human-male'
        if (fighter.gender == 'F') {
          gender = 'mdi-human-female'
        }
        return gender
      },
    }
  }
</script>