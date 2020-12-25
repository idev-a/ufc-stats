(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-63d73ef0","chunk-9824a526"],{"3c93":function(e,t,r){},"3f43":function(e,t,r){},a797:function(e,t,r){"use strict";r("a9e3");var s=r("5530"),a=(r("3c93"),r("a9ad")),i=r("7560"),n=r("f2e7"),o=r("58df");t["a"]=Object(o["a"])(a["a"],i["a"],n["a"]).extend({name:"v-overlay",props:{absolute:Boolean,color:{type:String,default:"#212121"},dark:{type:Boolean,default:!0},opacity:{type:[Number,String],default:.46},value:{default:!0},zIndex:{type:[Number,String],default:5}},computed:{__scrim:function(){var e=this.setBackgroundColor(this.color,{staticClass:"v-overlay__scrim",style:{opacity:this.computedOpacity}});return this.$createElement("div",e)},classes:function(){return Object(s["a"])({"v-overlay--absolute":this.absolute,"v-overlay--active":this.isActive},this.themeClasses)},computedOpacity:function(){return Number(this.isActive?this.opacity:0)},styles:function(){return{zIndex:this.zIndex}}},methods:{genContent:function(){return this.$createElement("div",{staticClass:"v-overlay__content"},this.$slots.default)}},render:function(e){var t=[this.__scrim];return this.isActive&&t.push(this.genContent()),e("div",{staticClass:"v-overlay",class:this.classes,style:this.styles},t)}})},aaf8:function(e,t,r){"use strict";r.r(t);var s=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-dialog",{attrs:{fullscreen:""},model:{value:e.propDlg,callback:function(t){e.propDlg=t},expression:"propDlg"}},[r("v-snackbar",{attrs:{timeout:5e3,color:e.snackbar.status},scopedSlots:e._u([{key:"action",fn:function(t){var s=t.attrs;return[r("v-btn",e._b({attrs:{dark:"",text:""},on:{click:function(t){e.snackbar.snack=!1}}},"v-btn",s,!1),[e._v(" Close ")])]}}]),model:{value:e.snackbar.snack,callback:function(t){e.$set(e.snackbar,"snack",t)},expression:"snackbar.snack"}},[e._v(" "+e._s(e.snackbar.message)+" ")]),r("v-row",{staticStyle:{"min-height":"100vh"},attrs:{justify:"center",align:"center"}},[r("v-slide-y-transition",{attrs:{appear:""}},[r("v-card",{staticClass:"px-5 py-3",attrs:{light:"","max-width":"100%",width:"400"}},[r("v-app-bar",{attrs:{flat:"",color:"rgba(0, 0, 0, 0)"}},[r("div",{staticClass:"text-center display-2 font-weight-bold"},[e._v(" Register to UFC Survivor ")]),r("v-spacer"),r("v-btn",{attrs:{icon:""},on:{click:function(t){e.propDlg=!1}}},[r("v-icon",[e._v("mdi-close")])],1)],1),r("div",{staticClass:"text-center"},[r("v-form",{ref:"form",attrs:{"lazy-validation":""},model:{value:e.valid,callback:function(t){e.valid=t},expression:"valid"}},[r("v-text-field",{ref:"email",staticClass:"mt-5 mb-7",attrs:{rules:[e.rules.required,e.rules.email],loading:e.registrationLoading,"hide-details":"auto",color:"secondary",label:"Please enter your email address.","prepend-icon":"mdi-email",required:""},on:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.submit(t)}},model:{value:e.form.email,callback:function(t){e.$set(e.form,"email",t)},expression:"form.email"}}),r("v-text-field",{attrs:{loading:e.registrationLoading,"prepend-icon":e.show1?"mdi-eye":"mdi-eye-off",rules:[e.rules.required,e.rules.min],type:e.show1?"text":"password",name:"input-10-1",label:"Password",hint:"At least 8 characters",counter:""},on:{"click:prepend":function(t){e.show1=!e.show1}},model:{value:e.form.password1,callback:function(t){e.$set(e.form,"password1",t)},expression:"form.password1"}}),r("v-text-field",{attrs:{block:"",loading:e.registrationLoading,"prepend-icon":e.show1?"mdi-eye":"mdi-eye-off",rules:[e.rules.required,e.passwordMatch],type:e.show1?"text":"password",name:"input-10-1",label:"Confirm Password",counter:""},on:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.submit(t)},"click:prepend":function(t){e.show1=!e.show1}},model:{value:e.form.password2,callback:function(t){e.$set(e.form,"password2",t)},expression:"form.password2"}}),r("v-btn",{staticClass:"display-1",attrs:{loading:e.registrationLoading,color:"primary",diabled:!e.valid||e.registrationLoading},on:{click:e.submit}},[e._v(" Submit ")]),r("div",{staticClass:"text-center grey--text mt-2 body-1 font-weight-light"},[e._v(" If you already have an account, please "),r("a",{attrs:{href:"javascript:;"},on:{click:e.gotoLogin}},[e._v("login")])])],1)],1)],1)],1)],1)],1)},a=[],i=(r("dca8"),r("96cf"),r("1da1")),n=r("5530"),o=r("2f62"),c={name:"PagesRegister",props:["value"],data:function(){var e=this,t=Object.freeze({username:"",email:"",password1:"",password2:""});return{loading:!1,valid:!0,errorMessages:{username:"",email:{required:!1,invalid:!1,business:!1},password:""},timeout:1e4,multiLine:!0,snackbar:{snack:!1,message:"",status:"success"},terms:!1,defaultForm:t,form:Object.assign({},t),show1:!1,rules:{required:function(e){return!!e||"Required."},min:function(e){return e&&e.length>=8||"Min 8 characters"},counter:function(e){return e.length>=6||"Min 6 characters"},email:function(t){var r=/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;return e.errorMessages.email.invalid=r.test(t),e.errorMessages.email.invalid||"Invalid e-mail."}}}},computed:Object(n["a"])(Object(n["a"])(Object(n["a"])({},Object(o["d"])("signup",["registrationCompleted","registrationError","registrationLoading"])),Object(o["d"])("auth",["authenticating","error"])),{},{formHasErrors:function(){return!this.errorMessages.email.required||!this.errorMessages.email.invalid},passwordMatch:function(){var e=this;return function(){return e.form.password1===e.form.password2||"Password must match"}},propDlg:{get:function(){return this.$store.getters["signup/launchRegister"]},set:function(e){this.$store.commit("signup/showRegisterDlg",e)}}}),watch:{registrationLoading:function(e){if(!e){this.registrationError?(this.snackbar.message=this.registrationError,this.snackbar.status="failed"):(this.snackbar.message="Successfully registered.",this.snackbar.status="success"),this.snackbar.snack=!0;var t={username:this.form.username,password:this.form.password1};this.$store.dispatch("auth/login",t)}},authenticating:function(e){e||this.error||this.$store.commit("auth/showLoginDlg",!1)},registrationCompleted:function(e){console.log("registrationCompleted")}},methods:{gotoLogin:function(){this.$store.commit("signup/showRegisterDlg",!1),this.$store.commit("auth/showLoginDlg")},resetForm:function(){this.form=Object.assign({},this.defaultForm),this.$refs.form.reset(),this.formHasErrors=!1},submit:function(){var e=this;return Object(i["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:e.$refs.form.validate(!0),e.valid&&(e.form.username=e.form.email,e.$store.dispatch("signup/createAccount",e.form));case 2:case"end":return t.stop()}}),t)})))()}}},l=c,u=(r("fb8f"),r("2877")),d=r("6544"),f=r.n(d),m=r("40dc"),p=r("8336"),h=r("b0af"),v=r("169a"),g=r("4bd4"),b=r("132d"),y=r("0fd9"),k=r("0789"),w=r("2db4"),x=r("2fa4"),_=r("8654"),C=Object(u["a"])(l,s,a,!1,null,null,null);t["default"]=C.exports;f()(C,{VAppBar:m["a"],VBtn:p["a"],VCard:h["a"],VDialog:v["a"],VForm:g["a"],VIcon:b["a"],VRow:y["a"],VSlideYTransition:k["f"],VSnackbar:w["a"],VSpacer:x["a"],VTextField:_["a"]})},f977:function(e,t,r){"use strict";r.d(t,"a",(function(){return n}));var s=r("53ca");function a(e,t){var r=t.modifiers||{},a=r.self,i=void 0!==a&&a,n=t.value,o="object"===Object(s["a"])(n)&&n.options||{passive:!0},c="function"===typeof n||"handleEvent"in n?n:n.handler,l=i?e:t.arg?document.querySelector(t.arg):window;l&&(l.addEventListener("scroll",c,o),e._onScroll={handler:c,options:o,target:i?void 0:l})}function i(e){if(e._onScroll){var t=e._onScroll,r=t.handler,s=t.options,a=t.target,i=void 0===a?e:a;i.removeEventListener("scroll",r,s),delete e._onScroll}}var n={inserted:a,unbind:i};t["b"]=n},fb8f:function(e,t,r){"use strict";r("3f43")}}]);
//# sourceMappingURL=chunk-63d73ef0.46c2dd73.js.map