<template>
	<v-container
    tag="section"
    class="d-flex justify-center pa-1"
  >
		<v-sheet
			class="faq-box w-100 fq-popup"
		>
			<h1 class="display-3 font-weight-bold mb-4"><span class="h2"></span>Got a question?</h1>
			<v-text-field
        v-model="query"
        class="mb-8"
        append-outer-icon="mdi-magnify"
        clearable
        label="Search for a question"
        type="text"
        @click:append-outer="searchQuestion"
        @click:clear="clearQuestion"
      ></v-text-field>

      <!-- <v-divider class="my-5" /> -->

      <p class="display-1 ml-3" v-if="filterData">Total {{filterData.length}}</p>
      <v-sheet
	    	class="accordions"
      >
	      <v-expansion-panels 
	      	focusable
	      	accordion
	      	popout
	      >
			    <v-expansion-panel
			      v-for="item in filterData"
			      :key="item.id"
			    >
			      <v-expansion-panel-header>{{ item.question }}</v-expansion-panel-header>
			      <v-expansion-panel-content>
			        {{ item.answer }}
			      </v-expansion-panel-content>
			    </v-expansion-panel>
			  </v-expansion-panels>
			</v-sheet>
		</v-sheet>
	</v-container>
</template>

<script>
	import main from '@/api/main'

	export default {
		name: 'FAQ',

		data () {
			return {
				loading: false,
				query: '',
				data: []
			}
		},

		computed: {
			filterData () {
				let newFaqs = []
				const pattern = new RegExp(this.query, "i")
				this.data.map(faq => {
					if (faq.question.search(pattern) != -1 || faq.answer.search(pattern) != -1) {
						newFaqs.push(faq)
					}
				})
				return newFaqs
			}
		},

		mounted() {
			this.loadFaqs()
		},

		methods: {
			async loadFaqs () {
				this.loading = true
				const { data } = await main.getFaqs()
				this.data = data.results
				this.loading = false
			},
			searchQuestion () {

			},
			clearQuestion () {

			}
		}
	}
</script>

<style lang="scss">
	.faq-box {
		padding: 2rem;
		min-height: calc(100vh - 98px);
		background-color: #1e1e1eed;
	}

	.accordions {
		background: transparent !important; 
		//max-height: calc(100vh - 298px); 
		//overflow-y: auto;

		.v-expansion-panel-content__wrap {
			padding: 18px 24px 16px;
		}
	}
	
</style>