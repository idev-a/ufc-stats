(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0e8c24"],{"8b48":function(e,t,a){"use strict";a.r(t);var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("v-dialog",{attrs:{fullscreen:""},model:{value:e.propDlg,callback:function(t){e.propDlg=t},expression:"propDlg"}},[a("v-snackbar",{attrs:{absolute:"",top:"",center:"",color:e.snackbar_color,"multi-line":e.multiLine},model:{value:e.snackbar,callback:function(t){e.snackbar=t},expression:"snackbar"}},[a("span",[e._v(e._s(e.snackbar_message))]),a("v-icon",{attrs:{dark:""}},[e._v(" mdi-checkbox-marked-circle ")])],1),a("v-row",{staticStyle:{"min-height":"100vh"},attrs:{justify:"center",align:"center"}},[a("v-slide-y-transition",{attrs:{appear:""}},[a("v-card",{staticClass:"px-5 py-5",attrs:{light:"","max-width":"100%",width:"400"}},[a("v-app-bar",{attrs:{flat:"",color:"rgba(0, 0, 0, 0)"}},[a("div",{staticClass:"text-center display-2 font-weight-bold"},[e._v(" Login ")]),a("v-spacer"),a("v-btn",{attrs:{icon:""},on:{click:function(t){e.propDlg=!1}}},[a("v-icon",[e._v("mdi-close")])],1)],1),a("v-card-text",{staticClass:"text-center"},[a("v-form",{ref:"form",model:{value:e.valid,callback:function(t){e.valid=t},expression:"valid"}},[a("v-text-field",{ref:"email",staticClass:"mb-5",attrs:{rules:[e.rules.required,e.rules.email],loading:e.authenticating,"hide-details":"auto",color:"secondary",label:"Email address.","prepend-icon":"mdi-email",required:""},on:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.submit(t)}},model:{value:e.form.email,callback:function(t){e.$set(e.form,"email",t)},expression:"form.email"}}),a("v-text-field",{ref:"password",staticClass:"mb-7",attrs:{type:"password",rules:[e.rules.required],loading:e.authenticating,"hide-details":"auto",color:"secondary",label:"Password.","prepend-icon":"mdi-key",required:""},on:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.submit(t)}},model:{value:e.form.password,callback:function(t){e.$set(e.form,"password",t)},expression:"form.password"}}),a("v-btn",{staticClass:"ma-1 mt-1",attrs:{color:"primary",loading:e.authenticating},on:{click:e.submit}},[e._v(" Login ")]),a("div",{staticClass:"text-center mt-2 grey--text body-1 font-weight-light"},[e._v(" If you don't have any account, please "),a("a",{attrs:{href:"javascript:;"},on:{click:e.gotoSignup}},[e._v("sign up")])])],1)],1)],1)],1)],1)],1)},s=[],i=(a("b0c0"),a("dca8"),a("5530")),o=(a("d722"),a("bc3a"),a("2f62")),n={name:"PagesLogin",components:{},props:["value"],data:function(){var e=this,t=Object.freeze({email:"",password:""});return{valid:!0,loading:!1,formHasErrors:!1,errorMessages:{email:{required:!1,invalid:!1,business:!1}},snackbar:!1,snackbar_message:"",snackbar_color:"success",multiLine:!0,defaultForm:t,form:Object.assign({},t),code:"",keepMeLogin:!1,rules:{required:function(t){return e.errorMessages.email.required=!!t,e.errorMessages.email.required||"This field is required."},counter:function(e){return e.length>=6||"Min 6 characters"},email:function(t){var a=/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;return e.errorMessages.email.invalid=a.test(t),e.errorMessages.email.invalid||"Invalid e-mail."}},socials:[{href:"#",icon:"mdi-google"}]}},computed:Object(i["a"])(Object(i["a"])(Object(i["a"])({},Object(o["d"])("auth",["authenticating","error"])),Object(o["b"])("auth",["isAuthenticated"])),{},{propDlg:{get:function(){return this.$store.getters["auth/launchLogin"]},set:function(e){this.$store.commit("auth/showLoginDlg",e)}}}),watch:{authenticating:function(e){e||this.error||"Dashboard"==this.$route.name||this.$router.push({name:"Dashboard"})}},methods:{gotoSignup:function(){this.$store.commit("auth/showLoginDlg",!1),this.$store.commit("signup/showRegisterDlg")},gotoDashboard:function(e){localStorage.setItem("jwt","success"),localStorage.setItem("user",JSON.stringify(e)),this.$store.commit("signup/showRegisterDlg",!1)},resetForm:function(){this.form=Object.assign({},this.defaultForm),this.$refs.form.reset(),this.formHasErrors=!1},submit:function(){if(this.$refs.form.validate(),this.valid){var e={username:this.form.email,password:this.form.password};this.$store.dispatch("auth/login",e)}}}},l=n,c=a("2877"),u=a("6544"),d=a.n(u),m=a("40dc"),f=a("8336"),p=a("b0af"),g=a("99d9"),h=a("169a"),b=a("4bd4"),v=a("132d"),k=a("0fd9"),w=a("0789"),y=a("2db4"),x=a("2fa4"),_=a("8654"),$=Object(c["a"])(l,r,s,!1,null,null,null);t["default"]=$.exports;d()($,{VAppBar:m["a"],VBtn:f["a"],VCard:p["a"],VCardText:g["b"],VDialog:h["a"],VForm:b["a"],VIcon:v["a"],VRow:k["a"],VSlideYTransition:w["f"],VSnackbar:y["a"],VSpacer:x["a"],VTextField:_["a"]})}}]);
//# sourceMappingURL=chunk-2d0e8c24.f302e69e.js.map