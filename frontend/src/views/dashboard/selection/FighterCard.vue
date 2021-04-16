<template>
  <carousel-3d :controls-visible="true" :controls-width="40" :border="0" :controls-color="'red'" :display="3" >
    <slide v-for="(bout, i) in bouts" :index="i">
        <div class="font-weight-medium display-2">Fight {{i+1}}</div>
        <v-item-group @change="$emit('changeContests')" v-model="bout.survivors" mandatory multiple>
          <div class="d-flex align-center">
            <v-item :value="bout.fighter1.id" v-slot="{ active, toggle }">
              <fighter-clip
                :item="bout.fighter1"
                :active="active"
                @toggle="toggle"
              />
            </v-item>
            <img
              height="20"
              style="width:auto;"
              class="mx-3"
              src="https://ik.imagekit.io/cuhwrvztecz/vs_du08k6_9Q.png"
            ></img>
            <v-item :value="bout.fighter2.id" v-slot="{ active, toggle }">
              <fighter-clip
                :item="bout.fighter2"
                :active="active"
                @toggle="toggle"
              />
            </v-item>
        </div>
          </v-item-group>
        <div class="highlight--text">{{bout.division}}</div>
      </v-item-group> 
    </slide>
  </carousel-3d>
</template>

<script>
  import FighterClip from './FighterClip'

  export default {
    name: 'FighterCard',

    props: ['bouts'],

    components: { FighterClip },

    data () {
      return {
      }
    },

    methods: {
      // toggle(fighter, index) {
      //   console.log(fighter, index)
      // }
    }
  }
</script>

<style lang="scss">
  .carousel-3d-slide {
    display: flex;
    flex-direction:column;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    background-color: #212121ab;
    backdrop-filter: blur(5px);
  }

  .carousel-3d-controls {
    span {
      color: #EF5350;
    }
  }
</style>