(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-20fa281c"],{"0fd9":function(t,e,a){"use strict";a("99af"),a("4160"),a("caad"),a("13d5"),a("4ec9"),a("b64b"),a("d3b7"),a("ac1f"),a("2532"),a("3ca3"),a("5319"),a("159b"),a("ddb0");var r=a("ade3"),n=a("5530"),i=(a("4b85"),a("2b0e")),s=a("d9f7"),o=a("80d2"),c=["sm","md","lg","xl"],u=["start","end","center"];function l(t,e){return c.reduce((function(a,r){return a[t+Object(o["D"])(r)]=e(),a}),{})}var d=function(t){return[].concat(u,["baseline","stretch"]).includes(t)},f=l("align",(function(){return{type:String,default:null,validator:d}})),h=function(t){return[].concat(u,["space-between","space-around"]).includes(t)},m=l("justify",(function(){return{type:String,default:null,validator:h}})),g=function(t){return[].concat(u,["space-between","space-around","stretch"]).includes(t)},p=l("alignContent",(function(){return{type:String,default:null,validator:g}})),v={align:Object.keys(f),justify:Object.keys(m),alignContent:Object.keys(p)},b={align:"align",justify:"justify",alignContent:"align-content"};function w(t,e,a){var r=b[t];if(null!=a){if(e){var n=e.replace(t,"");r+="-".concat(n)}return r+="-".concat(a),r.toLowerCase()}}var y=new Map;e["a"]=i["a"].extend({name:"v-row",functional:!0,props:Object(n["a"])(Object(n["a"])(Object(n["a"])({tag:{type:String,default:"div"},dense:Boolean,noGutters:Boolean,align:{type:String,default:null,validator:d}},f),{},{justify:{type:String,default:null,validator:h}},m),{},{alignContent:{type:String,default:null,validator:g}},p),render:function(t,e){var a=e.props,n=e.data,i=e.children,o="";for(var c in a)o+=String(a[c]);var u=y.get(o);return u||function(){var t,e;for(e in u=[],v)v[e].forEach((function(t){var r=a[t],n=w(e,t,r);n&&u.push(n)}));u.push((t={"no-gutters":a.noGutters,"row--dense":a.dense},Object(r["a"])(t,"align-".concat(a.align),a.align),Object(r["a"])(t,"justify-".concat(a.justify),a.justify),Object(r["a"])(t,"align-content-".concat(a.alignContent),a.alignContent),t)),y.set(o,u)}(),t(a.tag,Object(s["a"])(n,{staticClass:"row",class:u}),i)}})},"3f43":function(t,e,a){},"4bd4":function(t,e,a){"use strict";a("4de4"),a("7db0"),a("4160"),a("caad"),a("07ac"),a("2532"),a("159b");var r=a("5530"),n=a("58df"),i=a("7e2b"),s=a("3206");e["a"]=Object(n["a"])(i["a"],Object(s["b"])("form")).extend({name:"v-form",provide:function(){return{form:this}},inheritAttrs:!1,props:{disabled:Boolean,lazyValidation:Boolean,readonly:Boolean,value:Boolean},data:function(){return{inputs:[],watchers:[],errorBag:{}}},watch:{errorBag:{handler:function(t){var e=Object.values(t).includes(!0);this.$emit("input",!e)},deep:!0,immediate:!0}},methods:{watchInput:function(t){var e=this,a=function(t){return t.$watch("hasError",(function(a){e.$set(e.errorBag,t._uid,a)}),{immediate:!0})},r={_uid:t._uid,valid:function(){},shouldValidate:function(){}};return this.lazyValidation?r.shouldValidate=t.$watch("shouldValidate",(function(n){n&&(e.errorBag.hasOwnProperty(t._uid)||(r.valid=a(t)))})):r.valid=a(t),r},validate:function(){return 0===this.inputs.filter((function(t){return!t.validate(!0)})).length},reset:function(){this.inputs.forEach((function(t){return t.reset()})),this.resetErrorBag()},resetErrorBag:function(){var t=this;this.lazyValidation&&setTimeout((function(){t.errorBag={}}),0)},resetValidation:function(){this.inputs.forEach((function(t){return t.resetValidation()})),this.resetErrorBag()},register:function(t){this.inputs.push(t),this.watchers.push(this.watchInput(t))},unregister:function(t){var e=this.inputs.find((function(e){return e._uid===t._uid}));if(e){var a=this.watchers.find((function(t){return t._uid===e._uid}));a&&(a.valid(),a.shouldValidate()),this.watchers=this.watchers.filter((function(t){return t._uid!==e._uid})),this.inputs=this.inputs.filter((function(t){return t._uid!==e._uid})),this.$delete(this.errorBag,e._uid)}}},render:function(t){var e=this;return t("form",{staticClass:"v-form",attrs:Object(r["a"])({novalidate:!0},this.attrs$),on:{submit:function(t){return e.$emit("submit",t)}}},this.$slots.default)}})},aaf8:function(t,e,a){"use strict";a.r(e);var r=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-container",{staticClass:"fill-height justify-center",attrs:{id:"register",tag:"section"}},[a("v-snackbar",{attrs:{timeout:5e3,color:t.snackbar.status},scopedSlots:t._u([{key:"action",fn:function(e){var r=e.attrs;return[a("v-btn",t._b({attrs:{dark:"",text:""},on:{click:function(e){t.snackbar.snack=!1}}},"v-btn",r,!1),[t._v(" Close ")])]}}]),model:{value:t.snackbar.snack,callback:function(e){t.$set(t.snackbar,"snack",e)},expression:"snackbar.snack"}},[t._v(" "+t._s(t.snackbar.message)+" ")]),a("v-row",{attrs:{justify:"center"}},[a("v-slide-y-transition",{attrs:{appear:""}},[a("base-material-card",{staticClass:"px-5 py-3",attrs:{color:"light-blue accent-3",light:"","max-width":"100%",width:"400"},scopedSlots:t._u([{key:"heading",fn:function(){return[a("div",{staticClass:"text-center"},[a("div",{staticClass:"display-2 font-weight-bold"},[t._v(" Register to UFC Survivor ")])])]},proxy:!0}])},[a("div",{staticClass:"text-center"},[a("v-form",{ref:"form",attrs:{"lazy-validation":""},model:{value:t.valid,callback:function(e){t.valid=e},expression:"valid"}},[a("v-text-field",{ref:"email",staticClass:"mt-5 mb-7",attrs:{rules:[t.rules.required,t.rules.email],loading:t.registrationLoading,"hide-details":"auto",color:"secondary",label:"Please enter your email address.","prepend-icon":"mdi-email",required:""},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.submit(e)}},model:{value:t.form.email,callback:function(e){t.$set(t.form,"email",e)},expression:"form.email"}}),a("v-text-field",{attrs:{loading:t.registrationLoading,"prepend-icon":t.show1?"mdi-eye":"mdi-eye-off",rules:[t.rules.required,t.rules.min],type:t.show1?"text":"password",name:"input-10-1",label:"Password",hint:"At least 8 characters",counter:""},on:{"click:prepend":function(e){t.show1=!t.show1}},model:{value:t.form.password1,callback:function(e){t.$set(t.form,"password1",e)},expression:"form.password1"}}),a("v-text-field",{attrs:{block:"",loading:t.registrationLoading,"prepend-icon":t.show1?"mdi-eye":"mdi-eye-off",rules:[t.rules.required,t.passwordMatch],type:t.show1?"text":"password",name:"input-10-1",label:"Confirm Password",counter:""},on:{"click:prepend":function(e){t.show1=!t.show1}},model:{value:t.form.password2,callback:function(e){t.$set(t.form,"password2",e)},expression:"form.password2"}}),a("v-btn",{staticClass:"display-1",attrs:{loading:t.registrationLoading,color:"primary",diabled:!t.valid||t.registrationLoading},on:{click:t.submit}},[t._v(" Submit ")]),a("div",{staticClass:"text-center grey--text mt-2 body-1 font-weight-light"},[t._v(" If you already have an account, please "),a("a",{attrs:{href:"javascript:;"},on:{click:t.gotoLogin}},[t._v("login")])])],1)],1)])],1)],1)],1)},n=[],i=(a("dca8"),a("96cf"),a("1da1")),s=a("5530"),o=a("2f62"),c={name:"PagesRegister",data:function(){var t=this,e=Object.freeze({username:"",email:"",password1:"",password2:""});return{loading:!1,valid:!0,errorMessages:{username:"",email:{required:!1,invalid:!1,business:!1},password:""},timeout:1e4,multiLine:!0,snackbar:{snack:!1,message:"",status:"success"},terms:!1,defaultForm:e,form:Object.assign({},e),show1:!1,rules:{required:function(t){return!!t||"Required."},min:function(t){return t&&t.length>=8||"Min 8 characters"},counter:function(t){return t.length>=6||"Min 6 characters"},email:function(e){var a=/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;return t.errorMessages.email.invalid=a.test(e),t.errorMessages.email.invalid||"Invalid e-mail."}}}},computed:Object(s["a"])(Object(s["a"])({},Object(o["d"])("signup",["registrationCompleted","registrationError","registrationLoading"])),{},{formHasErrors:function(){return!this.errorMessages.email.required||!this.errorMessages.email.invalid},passwordMatch:function(){var t=this;return function(){return t.form.password1===t.form.password2||"Password must match"}}}),watch:{registrationLoading:function(t){t||(this.registrationError?(this.snackbar.message=this.registrationError,this.snackbar.status="failed"):(this.snackbar.message="Successfully registered.",this.snackbar.status="success"),this.snackbar.snack=!0)}},methods:{gotoLogin:function(){this.$router.push({name:"Login"})},resetForm:function(){this.form=Object.assign({},this.defaultForm),this.$refs.form.reset(),this.formHasErrors=!1},submit:function(){var t=this;return Object(i["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:t.$refs.form.validate(!0),t.valid&&(t.form.username=t.form.email,t.$store.dispatch("signup/createAccount",t.form));case 2:case"end":return e.stop()}}),e)})))()}}},u=c,l=(a("fb8f"),a("2877")),d=a("6544"),f=a.n(d),h=a("8336"),m=a("a523"),g=a("4bd4"),p=a("0fd9"),v=a("0789"),b=a("2db4"),w=a("8654"),y=Object(l["a"])(u,r,n,!1,null,null,null);e["default"]=y.exports;f()(y,{VBtn:h["a"],VContainer:m["a"],VForm:g["a"],VRow:p["a"],VSlideYTransition:v["f"],VSnackbar:b["a"],VTextField:w["a"]})},fb8f:function(t,e,a){"use strict";a("3f43")}}]);
//# sourceMappingURL=chunk-20fa281c.0a0d7d96.js.map