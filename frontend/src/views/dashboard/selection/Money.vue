<template>
	<div>
		<div
      v-if="isPaidContest"
      class="d-flex"
      style="font-size: 14px; position: absolute; right: 20px;" 
    >
      <div 
        class="d-flex"
      >
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-icon v-on="on"  color="gold">mdi-crown-outline</v-icon>
          </template>
          <span>Prize</span>
        </v-tooltip>
        <span class="gold--text">{{contestPrize}}</span>
      </div>
      <div 
        class="d-flex ml-2"
      >
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-icon v-on="on" color="red lighten-1">mdi-cash</v-icon>
          </template>
          <span>Buyin</span>
        </v-tooltip>
        <span class="red--text lighten-1">{{contestBuyin}}</span>
      </div>
    </div>
	</div>
</template>

<script>
	export default {
		name: "Money",

		props: ['curContest'],

		computed: {
			isPaidContest () {
        return this.curContest && this.curContest.genre == 'paid'
      },
      contestPrize() {
        return this.curContest && this.curContest.prize
      },
      contestBuyin () {
        return this.curContest && this.curContest.buyin
      },
		}
	}
</script>