(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-0a429868"],{"8eb4":function(t,e,r){var a=r("24fb");e=a(!1),e.push([t.i,"#register .v-list-item__subtitle{-webkic-line-clamp:initial;-webkit-box-orient:initial}",""]),t.exports=e},aaf8:function(t,e,r){"use strict";r.r(e);var a=function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("v-dialog",{attrs:{fullscreen:""},model:{value:t.propDlg,callback:function(e){t.propDlg=e},expression:"propDlg"}},[r("v-row",{staticStyle:{"min-height":"100vh"},attrs:{justify:"center",align:"center"}},[r("v-slide-y-transition",{attrs:{appear:""}},[r("v-card",{staticClass:"px-auto py-3 fq-popup",attrs:{"max-width":"100%",width:"400",height:t.height}},[r("v-app-bar",{attrs:{flat:"",color:"rgba(0, 0, 0, 0)"}},[r("div",{staticClass:"text-center display-2 font-weight-bold"},[t._v(" Register to UFC Survivor ")]),r("v-spacer"),r("v-btn",{attrs:{icon:""},on:{click:function(e){t.propDlg=!1}}},[r("v-icon",[t._v("mdi-close")])],1)],1),r("v-card-text",{staticClass:"text-center"},[r("v-btn",{staticClass:"mb-5",attrs:{block:"",color:"#1DA1F2",loading:t.authenticating},on:{click:function(e){return t.twitterLogin()}}},[t._v(" Signup with Twitter "),r("v-icon",{attrs:{right:""}},[t._v("mdi-twitter")])],1),r("div",{staticClass:"my-2"},[t._v("Or")]),r("v-btn",{attrs:{block:"",color:"teal accent-4"},on:{click:function(e){t.reveal=!0}}},[t._v(" Signup with Email ")])],1),r("div",{staticClass:"text-center grey--text mt-2 body-1 font-weight-light"},[t._v(" If you already have an account, please "),r("a",{attrs:{href:"javascript:;"},on:{click:t.gotoLogin}},[t._v("login")])]),r("v-expand-transition",[t.reveal?r("v-card",{staticClass:"transition-fast-in-fast-out v-card--reveal fq-popup",staticStyle:{height:"100%",top:"70px"}},[r("v-card-text",{staticClass:"pb-0"},[r("v-form",{ref:"form",model:{value:t.valid,callback:function(e){t.valid=e},expression:"valid"}},[r("v-text-field",{ref:"email",staticClass:"mt-5 mb-7",attrs:{rules:[t.rules.required,t.rules.email],loading:t.registrationLoading,"hide-details":"auto",color:"secondary",label:"Please enter your email address.","prepend-icon":"mdi-email",required:""},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.submit(e)}},model:{value:t.form.email,callback:function(e){t.$set(t.form,"email",e)},expression:"form.email"}}),r("v-text-field",{ref:"displayname",staticClass:"mb-5",attrs:{rules:[t.rules.required],loading:t.authenticating,"hide-details":"auto",color:"secondary",label:"Display Name","prepend-icon":"mdi-account",required:""},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.submit(e)}},model:{value:t.form.displayname,callback:function(e){t.$set(t.form,"displayname",e)},expression:"form.displayname"}}),r("v-text-field",{attrs:{loading:t.registrationLoading,"prepend-icon":t.show1?"mdi-eye":"mdi-eye-off",rules:[t.rules.required,t.rules.min],type:t.show1?"text":"password",name:"input-10-1",label:"Password",hint:"At least 8 characters",counter:""},on:{"click:prepend":function(e){t.show1=!t.show1}},model:{value:t.form.password1,callback:function(e){t.$set(t.form,"password1",e)},expression:"form.password1"}}),r("v-text-field",{attrs:{block:"",loading:t.registrationLoading,"prepend-icon":t.show1?"mdi-eye":"mdi-eye-off",rules:[t.rules.required,t.passwordMatch],type:t.show1?"text":"password",name:"input-10-1",label:"Confirm Password",counter:""},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.submit(e)},"click:prepend":function(e){t.show1=!t.show1}},model:{value:t.form.password2,callback:function(e){t.$set(t.form,"password2",e)},expression:"form.password2"}}),r("v-btn",{staticClass:"my-5",attrs:{loading:t.registrationLoading,color:"primary",diabled:!t.valid||t.registrationLoading,block:""},on:{click:t.submit}},[t._v(" Submit ")]),r("v-btn",{staticClass:"mt-5",attrs:{color:"teal accent-4",block:""},on:{click:function(e){t.reveal=!1}}},[t._v(" Close ")])],1)],1)],1):t._e()],1)],1)],1)],1)],1)},i=[],s=(r("dca8"),r("96cf"),r("1da1")),n=r("5530"),o=r("2f62"),c={name:"PagesRegister",props:["value"],data:function(){var t=Object.freeze({username:"",displayname:"",email:"",password1:"",password2:""});return{reveal:!1,loading:!1,valid:!0,snackbar:{snack:!1,message:"",status:"success"},defaultForm:t,form:Object.assign({},t),show1:!1,rules:{required:function(t){return!!t||"Required."},min:function(t){return t&&t.length>=8||"Min 8 characters"},counter:function(t){return t.length>=6||"Min 6 characters"},email:function(t){var e=/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;return e.test(t)||"Invalid e-mail."}}}},computed:Object(n["a"])(Object(n["a"])(Object(n["a"])({},Object(o["d"])("signup",["registrationCompleted","registrationError","registrationLoading"])),Object(o["d"])("auth",["authenticating","error"])),{},{propDlg:{get:function(){return this.$store.getters["signup/launchRegister"]},set:function(t){this.reveal=!1,this.$store.commit("signup/showRegisterDlg",t)}},passwordMatch:function(){var t=this;return function(){return t.form.password1===t.form.password2||"Password must match"}},height:function(){return this.reveal?"470px":"100%"}}),watch:{registrationLoading:function(t){if(!t&&(this.registrationError?(this.snackbar.message=this.registrationError,this.snackbar.status="failed"):(this.snackbar.message="Successfully registered.",this.snackbar.status="success"),this.snackbar.snack=!0,this.$store.dispatch("snackbar/setSnack",this.snackbar),!this.registrationError)){var e={username:this.form.username,password:this.form.password1};this.$store.dispatch("auth/login",e)}},authenticating:function(t){t||this.error||this.$store.commit("auth/showLoginDlg",!1)},registrationCompleted:function(t){console.log("registrationCompleted")}},methods:{gotoLogin:function(){this.$store.commit("signup/showRegisterDlg",!1),this.$store.commit("auth/showLoginDlg")},submit:function(){var t=this;return Object(s["a"])(regeneratorRuntime.mark((function e(){var r;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:if(t.$refs.form.validate(!0),t.valid){e.next=3;break}return e.abrupt("return");case 3:t.valid&&(t.form.username=t.form.email,t.form.referred_by=null===(r=t.$route.params)||void 0===r?void 0:r.id,console.log(t.form),t.$store.dispatch("signup/createAccount",t.form));case 4:case"end":return e.stop()}}),e)})))()},twitterLogin:function(){this.$store.dispatch("auth/twitterLogin")}}},l=c,u=(r("fb8f"),r("2877")),d=r("6544"),p=r.n(d),f=r("40dc"),m=r("8336"),g=r("b0af"),h=r("99d9"),v=r("169a"),b=r("0789"),w=r("4bd4"),k=r("132d"),y=r("0fd9b"),x=r("2fa4"),C=r("8654"),_=Object(u["a"])(l,a,i,!1,null,null,null);e["default"]=_.exports;p()(_,{VAppBar:f["a"],VBtn:m["a"],VCard:g["a"],VCardText:h["b"],VDialog:v["a"],VExpandTransition:b["a"],VForm:w["a"],VIcon:k["a"],VRow:y["a"],VSlideYTransition:b["e"],VSpacer:x["a"],VTextField:C["a"]})},cb65:function(t,e,r){var a=r("8eb4");"string"===typeof a&&(a=[[t.i,a,""]]),a.locals&&(t.exports=a.locals);var i=r("499e").default;i("510600dc",a,!0,{sourceMap:!1,shadowMode:!1})},fb8f:function(t,e,r){"use strict";r("cb65")}}]);
//# sourceMappingURL=chunk-0a429868.0bf86182.js.map