(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-725fbd2a"],{"0fd9b":function(t,e,i){"use strict";i("99af"),i("4160"),i("caad"),i("13d5"),i("4ec9"),i("b64b"),i("d3b7"),i("ac1f"),i("2532"),i("3ca3"),i("5319"),i("159b"),i("ddb0");var n=i("ade3"),a=i("5530"),o=(i("4b85"),i("2b0e")),r=i("d9f7"),s=i("80d2"),c=["sm","md","lg","xl"],l=["start","end","center"];function u(t,e){return c.reduce((function(i,n){return i[t+Object(s["D"])(n)]=e(),i}),{})}var d=function(t){return[].concat(l,["baseline","stretch"]).includes(t)},f=u("align",(function(){return{type:String,default:null,validator:d}})),p=function(t){return[].concat(l,["space-between","space-around"]).includes(t)},h=u("justify",(function(){return{type:String,default:null,validator:p}})),b=function(t){return[].concat(l,["space-between","space-around","stretch"]).includes(t)},v=u("alignContent",(function(){return{type:String,default:null,validator:b}})),g={align:Object.keys(f),justify:Object.keys(h),alignContent:Object.keys(v)},m={align:"align",justify:"justify",alignContent:"align-content"};function y(t,e,i){var n=m[t];if(null!=i){if(e){var a=e.replace(t,"");n+="-".concat(a)}return n+="-".concat(i),n.toLowerCase()}}var w=new Map;e["a"]=o["a"].extend({name:"v-row",functional:!0,props:Object(a["a"])(Object(a["a"])(Object(a["a"])({tag:{type:String,default:"div"},dense:Boolean,noGutters:Boolean,align:{type:String,default:null,validator:d}},f),{},{justify:{type:String,default:null,validator:p}},h),{},{alignContent:{type:String,default:null,validator:b}},v),render:function(t,e){var i=e.props,a=e.data,o=e.children,s="";for(var c in i)s+=String(i[c]);var l=w.get(s);return l||function(){var t,e;for(e in l=[],g)g[e].forEach((function(t){var n=i[t],a=y(e,t,n);a&&l.push(a)}));l.push((t={"no-gutters":i.noGutters,"row--dense":i.dense},Object(n["a"])(t,"align-".concat(i.align),i.align),Object(n["a"])(t,"justify-".concat(i.justify),i.justify),Object(n["a"])(t,"align-content-".concat(i.alignContent),i.alignContent),t)),w.set(s,l)}(),t(i.tag,Object(r["a"])(a,{staticClass:"row",class:l}),o)}})},"145b":function(t,e,i){"use strict";i("83c0")},1727:function(t,e,i){var n=i("24fb");e=n(!1),e.push([t.i,".theme--light.v-footer{background-color:#f5f5f5;color:rgba(0,0,0,.87)}.theme--dark.v-footer{background-color:#272727;color:#fff}.v-sheet.v-footer{border-radius:0}.v-sheet.v-footer:not(.v-sheet--outlined){-webkit-box-shadow:0 0 0 0 rgba(0,0,0,.2),0 0 0 0 rgba(0,0,0,.14),0 0 0 0 rgba(0,0,0,.12);box-shadow:0 0 0 0 rgba(0,0,0,.2),0 0 0 0 rgba(0,0,0,.14),0 0 0 0 rgba(0,0,0,.12)}.v-sheet.v-footer.v-sheet--shaped{border-radius:24px 0}.v-footer{-webkit-box-align:center;-ms-flex-align:center;align-items:center;display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-flex:0!important;-ms-flex:0 1 auto!important;flex:0 1 auto!important;-ms-flex-wrap:wrap;flex-wrap:wrap;padding:6px 16px;position:relative;-webkit-transition-duration:.2s;transition-duration:.2s;-webkit-transition-property:background-color,left,right;transition-property:background-color,left,right;-webkit-transition-timing-function:cubic-bezier(.4,0,.2,1);transition-timing-function:cubic-bezier(.4,0,.2,1)}.v-footer:not([data-booted=true]){-webkit-transition:none!important;transition:none!important}.v-footer--absolute,.v-footer--fixed{z-index:3}.v-footer--absolute{position:absolute}.v-footer--absolute:not(.v-footer--inset){width:100%}.v-footer--fixed{position:fixed}.v-footer--padless{padding:0}",""]),t.exports=e},1859:function(t,e,i){"use strict";i.r(e);var n=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("v-footer",{attrs:{id:"dashboard-core-footer"}},[i("v-container",[i("v-row",{attrs:{align:"center","no-gutters":""}},[t._l(t.socials,(function(e,n){return i("v-col",{key:n,staticClass:"text-center mb-sm-0 mb-5 mx-2",attrs:{cols:"auto"}},[i("v-btn",{attrs:{icon:"",color:"indigo",fab:"",outlined:"",href:e.href}},[i("v-icon",{attrs:{size:"25"}},[t._v(t._s(e.icon))])],1)],1)})),i("v-spacer",{staticClass:"hidden-sm-and-down"}),i("v-col",{attrs:{cols:"12",md:"auto"}},[i("div",{staticClass:"text-center"},t._l(t.links,(function(e,n){return i("a",{key:n,staticClass:"mb-sm-0 mb-5 mx-1 text--black",attrs:{href:e.href}},[t._v(" "+t._s(e.text)+" ")])})),0)])],2),i("v-row",{staticClass:"mt-7",attrs:{align:"center",justify:"center"}},[i("div",{staticClass:"body-1 font-weight-light pt-6 pt-md-0 text-center"},[t._v(" © 2019, copyright ")])])],1)],1)},a=[],o={name:"DashboardCoreFooter",data:function(){return{links:[{href:"https://revampcybersecurity.com",icon:"mdi-home",text:"Home"},{href:"https://revampcybersecurity.com/privacy-policy/",icon:"mdi-twitter",text:"Privacy Policy"},{href:"https://revampcybersecurity.com/security/",icon:"mdi-twitter",text:"Security"}],socials:[{href:"https://twitter.com/revampcyber",icon:"mdi-twitter",text:"Twitter"},{href:"https://www.instagram.com/revampcyber/",icon:"mdi-instagram",text:"Instagram"},{href:"https://www.facebook.com/Revamp-Cybersecurity-764581397233712/",icon:"mdi-facebook",text:"Facebook"},{href:"https://www.linkedin.com/company/revamp-cybersecurity",icon:"mdi-linkedin",text:"Linkedin"},{href:"https://www.youtube.com/channel/UCCKRNAopNV_U-9EGVUGM7rA",icon:"mdi-youtube",text:"Youtube"}]}}},r=o,s=(i("145b"),i("2877")),c=i("6544"),l=i.n(c),u=i("8336"),d=i("62ad"),f=i("a523"),p=(i("a9e3"),i("c7cd"),i("5530")),h=(i("b5b6"),i("8dd9")),b=i("3a66"),v=i("d10f"),g=i("58df"),m=i("80d2"),y=Object(g["a"])(h["a"],Object(b["a"])("footer",["height","inset"]),v["a"]).extend({name:"v-footer",props:{height:{default:"auto",type:[Number,String]},inset:Boolean,padless:Boolean,tag:{type:String,default:"footer"}},computed:{applicationProperty:function(){return this.inset?"insetFooter":"footer"},classes:function(){return Object(p["a"])(Object(p["a"])({},h["a"].options.computed.classes.call(this)),{},{"v-footer--absolute":this.absolute,"v-footer--fixed":!this.absolute&&(this.app||this.fixed),"v-footer--padless":this.padless,"v-footer--inset":this.inset})},computedBottom:function(){if(this.isPositioned)return this.app?this.$vuetify.application.bottom:0},computedLeft:function(){if(this.isPositioned)return this.app&&this.inset?this.$vuetify.application.left:0},computedRight:function(){if(this.isPositioned)return this.app&&this.inset?this.$vuetify.application.right:0},isPositioned:function(){return Boolean(this.absolute||this.fixed||this.app)},styles:function(){var t=parseInt(this.height);return Object(p["a"])(Object(p["a"])({},h["a"].options.computed.styles.call(this)),{},{height:isNaN(t)?t:Object(m["g"])(t),left:Object(m["g"])(this.computedLeft),right:Object(m["g"])(this.computedRight),bottom:Object(m["g"])(this.computedBottom)})}},methods:{updateApplication:function(){var t=parseInt(this.height);return isNaN(t)?this.$el?this.$el.clientHeight:0:t}},render:function(t){var e=this.setBackgroundColor(this.color,{staticClass:"v-footer",class:this.classes,style:this.styles});return t(this.tag,e,this.$slots.default)}}),w=i("132d"),x=i("0fd9b"),j=i("2fa4"),k=Object(s["a"])(r,n,a,!1,null,null,null);e["default"]=k.exports;l()(k,{VBtn:u["a"],VCol:d["a"],VContainer:f["a"],VFooter:y,VIcon:w["a"],VRow:x["a"],VSpacer:j["a"]})},"24e2":function(t,e,i){var n=i("24fb");e=n(!1),e.push([t.i,"#dashboard-core-footer a{font-size:.825rem;font-weight:500;text-decoration:none;text-transform:uppercase}",""]),t.exports=e},"3a66":function(t,e,i){"use strict";i.d(e,"a",(function(){return o}));var n=i("fe6c"),a=i("58df");function o(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:[];return Object(a["a"])(Object(n["b"])(["absolute","fixed"])).extend({name:"applicationable",props:{app:Boolean},computed:{applicationProperty:function(){return t}},watch:{app:function(t,e){e?this.removeApplication(!0):this.callUpdate()},applicationProperty:function(t,e){this.$vuetify.application.unregister(this._uid,e)}},activated:function(){this.callUpdate()},created:function(){for(var t=0,i=e.length;t<i;t++)this.$watch(e[t],this.callUpdate);this.callUpdate()},mounted:function(){this.callUpdate()},deactivated:function(){this.removeApplication()},destroyed:function(){this.removeApplication()},methods:{callUpdate:function(){this.app&&this.$vuetify.application.register(this._uid,this.applicationProperty,this.updateApplication())},removeApplication:function(){var t=arguments.length>0&&void 0!==arguments[0]&&arguments[0];(t||this.app)&&this.$vuetify.application.unregister(this._uid,this.applicationProperty)},updateApplication:function(){return 0}}})}},"83c0":function(t,e,i){var n=i("24e2");"string"===typeof n&&(n=[[t.i,n,""]]),n.locals&&(t.exports=n.locals);var a=i("499e").default;a("0f623dc3",n,!0,{sourceMap:!1,shadowMode:!1})},a523:function(t,e,i){"use strict";i("99af"),i("4de4"),i("b64b"),i("2ca0"),i("20f6"),i("4b85");var n=i("e8f2"),a=i("d9f7");e["a"]=Object(n["a"])("container").extend({name:"v-container",functional:!0,props:{id:String,tag:{type:String,default:"div"},fluid:{type:Boolean,default:!1}},render:function(t,e){var i,n=e.props,o=e.data,r=e.children,s=o.attrs;return s&&(o.attrs={},i=Object.keys(s).filter((function(t){if("slot"===t)return!1;var e=s[t];return t.startsWith("data-")?(o.attrs[t]=e,!1):e||"string"===typeof e}))),n.id&&(o.domProps=o.domProps||{},o.domProps.id=n.id),t(n.tag,Object(a["a"])(o,{staticClass:"container",class:Array({"container--fluid":n.fluid}).concat(i||[])}),r)}})},b5b6:function(t,e,i){var n=i("1727");"string"===typeof n&&(n=[[t.i,n,""]]),n.locals&&(t.exports=n.locals);var a=i("499e").default;a("a83c1470",n,!0,{sourceMap:!1,shadowMode:!1})},e8f2:function(t,e,i){"use strict";i.d(e,"a",(function(){return a}));i("99af"),i("4de4"),i("a15b"),i("b64b"),i("2ca0"),i("498a");var n=i("2b0e");function a(t){return n["a"].extend({name:"v-".concat(t),functional:!0,props:{id:String,tag:{type:String,default:"div"}},render:function(e,i){var n=i.props,a=i.data,o=i.children;a.staticClass="".concat(t," ").concat(a.staticClass||"").trim();var r=a.attrs;if(r){a.attrs={};var s=Object.keys(r).filter((function(t){if("slot"===t)return!1;var e=r[t];return t.startsWith("data-")?(a.attrs[t]=e,!1):e||"string"===typeof e}));s.length&&(a.staticClass+=" ".concat(s.join(" ")))}return n.id&&(a.domProps=a.domProps||{},a.domProps.id=n.id),e(n.tag,a,o)}})}}}]);
//# sourceMappingURL=chunk-725fbd2a.2be5e6be.js.map