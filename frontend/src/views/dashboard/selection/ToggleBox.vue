<template>
  <div
    class="text-center w-100"
  >
    <div class="overline">{{bouts.length*2}} FIGHTERS ( <b style="color:#fffd">SQUAD SIZE: {{squadSize}}</b> )</div>

    <div 
      class="relative"
    >
      <v-icon v-if="_down" class="arrow-down" color="red">mdi-arrow-down-drop-circle-outline</v-icon>
      <v-btn v-if="_side" class="arrow-side" :class="sideCollapseClass" @click="collapseSide" fab small color="#eeea"><v-icon color="red">mdi-arrow-collapse-right</v-icon></v-btn>
      <div
        id="scrollContainer"
        @scroll="onScroll"
      >
        <template v-for="bout in bouts">
          <v-btn-toggle
            v-model="bout.survivors"
            :disabled="loading"
            :key="bout.id"
            dense
            multiple
            class="justify-space-between mb-2 mx-1"
            tile
            @change="changeContests"
          >
            <fighter 
              :id="bout.fighter1"
              :fighters="fighters"
              :eventStated="eventStarted"
              :initial="initial"
            />

            <div 
              class="between-fighters"
            >
              ({{ bout.division }})
            </div>

            <fighter 
              :id="bout.fighter2"
              :fighters="fighters"
              :eventStated="eventStarted"
              :initial="initial"
            />

          </v-btn-toggle>
        </template>
      </div>
      <v-icon v-if="_up" class="arrow-up" color="red">mdi-arrow-up-drop-circle-outline</v-icon>
    </div>
  </div>
</template>

<script>
  import Fighter from './Fighter'

  export default {
    name: 'ToggleBox',

    components: { Fighter },

    props: ['bouts', 'eventStarted', 'fighters', 'loading', 'initial'],

    data () {
      return {
        top: 0,
        sHeight: -1,
        squadSize: 0
      }
    },

    computed: {
      _up() {
        return this.top > 0 && this.$vuetify.breakpoint.mobile
      },
      _down() {
        return (this.top == 0 || (this.top + 300) < this.sHeight) && 
              this.$vuetify.breakpoint.mobile
      },
      _side() {
        return !this.$vuetify.breakpoint.mobile && false
      },
      sideCollapseClass () {
        return ''
      },
    },

    mounted () {
      this.changeContests()
    },

    methods: {
      onScroll ({ target: { scrollTop, clientHeight, scrollHeight }}) {
        this.top = scrollTop
        this.sHeight = scrollHeight
        if (scrollTop + clientHeight >= scrollHeight) {
        }
      },
      collapseSide () {
        this.side = !this.side
      },
      changeContests () {
        this.squadSize = 0
        this.bouts.forEach(bout => {
          this.squadSize += bout.survivors.length
        })
      }
    }
  }
</script>