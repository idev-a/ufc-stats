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
      src="https://ik.imagekit.io/cuhwrvztecz/0sHOA324_200x200_nYjw_BM9ezv7.jpg"
    ></v-img>
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