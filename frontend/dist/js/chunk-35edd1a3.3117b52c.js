(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-35edd1a3"],{"0ea9":function(t,e,a){var i=a("a134");"string"===typeof i&&(i=[[t.i,i,""]]),i.locals&&(t.exports=i.locals);var n=a("499e").default;n("80b0e8e6",i,!0,{sourceMap:!1,shadowMode:!1})},"2a7f":function(t,e,a){"use strict";a.d(e,"a",(function(){return s}));var i=a("71d9"),n=a("80d2"),s=Object(n["h"])("v-toolbar__title"),o=Object(n["h"])("v-toolbar__items");i["a"]},"47d5":function(t,e,a){var i=a("24fb");e=i(!1),e.push([t.i,".instruction-list{list-style:none}",""]),t.exports=e},"89c2":function(t,e,a){var i=a("24fb");e=i(!1),e.push([t.i,'.theme--light.v-badge .v-badge__badge:after{border-color:#fff}.theme--dark.v-badge .v-badge__badge:after{border-color:#1e1e1e}.v-badge{position:relative}.v-badge,.v-badge__badge{display:inline-block;line-height:1}.v-badge__badge{border-radius:10px;color:#fff;font-size:12px;height:20px;letter-spacing:0;min-width:20px;padding:4px 6px;pointer-events:auto;position:absolute;text-align:center;text-indent:0;top:auto;-webkit-transition:.3s cubic-bezier(.25,.8,.5,1);transition:.3s cubic-bezier(.25,.8,.5,1);white-space:nowrap}.v-application--is-ltr .v-badge__badge{right:auto}.v-application--is-rtl .v-badge__badge{left:auto}.v-badge__badge .v-icon{color:inherit;font-size:12px;margin:0 -2px}.v-badge__badge .v-img{height:12px;width:12px}.v-badge__wrapper{-webkit-box-flex:0;-ms-flex:0 1;flex:0 1;height:100%;left:0;pointer-events:none;position:absolute;top:0;width:100%}.v-badge--avatar .v-badge__badge{padding:0}.v-badge--avatar .v-badge__badge .v-avatar{height:20px!important;min-width:0!important;max-width:20px!important}.v-badge--bordered .v-badge__badge:after{border-radius:inherit;border-width:2px;border-style:solid;bottom:0;content:"";left:0;position:absolute;right:0;top:0;-webkit-transform:scale(1.15);transform:scale(1.15)}.v-badge--dot .v-badge__badge{border-radius:4.5px;height:9px;min-width:0;padding:0;width:9px}.v-badge--dot .v-badge__badge:after{border-width:1.5px}.v-badge--icon .v-badge__badge{padding:4px 6px}.v-badge--inline{-webkit-box-align:center;-ms-flex-align:center;align-items:center;display:-webkit-inline-box;display:-ms-inline-flexbox;display:inline-flex;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center}.v-badge--inline .v-badge__badge,.v-badge--inline .v-badge__wrapper{position:relative}.v-badge--inline .v-badge__wrapper{margin:0 4px}.v-badge--tile .v-badge__badge{border-radius:0}',""]),t.exports=e},"8e07":function(t,e,a){"use strict";a.r(e);var i=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-app-bar",{attrs:{id:"app-bar",absolute:"",app:"",color:"transparent",flat:"",height:"75"}},[a("v-toolbar-title",{staticClass:"hidden-sm-and-down font-weight-medium white--text",domProps:{textContent:t._s(t.$route.name)}}),a("v-spacer"),a("div",{staticClass:"mx-3"}),a("v-tooltip",{attrs:{bottom:"","z-index":"100"},scopedSlots:t._u([{key:"activator",fn:function(e){var i=e.on;return[a("v-btn",t._g({staticStyle:{padding:"10px 10px !important",margin:"0 1px"},attrs:{"min-width":"0",text:"",to:"/"}},i),[a("v-icon",{attrs:{color:"white"}},[t._v("mdi-pickaxe")])],1)]}}])},[a("span",[t._v("Selection")])]),a("v-tooltip",{attrs:{bottom:"","z-index":"100"},scopedSlots:t._u([{key:"activator",fn:function(e){var i=e.on;return[a("v-btn",t._g({staticStyle:{padding:"10px 10px !important",margin:"0 1px"},attrs:{"min-width":"0",text:"",to:"/contest"}},i),[a("v-icon",{attrs:{color:"white"}},[t._v("mdi-sofa-single-outline")])],1)]}}])},[a("span",[t._v("Contest")])]),a("v-tooltip",{attrs:{bottom:"","z-index":"100"},scopedSlots:t._u([{key:"activator",fn:function(e){var i=e.on;return[a("v-btn",t._g({staticStyle:{padding:"10px 10px !important",margin:"0 1px"},attrs:{"min-width":"0",text:""},on:{click:function(e){return e.stopPropagation(),t.showInstruction(e)}}},i),[a("v-icon",{attrs:{color:"white"}},[t._v("mdi-information-outline")])],1)]}}])},[a("span",[t._v("Instructions")])]),a("v-menu",{attrs:{bottom:"",left:"","offset-y":"",origin:"top right",transition:"scale-transition","z-index":"100"},scopedSlots:t._u([{key:"activator",fn:function(e){var i=e.attrs,n=e.on;return[a("v-btn",t._g(t._b({staticStyle:{padding:"10px 10px !important",margin:"0 1px"},attrs:{"min-width":"0",text:""}},"v-btn",i,!1),n),[a("v-badge",{attrs:{content:t.notificationLengh,value:t.notificationLengh,color:"red lighten-1",overlap:"",left:"",small:""}},[a("v-icon",[t._v("mdi-bell")])],1)],1)]}}])},[a("v-list",{staticClass:"overflow-y-auto",staticStyle:{"max-height":"300px"},attrs:{tile:!1,nav:"","two-line":"",dense:"","min-height":"50","min-width":"350"}},[a("v-list-item-group",[t._l(t.notifications,(function(e,i){return[a("v-list-item",{key:i,attrs:{dense:""}},[a("v-list-item-content",[a("v-list-item-subtitle",{staticClass:"text--primary",domProps:{textContent:t._s(e.msg)}})],1),a("v-list-item-action",[a("v-icon",{staticClass:"mb-2"},[t._v("mdi-clock")]),a("v-list-item-action-text",{domProps:{textContent:t._s(e.time)}})],1)],1)]}))],2)],1)],1),a("v-menu",{attrs:{bottom:"",left:"","min-width":"200","offset-y":"",origin:"top right","open-on-hover":"",transition:"scale-transition","z-index":"100"},scopedSlots:t._u([{key:"activator",fn:function(e){var i=e.attrs,n=e.on;return[a("v-btn",t._g(t._b({staticStyle:{padding:"10px 10px !important",margin:"0 1px"},attrs:{"min-width":"0",text:""}},"v-btn",i,!1),n),[a("v-icon",{attrs:{left:t.isAuthenticated,color:"white"}},[t._v("mdi-account")]),t.isAuthenticated&&t.authUser?a("span",{staticClass:"white--text"},[t._v(t._s(t.authUser.displayname))]):t._e()],1)]}}])},[a("v-list",{attrs:{tile:!1,flat:"",nav:""}},[a("div",[t.isAuthenticated?t._e():a("v-btn",{attrs:{text:"",block:"",plain:""},on:{click:t.launchLogin}},[t._v(" Login ")]),t.isAuthenticated?a("v-btn",{attrs:{text:"",block:"",plain:""},on:{click:t.showProfileDlg}},[t._v(" View Profile ")]):t._e(),t.isAuthenticated?a("v-btn",{attrs:{text:"",block:"",plain:""},on:{click:function(e){t.accountDlg=!0}}},[t._v(" Your Account ")]):t._e(),t.isAuthenticated?a("v-divider"):t._e(),t.isAuthenticated?a("v-btn",{attrs:{text:"",block:"",plain:""},on:{click:function(e){t.referralDlg=!0}}},[t._v(" Refer a Friend ")]):t._e(),t.isAuthenticated?a("v-divider"):t._e(),t.isAuthenticated?a("v-btn",{attrs:{text:"",to:"leaderboard",block:"",plain:""}},[t._v(" Leaderboard ")]):t._e(),t.isAuthenticated?a("v-divider"):t._e(),t.isAuthenticated?a("v-btn",{attrs:{text:"",block:"",plain:""},on:{click:t.logout}},[t._v(" Logout ")]):t._e()],1)])],1),a("instruction",{attrs:{value:t.instructionDlg},on:{"update:value":function(e){t.instructionDlg=e},update:function(e){t.instructionDlg=!1}}}),t.isProfileDlg?a("user-profile"):t._e(),t.isAuthenticated?a("your-account",{attrs:{value:t.accountDlg},on:{"update:value":function(e){t.accountDlg=e},update:function(e){t.accountDlg=!1}}}):t._e(),a("referral",{attrs:{value:t.referralDlg},on:{"update:value":function(e){t.referralDlg=e},update:function(e){t.referralDlg=!1}}})],1)},n=[],s=(a("b0c0"),a("5530")),o=a("16b7"),r=a("f2e7"),l=a("58df"),c=a("d9bd"),u=Object(l["a"])(o["a"],r["a"]).extend({name:"v-hover",props:{disabled:{type:Boolean,default:!1},value:{type:Boolean,default:void 0}},methods:{onMouseEnter:function(){this.runDelay("open")},onMouseLeave:function(){this.runDelay("close")}},render:function(){return this.$scopedSlots.default||void 0!==this.value?(this.$scopedSlots.default&&(t=this.$scopedSlots.default({hover:this.isActive})),Array.isArray(t)&&1===t.length&&(t=t[0]),t&&!Array.isArray(t)&&t.tag?(this.disabled||(t.data=t.data||{},this._g(t.data,{mouseenter:this.onMouseEnter,mouseleave:this.onMouseLeave})),t):(Object(c["c"])("v-hover should only contain a single element",this),t)):(Object(c["c"])("v-hover is missing a default scopedSlot or bound value",this),null);var t}}),d=a("da13"),p=a("2f62"),f=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-dialog",{attrs:{width:"600px"},model:{value:t.insideValue,callback:function(e){t.insideValue=e},expression:"insideValue"}},[a("v-card",{staticClass:"fq-popup",attrs:{icon:"mdi-account-outline",loading:t.loading,id:"profile-card"}},[a("v-card-title",[a("div",{staticClass:"d-flex align-center"},[a("v-avatar",{attrs:{color:"brown",size:"84"}},[t.userAvatar?a("v-img",{attrs:{src:t.userAvatar}}):a("span",{staticClass:"white--text initials"},[t._v(" "+t._s(t.userInitials)+" ")])],1),a("div",{staticClass:"display-box"},[a("div",{staticClass:"displayname",domProps:{innerHTML:t._s(t.userDisplayname)}}),a("div",{staticClass:"subtitle"},[t._v("Member since "+t._s(t.userJoinedDate))])])],1)]),a("v-card-text",[a("v-divider"),a("div",{staticClass:"stats-title"},[t._v(" Overview ")]),a("div",{staticClass:"stats-blocks"},[a("v-card",{staticClass:"well",attrs:{loading:t.loading}},[a("div",{staticClass:"stats-value"},[t._v(" "+t._s(t.profile.total_contests)+" ")]),a("div",[t._v(" Contests ")])]),a("v-card",{staticClass:"well",attrs:{loading:t.loading}},[a("div",{staticClass:"stats-value"},[t._v(" "+t._s(t.profile.total_wins)+" ")]),a("div",[t._v(" Win Rate % ")])])],1),a("div",{staticClass:"stats-title mt-5"},[t._v(" Contest History ")]),a("v-data-table",{attrs:{items:t.profile.contest_history,loading:t.loading,headers:t.headers,"fixed-header":"","item-key":"id",dense:"","item-class":"contest-history-tb-row"},scopedSlots:t._u([{key:"item.date",fn:function(e){var a=e.item;return[t._v(" "+t._s(t.beautifyDate(a.date))+" ")]}}])})],1)],1)],1)},v=[],h=(a("96cf"),a("1da1")),b=(a("3786"),a("e0eb")),g={name:"UserProfile",data:function(){return{valid:!0,headers:[{text:"Event",value:"event"},{text:"Date",value:"date"},{text:"Ranking",value:"ranking"}],rules:{required:function(t){return!!t||"This field is required."}}}},computed:Object(s["a"])(Object(s["a"])({},Object(p["d"])("auth",["authUser","loading","profile"])),{},{insideValue:{get:function(){return this.$store.getters["auth/selectedUserId"]},set:function(t){this.$store.commit("auth/setUserId",t)}},userAvatar:function(){return this.profile.user&&this.profile.user.avatar},userInitials:function(){return this.profile.user&&this.profile.user.initials},userDisplayname:function(){return this.profile.user&&this.profile.user.displayname||"Unknown"},userJoinedDate:function(){return this.profile.user&&this.beautifyDate(this.profile.user.date_joined)}}),methods:{beautifyDate:b["a"],updateProfile:function(){var t=this;return Object(h["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:t.$store.dispatch("auth/updateUser",t.authUser);case 1:case"end":return e.stop()}}),e)})))()}}},m=g,x=(a("deaa"),a("2877")),_=a("6544"),y=a.n(_),w=a("8212"),k=a("b0af"),C=a("99d9"),V=a("8fea"),O=a("169a"),$=a("ce7e"),D=a("adda"),j=Object(x["a"])(m,f,v,!1,null,"2765517f",null),A=j.exports;y()(j,{VAvatar:w["a"],VCard:k["a"],VCardText:C["b"],VCardTitle:C["c"],VDataTable:V["a"],VDialog:O["a"],VDivider:$["a"],VImg:D["a"]});var S=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-dialog",{attrs:{width:"600px"},model:{value:t.insideValue,callback:function(e){t.insideValue=e},expression:"insideValue"}},[a("v-card",{staticClass:"fq-popup",attrs:{icon:"mdi-account-outline"}},[a("v-card-title",[a("div",{staticClass:"font-weight-light card-title mt-2"},[t._v(" Account Information ")])]),t.user?a("v-card-text",[a("v-form",{ref:"form",model:{value:t.valid,callback:function(e){t.valid=e},expression:"valid"}},[a("v-container",{staticClass:"py-0"},[a("v-row",[a("v-col",{attrs:{cols:"12",md:"4"}},[a("v-text-field",{staticClass:"purple-input",attrs:{label:"User Name"},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.updateProfile(e)}},model:{value:t.user.username,callback:function(e){t.$set(t.user,"username",e)},expression:"user.username"}})],1),a("v-col",{attrs:{cols:"12",md:"4"}},[a("v-text-field",{staticClass:"purple-input",attrs:{label:"Display Name",required:"",counter:"",minlength:"3",rules:[t.rules.required,t.rules.min3]},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.updateProfile(e)}},model:{value:t.user.displayname,callback:function(e){t.$set(t.user,"displayname",e)},expression:"user.displayname"}})],1),a("v-col",{attrs:{cols:"12",md:"4"}},[a("v-text-field",{staticClass:"purple-input",attrs:{label:"Email Address"},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.updateProfile(e)}},model:{value:t.user.email,callback:function(e){t.$set(t.user,"email",e)},expression:"user.email"}})],1),a("v-col",{staticClass:"text-right",attrs:{cols:"12"}},[a("v-btn",{staticClass:"mr-0",attrs:{color:"success",disabled:!t.valid||t.loading},on:{click:function(e){return e.stopPropagation(),t.updateProfile(e)}}},[t._v(" Update ")])],1)],1)],1)],1)],1):t._e()],1)],1)},I=[],B={name:"Player",data:function(){return{loading:!1,valid:!0,user:null,rules:{required:function(t){return!!t||"This field is required."},min3:function(t){return t.length>=3||"Minimum length is 3"}}}},props:["value"],computed:Object(s["a"])(Object(s["a"])({},Object(p["d"])("auth",["authUser","error"])),{},{insideValue:{get:function(){return this.value},set:function(){this.$emit("update")}}}),watch:{insideValue:function(t){t&&(this.user=Object(s["a"])({},this.authUser))},error:function(t){if(t){var e={message:t,status:"failed",snack:!0};this.$store.dispatch("snackbar/setSnack",e)}}},methods:{updateProfile:function(){var t=this;return Object(h["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:t.$store.dispatch("auth/updateUser",t.user);case 1:case"end":return e.stop()}}),e)})))()}}},L=B,P=a("8336"),T=a("62ad"),U=a("a523"),R=a("4bd4"),E=a("0fd9b"),z=a("8654"),M=Object(x["a"])(L,S,I,!1,null,null,null),q=M.exports;y()(M,{VBtn:P["a"],VCard:k["a"],VCardText:C["b"],VCardTitle:C["c"],VCol:T["a"],VContainer:U["a"],VDialog:O["a"],VForm:R["a"],VRow:E["a"],VTextField:z["a"]});var Y=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-dialog",{attrs:{width:"600px"},model:{value:t.insideValue,callback:function(e){t.insideValue=e},expression:"insideValue"}},[a("InstructionBody")],1)},X=[],F=a("b709"),J={name:"Instruction",props:["value"],components:{InstructionBody:F["a"]},computed:{insideValue:{get:function(){return this.value},set:function(){this.$emit("update")}}}},H=J,N=Object(x["a"])(H,Y,X,!1,null,null,null),W=N.exports;y()(N,{VDialog:O["a"]});var G=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-dialog",{attrs:{width:"600px",persistent:""},model:{value:t.insideValue,callback:function(e){t.insideValue=e},expression:"insideValue"}},[a("v-card",{staticClass:"fq-popup"},[a("v-app-bar",{staticClass:"pt-3 mb-5",attrs:{color:"rgba(0, 0, 0, 0)"}},[a("div",{staticClass:"text-center display-2 font-weight-bold"},[t._v(" Refer A Friend ")]),a("v-spacer"),a("v-btn",{attrs:{icon:""},on:{click:function(e){t.insideValue=!1}}},[a("v-icon",[t._v("mdi-close")])],1)],1),a("v-card-text",[a("v-text-field",{ref:"link",attrs:{outlined:"",readonly:"",success:"",value:t.link,"append-icon":t.copyIcon},on:{"click:append":t.copyLink}}),a("input",{attrs:{type:"hidden",id:"referral-code"},domProps:{value:t.link}}),a("v-card-actions",{staticClass:"d-flex justify-center"},[a("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(e){var i=e.on;return[a("v-btn",t._g({attrs:{fab:"",small:"",link:"",target:"_blank",href:t.tweetShareLink}},i),[a("v-icon",{attrs:{size:"24",color:"twitter"}},[t._v("mdi-twitter")])],1)]}}])},[t._v(" Share with Twitter ")])],1)],1)],1),a("v-snackbar",{attrs:{timeout:3e3,color:t.status},scopedSlots:t._u([{key:"action",fn:function(e){var i=e.attrs;return[a("v-btn",t._b({attrs:{dark:"",text:""},on:{click:function(e){t.snack=!1}}},"v-btn",i,!1),[t._v(" Close ")])]}}]),model:{value:t.snack,callback:function(e){t.snack=e},expression:"snack"}},[t._v(" "+t._s(t.message)+" ")])],1)},K=[],Q=(a("99af"),a("9911"),a("365c"),{name:"Referral",props:["value"],computed:{insideValue:{get:function(){return this.value},set:function(){this.$emit("update")}},copyIcon:function(){return this.copy?"mdi-content-paste":"mdi-content-copy"},link:function(){var t,e,a=(null===(t=this.$store.getters["auth/authUser"])||void 0===t?void 0:t.pk)||(null===(e=this.$store.getters["auth/authUser"])||void 0===e?void 0:e.id);return"".concat("https://test.fightquake.com","/rf/").concat(a)},tweetShareLink:function(){var t="https://twitter.com/intent/tweet?url=".concat(this.link,"&via=fightquake&text=Join me on FIGHTQUAKE to play fantasy MMA!&hashtags=ufc,fightquake,survival");return encodeURI(t)}},data:function(){return{copy:!1,message:"Copied",status:"warning",snack:!1}},methods:{copyLink:function(){this.copy=!0;var t=document.querySelector("#referral-code");t.setAttribute("type","text"),t.select();try{var e=document.execCommand("copy");this.message=e?"Copied":"Cannot copy",this.status=e?"success":"warning"}catch(i){this.message="Oops, unable to copy"}this.snack=!0,t.setAttribute("type","hidden"),window.getSelection().removeAllRanges();var a=this;setTimeout((function(){return a.copy=!1}),1e3)}}}),Z=Q,tt=a("40dc"),et=a("132d"),at=a("2db4"),it=a("2fa4"),nt=a("3a2f"),st=Object(x["a"])(Z,G,K,!1,null,null,null),ot=st.exports;y()(st,{VAppBar:tt["a"],VBtn:P["a"],VCard:k["a"],VCardActions:C["a"],VCardText:C["b"],VDialog:O["a"],VIcon:et["a"],VSnackbar:at["a"],VSpacer:it["a"],VTextField:z["a"],VTooltip:nt["a"]});var rt={name:"DashboardCoreAppBar",components:{Instruction:W,UserProfile:A,YourAccount:q,Referral:ot,AppBarItem:{render:function(t){var e=this;return t(u,{scopedSlots:{default:function(a){var i=a.hover;return t(d["a"],{attrs:e.$attrs,class:{"black--text":!i,"white--text secondary elevation-12":i},props:Object(s["a"])({activeClass:"",dark:i,link:!0},e.$attrs)},e.$slots.default)}}})}}},props:{value:{type:Boolean,default:!1}},data:function(){return{instructionDlg:!1,profileDlg:!1,referralDlg:!1,accountDlg:!1}},computed:Object(s["a"])(Object(s["a"])(Object(s["a"])(Object(s["a"])({},Object(p["d"])(["drawer","notifications"])),Object(p["d"])("auth",["authUser"])),Object(p["b"])("auth",["isAuthenticated"])),{},{notificationLengh:function(){return this.notifications.length<100?this.notifications.length:"99+"},isProfileDlg:function(){return this.$store.getters["auth/selectedUserId"]}}),mounted:function(){},methods:Object(s["a"])(Object(s["a"])({},Object(p["c"])({setDrawer:"SET_DRAWER"})),{},{goTo:function(t){"Logout"!==t?this.$router.push({name:t}):window.location.href="/pages/logout"},launchLogin:function(){this.$store.commit("auth/showLoginDlg")},logout:function(){this.$store.dispatch("auth/logout")},showInstruction:function(){this.instructionDlg=!0},showChat:function(){"Chat"!=this.$route.name&&this.$router.push({name:"Chat"})},showProfileDlg:function(){this.$store.dispatch("auth/loadProfile",this.authUser.pk||this.authUser.id)}})},lt=rt,ct=(a("b64c"),a("a9e3"),a("15fd")),ut=(a("ff44"),a("a9ad")),dt=a("7560"),pt=a("f40d"),ft=a("fe6c"),vt=a("80d2"),ht=Object(l["a"])(ut["a"],Object(ft["b"])(["left","bottom"]),dt["a"],r["a"],pt["a"]).extend({name:"v-badge",props:{avatar:Boolean,bordered:Boolean,color:{type:String,default:"primary"},content:{required:!1},dot:Boolean,label:{type:String,default:"$vuetify.badge"},icon:String,inline:Boolean,offsetX:[Number,String],offsetY:[Number,String],overlap:Boolean,tile:Boolean,transition:{type:String,default:"scale-rotate-transition"},value:{default:!0}},computed:{classes:function(){return Object(s["a"])({"v-badge--avatar":this.avatar,"v-badge--bordered":this.bordered,"v-badge--bottom":this.bottom,"v-badge--dot":this.dot,"v-badge--icon":null!=this.icon,"v-badge--inline":this.inline,"v-badge--left":this.left,"v-badge--overlap":this.overlap,"v-badge--tile":this.tile},this.themeClasses)},computedBottom:function(){return this.bottom?"auto":this.computedYOffset},computedLeft:function(){return this.isRtl?this.left?this.computedXOffset:"auto":this.left?"auto":this.computedXOffset},computedRight:function(){return this.isRtl?this.left?"auto":this.computedXOffset:this.left?this.computedXOffset:"auto"},computedTop:function(){return this.bottom?this.computedYOffset:"auto"},computedXOffset:function(){return this.calcPosition(this.offsetX)},computedYOffset:function(){return this.calcPosition(this.offsetY)},isRtl:function(){return this.$vuetify.rtl},offset:function(){return this.overlap?this.dot?8:12:this.dot?2:4},styles:function(){return this.inline?{}:{bottom:this.computedBottom,left:this.computedLeft,right:this.computedRight,top:this.computedTop}}},methods:{calcPosition:function(t){return"calc(100% - ".concat(Object(vt["g"])(t||this.offset),")")},genBadge:function(){var t=this.$vuetify.lang,e=this.$attrs["aria-label"]||t.t(this.label),a=this.setBackgroundColor(this.color,{staticClass:"v-badge__badge",style:this.styles,attrs:{"aria-atomic":this.$attrs["aria-atomic"]||"true","aria-label":e,"aria-live":this.$attrs["aria-live"]||"polite",title:this.$attrs.title,role:this.$attrs.role||"status"},directives:[{name:"show",value:this.isActive}]}),i=this.$createElement("span",a,[this.genBadgeContent()]);return this.transition?this.$createElement("transition",{props:{name:this.transition,origin:this.origin,mode:this.mode}},[i]):i},genBadgeContent:function(){if(!this.dot){var t=Object(vt["r"])(this,"badge");return t||(this.content?String(this.content):this.icon?this.$createElement(et["a"],this.icon):void 0)}},genBadgeWrapper:function(){return this.$createElement("span",{staticClass:"v-badge__wrapper"},[this.genBadge()])}},render:function(t){var e=[this.genBadgeWrapper()],a=[Object(vt["r"])(this)],i=this.$attrs,n=(i["aria-atomic"],i["aria-label"],i["aria-live"],i.role,i.title,Object(ct["a"])(i,["aria-atomic","aria-label","aria-live","role","title"]));return this.inline&&this.left?a.unshift(e):a.push(e),t("span",{staticClass:"v-badge",attrs:n,class:this.classes},a)}}),bt=a("8860"),gt=a("1800"),mt=a("5d23"),xt=a("1baa"),_t=a("e449"),yt=a("2a7f"),wt=Object(x["a"])(lt,i,n,!1,null,null,null);e["default"]=wt.exports;y()(wt,{VAppBar:tt["a"],VBadge:ht,VBtn:P["a"],VDivider:$["a"],VIcon:et["a"],VList:bt["a"],VListItem:d["a"],VListItemAction:gt["a"],VListItemActionText:mt["a"],VListItemContent:mt["b"],VListItemGroup:xt["a"],VListItemSubtitle:mt["c"],VMenu:_t["a"],VSpacer:it["a"],VToolbarTitle:yt["a"],VTooltip:nt["a"]})},a134:function(t,e,a){var i=a("24fb");e=i(!1),e.push([t.i,".display-box[data-v-2765517f]{text-align:left!important;margin:.5rem 0 0 1rem}.displayname[data-v-2765517f]{font-size:24px;font-weight:500;text-transform:capitalize}.subtitle[data-v-2765517f]{font-size:14px;font-weight:500}.initials[data-v-2765517f]{font-size:36px;font-weight:400;line-height:2rem;letter-spacing:normal!important;font-family:Roboto,sans-serif!important}.lock-icon[data-v-2765517f]{position:absolute;bottom:0;left:0;width:100%}.stats-title[data-v-2765517f]{margin:.2rem 0 .5rem;font-size:14px;text-transform:uppercase;font-weight:700}.stats-blocks[data-v-2765517f]{display:-webkit-box;display:-ms-flexbox;display:flex}.stats-blocks .well[data-v-2765517f]{padding:19px 10px;font-size:12px;text-align:center;background-color:#181818;height:100%;border-radius:3px;margin-right:1.5rem;min-width:100px}.stats-blocks .well .stats-value[data-v-2765517f]{font-size:18px;font-weight:700}",""]),t.exports=e},b64c:function(t,e,a){"use strict";a("e6c5")},b709:function(t,e,a){"use strict";var i=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-card",{staticClass:"fq-popup"},[a("v-card-title",[a("b",{staticClass:"display-2"},[t._v("Instructions")])]),a("v-card-text",[a("ul",{staticClass:"instruction-list"},t._l(t.instructions,(function(e,i){return a("li",[t._v(t._s(i+1)+". "+t._s(e))])})),0)]),a("v-card-title",[a("b",{staticClass:"display-2"},[t._v("Rules")])]),a("v-card-text",[a("ul",{staticClass:"instruction-list"},t._l(t.rules,(function(e,i){return a("li",[t._v(t._s(i+1)+". "+t._s(e))])})),0)])],1)},n=[],s={name:"InstructionBody",data:function(){return{instructions:["Choose fighters","Hope they all survive"],rules:["User can pick any number of fighters. If any of them get finished, user is eliminated.","Out of all surviving entries, the user with the most surviving fighters, wins the contest.","If there is a tie, the winner is the entry with the most winning fighters.","You are allowed to resubmit your team. 1 team per person."]}}},o=s,r=a("2877"),l=a("6544"),c=a.n(l),u=a("b0af"),d=a("99d9"),p=Object(r["a"])(o,i,n,!1,null,null,null);e["a"]=p.exports;c()(p,{VCard:u["a"],VCardText:d["b"],VCardTitle:d["c"]})},deaa:function(t,e,a){"use strict";a("0ea9")},e6c5:function(t,e,a){var i=a("47d5");"string"===typeof i&&(i=[[t.i,i,""]]),i.locals&&(t.exports=i.locals);var n=a("499e").default;n("0b1764cc",i,!0,{sourceMap:!1,shadowMode:!1})},ff44:function(t,e,a){var i=a("89c2");"string"===typeof i&&(i=[[t.i,i,""]]),i.locals&&(t.exports=i.locals);var n=a("499e").default;n("266a5314",i,!0,{sourceMap:!1,shadowMode:!1})}}]);
//# sourceMappingURL=chunk-35edd1a3.3117b52c.js.map