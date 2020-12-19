<template>
  <v-container
    id="contest"
    fluid
    tag="section"
    class="d-flex justify-center"
  >
  <v-card
  	:loading="loading"
  	min-width="60%"
  	class="px-5"
  >
  	<v-card-title 
        class="justify-center font-weight-medium mb-md-3"
      >
        <div class="text-center">
          <div>{{ this.event.name }}</div>
          <div class="subtitle-2">{{ this.event.date | beautifyDate }}</div>
        </div>
      </v-card-title>
      <v-card-text>
      	<template
      		v-for="contest in contests"
      	>
      		<v-card 
      			:elevation="1"
      			class="contest-row"
      			:class="{'row-inactive': contest.status=='pending'}"
      		>
    				<div class="contest-column">
	      			<div 
	      				class="contest-item"
	      				:class="{'winner-item': contest.fighter1 == contest.winner, 'loser-item': contest.fighter1 == contest.loser}"
	      			>
      					{{contest.fighter1}}
	      			</div>
	      			<v-virtual-scroll
			          :items="contest.users"
			          :item-height="17"
			          height="80"
			        >
		      			<template v-slot:default="{ item }">
	    						<div 
	    							:key="item.username"
	    							class="contest-user"
	    							:class="{'is-active': item.status}"
	    						>	
	    							{{ contest.fighter1 == item.fighter ? item.username : ''}}
	    						</div>
	    					</template>
	    				</v-virtual-scroll>
    				</div>
    				<div class="contest-column">
	      			<div 
	      				class="contest-item"
	      				:class="{'winner-item': contest.fighter2 == contest.winner, 'loser-item': contest.fighter2 == contest.loser}"
	      			>
	      				<span>{{contest.fighter2}}</span>
	      			</div>
	      			<v-virtual-scroll
			          :items="contest.users"
			          :item-height="17"
			          height="80"
			        >
		      			<template v-slot:default="{ item }">
	    						<div 
	    							:key="item.username"
	    							class="contest-user"
	    							:class="{'is-active': item.status}"
	    						>	
	    							{{ contest.fighter2 == item.fighter ? item.username : ''}}
	    						</div>
	    					</template>
	    				</v-virtual-scroll>
      			</div>
      		</v-card>
      	</template>
      </v-card-text>
  </v-card>
	</v-container>
</template>
<script>
	import session from '@/api/session'
	import { beautifyDate } from '@/util'

	export default {
    name: 'Contest',

    data () {
    	return {
    		loading: false,
    		contests: [],
    		event: ''
    	}
    },

    filters: {
      beautifyDate,
    },

    mounted() {
    	this.getLatestContest()
    },

    methods: {
    	async getLatestContest() {
    		this.loading = true
    		const { data } = await session.get('api/entries/contest')
    		this.contests = data.contests
    		this.event = data.event
    		this.loading = false
    	}
    }
	}
</script>

<style>
	.contest-row {
		display: flex;

		justify-content:space-around;
		margin-bottom: 1.5rem;
		border-radius: 5px;
	}

	.row-inactive {
		background-color: #ECEFF1 !important;
	}

	.contest-item {
		width: 10rem;
		height: 80px;
		border: 1px solid;
	  border-radius: 5px;
    margin: 0 .5rem 0 0;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
	}

	.winner-item {
		background-color: #4CAF50;
	}

	.loser-item {
		background-color: #FF5722;
	}

	.contest-column {
	  display: flex;
	  flex-basis: 100%;
	  flex: 1;
	}

	.contest-user {
		font-size: 14px;
		color: #BDBDBD;
		margin-bottom: .5rem;
	}

	.is-active {
		color: #212121;
	}
</style>