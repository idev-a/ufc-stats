<template>
	<div id="contest-table">
    <v-card
      tile
      :width="$vuetify.breakpoint.mobile ? '100%' : 320"
      class="ma-0 pa-0 fq-popup"
    >
      <v-card-title
        class="mb-3"
      >
        Add Fighters
      </v-card-title>
      <v-card-text>
        <toggle-box
          :fighters="fighters"
          :bouts="bouts"
          :initial="true"
        />
      </v-card-text>
      <v-card-actions class="pa-0">
        <v-spacer/>
        <v-btn small  @click="closeDlg">Close</v-btn> 
        <v-btn small  class="success" @click="okDlg">Ok</v-btn> 
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
	import ToggleBox from './ToggleBox'

	export default {
		name: "ToggleBoxCard",

		props: ['bouts', 'fighters'],

		components: { ToggleBox },

		methods: {
      closeDlg () {
        this.bouts.forEach(bout => {
          bout.contests = bout.contests_orig
        })
        this.$emit('closeDlg')
      },
      okDlg () {
        this.$emit('okDlg1')
      }
		}
	}
</script>