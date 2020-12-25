(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-be97661e","chunk-2d0e8c24"],{"3c93":function(e,t,a){},"8b48":function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("v-dialog",{attrs:{fullscreen:""},model:{value:e.propDlg,callback:function(t){e.propDlg=t},expression:"propDlg"}},[a("v-snackbar",{attrs:{absolute:"",top:"",center:"",color:e.snackbar_color,"multi-line":e.multiLine},model:{value:e.snackbar,callback:function(t){e.snackbar=t},expression:"snackbar"}},[a("span",[e._v(e._s(e.snackbar_message))]),a("v-icon",{attrs:{dark:""}},[e._v(" mdi-checkbox-marked-circle ")])],1),a("v-row",{staticStyle:{"min-height":"100vh"},attrs:{justify:"center",align:"center"}},[a("v-slide-y-transition",{attrs:{appear:""}},[a("v-card",{staticClass:"px-5 py-5",attrs:{light:"","max-width":"100%",width:"400"}},[a("v-app-bar",{attrs:{flat:"",color:"rgba(0, 0, 0, 0)"}},[a("div",{staticClass:"text-center display-2 font-weight-bold"},[e._v(" Login ")]),a("v-spacer"),a("v-btn",{attrs:{icon:""},on:{click:function(t){e.propDlg=!1}}},[a("v-icon",[e._v("mdi-close")])],1)],1),a("v-card-text",{staticClass:"text-center"},[a("v-form",{ref:"form",model:{value:e.valid,callback:function(t){e.valid=t},expression:"valid"}},[a("v-text-field",{ref:"email",staticClass:"mb-5",attrs:{rules:[e.rules.required,e.rules.email],loading:e.authenticating,"hide-details":"auto",color:"secondary",label:"Email address.","prepend-icon":"mdi-email",required:""},on:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.submit(t)}},model:{value:e.form.email,callback:function(t){e.$set(e.form,"email",t)},expression:"form.email"}}),a("v-text-field",{ref:"password",staticClass:"mb-7",attrs:{type:"password",rules:[e.rules.required],loading:e.authenticating,"hide-details":"auto",color:"secondary",label:"Password.","prepend-icon":"mdi-key",required:""},on:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.submit(t)}},model:{value:e.form.password,callback:function(t){e.$set(e.form,"password",t)},expression:"form.password"}}),a("v-btn",{staticClass:"ma-1 mt-1",attrs:{color:"primary",loading:e.authenticating},on:{click:e.submit}},[e._v(" Login ")]),a("div",{staticClass:"text-center mt-2 grey--text body-1 font-weight-light"},[e._v(" If you don't have any account, please "),a("a",{attrs:{href:"javascript:;"},on:{click:e.gotoSignup}},[e._v("sign up")])])],1)],1)],1)],1)],1)],1)},r=[],i=(a("b0c0"),a("dca8"),a("5530")),o=(a("d722"),a("bc3a"),a("2f62")),n={name:"PagesLogin",components:{},props:["value"],data:function(){var e=this,t=Object.freeze({email:"",password:""});return{valid:!0,loading:!1,formHasErrors:!1,errorMessages:{email:{required:!1,invalid:!1,business:!1}},snackbar:!1,snackbar_message:"",snackbar_color:"success",multiLine:!0,defaultForm:t,form:Object.assign({},t),code:"",keepMeLogin:!1,rules:{required:function(t){return e.errorMessages.email.required=!!t,e.errorMessages.email.required||"This field is required."},counter:function(e){return e.length>=6||"Min 6 characters"},email:function(t){var a=/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;return e.errorMessages.email.invalid=a.test(t),e.errorMessages.email.invalid||"Invalid e-mail."}},socials:[{href:"#",icon:"mdi-google"}]}},computed:Object(i["a"])(Object(i["a"])(Object(i["a"])({},Object(o["d"])("auth",["authenticating","error"])),Object(o["b"])("auth",["isAuthenticated"])),{},{propDlg:{get:function(){return this.$store.getters["auth/launchLogin"]},set:function(e){this.$store.commit("auth/showLoginDlg",e)}}}),watch:{authenticating:function(e){e||this.error||"Dashboard"==this.$route.name||this.$router.push({name:"Dashboard"})}},methods:{gotoSignup:function(){this.$store.commit("auth/showLoginDlg",!1),this.$store.commit("signup/showRegisterDlg")},gotoDashboard:function(e){localStorage.setItem("jwt","success"),localStorage.setItem("user",JSON.stringify(e)),this.$store.commit("signup/showRegisterDlg",!1)},resetForm:function(){this.form=Object.assign({},this.defaultForm),this.$refs.form.reset(),this.formHasErrors=!1},submit:function(){if(this.$refs.form.validate(),this.valid){var e={username:this.form.email,password:this.form.password};this.$store.dispatch("auth/login",e)}}}},c=n,l=a("2877"),u=a("6544"),d=a.n(u),m=a("40dc"),h=a("8336"),f=a("b0af"),p=a("99d9"),v=a("169a"),g=a("4bd4"),b=a("132d"),y=a("0fd9"),k=a("0789"),w=a("2db4"),x=a("2fa4"),_=a("8654"),C=Object(l["a"])(c,s,r,!1,null,null,null);t["default"]=C.exports;d()(C,{VAppBar:m["a"],VBtn:h["a"],VCard:f["a"],VCardText:p["b"],VDialog:v["a"],VForm:g["a"],VIcon:b["a"],VRow:y["a"],VSlideYTransition:k["f"],VSnackbar:w["a"],VSpacer:x["a"],VTextField:_["a"]})},a797:function(e,t,a){"use strict";a("a9e3");var s=a("5530"),r=(a("3c93"),a("a9ad")),i=a("7560"),o=a("f2e7"),n=a("58df");t["a"]=Object(n["a"])(r["a"],i["a"],o["a"]).extend({name:"v-overlay",props:{absolute:Boolean,color:{type:String,default:"#212121"},dark:{type:Boolean,default:!0},opacity:{type:[Number,String],default:.46},value:{default:!0},zIndex:{type:[Number,String],default:5}},computed:{__scrim:function(){var e=this.setBackgroundColor(this.color,{staticClass:"v-overlay__scrim",style:{opacity:this.computedOpacity}});return this.$createElement("div",e)},classes:function(){return Object(s["a"])({"v-overlay--absolute":this.absolute,"v-overlay--active":this.isActive},this.themeClasses)},computedOpacity:function(){return Number(this.isActive?this.opacity:0)},styles:function(){return{zIndex:this.zIndex}}},methods:{genContent:function(){return this.$createElement("div",{staticClass:"v-overlay__content"},this.$slots.default)}},render:function(e){var t=[this.__scrim];return this.isActive&&t.push(this.genContent()),e("div",{staticClass:"v-overlay",class:this.classes,style:this.styles},t)}})}}]);
//# sourceMappingURL=chunk-be97661e.11a915e5.js.map