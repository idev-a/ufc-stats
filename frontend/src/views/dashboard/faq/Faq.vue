<template>
  <v-container
    tag="section"
    class="d-flex justify-center pa-1"
  >
    <v-sheet
      class="faq-box w-100 fq-popup"
    >
      <div class="d-flex justify-space-between">
        <h1 class="display-3 font-weight-bold mb-4"><span class="h2"></span>Got a question?</h1>

        <div class="d-flex align-center ml-auto">
          <span class="mr-2 font-weight-medium">Need More Help?</span>
          <v-btn @click="showDlg" small class="success">Contact US<v-icon size=18 right>mdi-chat</v-icon> </v-btn>
        </div>
      </div>
      <v-text-field
        v-model="query"
        class="mb-8"
        append-outer-icon="mdi-magnify"
        clearable
        label="Search for a question"
        type="text"
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

    <!-- Contact US -->
    <v-dialog
      v-model="dlg"
      max-width=600
    >
      <v-card
        class="fq-popup"
      >
        <v-card-title
          class="font-weight-bold"
        >
          CONTACT US
        </v-card-title>
        <v-card-text>
          <v-form
            ref="form"
            v-model="valid"
          >
            <v-text-field
              v-model="form.title"
              :rules="[rules.required]"
              outlined
              clearable
              label="Title"
              type="text"
            ></v-text-field>
            <v-textarea
              v-model="form.message"
              :rules="[rules.required]"
              counter
              outlined
              class="mb-8"
              clearable
              label="Message"
              type="text"
              rows="4"
              auto-grow
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn :disabled="loading || !valid" :loading="loading" @click="submitTicket" small class="success">Submit</v-btn>
          <v-btn small @click="closeDlg">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
        data: [],
        dlg: false,
        valid: true,
        form: {
          title: '',
          message: '',
        },
        rules: {
          required: value => {
            return !!value || 'This field is required.'
          },
        }
      }
    },

    computed: {
      filterData () {
        if (this.query == null) {
          this.query = ''
        }
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
      showDlg () {
        this.dlg = true
      },
      closeDlg () {
        this.$refs.form.reset()
        this.$refs.form.resetValidation()
        this.dlg = false
      },
      async submitTicket () {
        this.loading = true
        const { data } = await main.submitTicket(this.form)
        const snackbar = {
          snack: true,
          message: data.message,
          status: data.status == 200 ? 'success' : 'dark'
        }
        this.$store.commit('snackbar/setSnack', snackbar)
        this.loading = false
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