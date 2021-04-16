<template>
  <v-card
    :color="active ? 'success' : ''"
    class="my-5 py-0"
    max-width="124"
    @click="$emit('toggle', item.id)"
    style="background-color: #424242ab; backdrop-filter: blur(5px);"
  >
    <v-img
      height="100"
      max-widht="40"
      :src="item.image"
      lazy-src="https://ik.imagekit.io/cuhwrvztecz/dustin_poirier_XTWHamMdf.jpg"
      contain
      aspect-ratio="2"
    >
      <template v-slot:placeholder>
        <v-row
          class="fill-height ma-0"
          align="center"
          justify="center"
        >
          <v-progress-circular
            indeterminate
            color="grey lighten-5"
          ></v-progress-circular>
        </v-row>
      </template>
    </v-img>
    <div class="pa-2 text-center" style="font-size: 14px;">{{item.name}}</div>
  </v-card>
</template>

<script>
  export default {
    name: 'FighterClip',

    props: ['item', 'active'],

    data () {
      return {

      }
    }
  }
</script>