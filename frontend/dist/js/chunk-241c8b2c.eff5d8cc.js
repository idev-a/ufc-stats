(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-241c8b2c","chunk-55403d0e"],{"0de5":function(t,e,i){"use strict";i("d81d"),i("fb6a"),i("a9e3"),i("96a9");var n=i("24b2"),s=i("f977"),r=i("80d2");e["a"]=n["a"].extend({name:"v-virtual-scroll",directives:{Scroll:s["b"]},props:{bench:{type:[Number,String],default:0},itemHeight:{type:[Number,String],required:!0},items:{type:Array,default:function(){return[]}}},data:function(){return{first:0,last:0,scrollTop:0}},computed:{__bench:function(){return parseInt(this.bench,10)},__itemHeight:function(){return parseInt(this.itemHeight,10)},firstToRender:function(){return Math.max(0,this.first-this.__bench)},lastToRender:function(){return Math.min(this.items.length,this.last+this.__bench)}},watch:{height:"onScroll",itemHeight:"onScroll"},mounted:function(){this.last=this.getLast(0)},methods:{getChildren:function(){return this.items.slice(this.firstToRender,this.lastToRender).map(this.genChild)},genChild:function(t,e){e+=this.firstToRender;var i=Object(r["g"])(e*this.__itemHeight);return this.$createElement("div",{staticClass:"v-virtual-scroll__item",style:{top:i},key:e},Object(r["r"])(this,"default",{index:e,item:t}))},getFirst:function(){return Math.floor(this.scrollTop/this.__itemHeight)},getLast:function(t){var e=parseInt(this.height||0,10)||this.$el.clientHeight;return t+Math.ceil(e/this.__itemHeight)},onScroll:function(){this.scrollTop=this.$el.scrollTop,this.first=this.getFirst(),this.last=this.getLast(this.first)}},render:function(t){var e=t("div",{staticClass:"v-virtual-scroll__container",style:{height:Object(r["g"])(this.items.length*this.__itemHeight)}},this.getChildren());return t("div",{staticClass:"v-virtual-scroll",style:this.measurableStyles,directives:[{name:"scroll",modifiers:{self:!0},value:this.onScroll}],on:this.$listeners},[e])}})},"28f7":function(t,e,i){"use strict";i("e8ab")},"61b9":function(t,e,i){"use strict";i("6a0b")},"6a0b":function(t,e,i){},"8ed3":function(t,e,i){"use strict";i.r(e);var n=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("v-container",{staticClass:"pa-0",attrs:{id:"contest",fluid:"",tag:"section"}},[i("v-card",{staticClass:"grey lighten-4 mt-0 pa-0",class:{"fixed-card":t.$vuetify.breakpoint.smAndUp},attrs:{loading:t.loading}},[i("v-card-title",{staticClass:"justify-center font-weight-medium mb-md-3"},[t.event?i("div",{staticClass:"text-center"},[i("div",[t._v(t._s(this.event.name))]),i("div",{staticClass:"subtitle-2"},[t._v(t._s(t._f("beautifyDate")(this.event.date)))])]):t._e()]),i("v-card-text",{staticClass:"pb-0"},[i("v-virtual-scroll",{attrs:{items:t.bouts,"item-height":50,height:"300"},scopedSlots:t._u([{key:"default",fn:function(e){var n=e.item;return[i("toggle-switch",{key:n.id,attrs:{options:t.myOptions(n)},model:{value:t.contests[n.id],callback:function(e){t.$set(t.contests,n.id,e)},expression:"contests[item.id]"}})]}}])}),i("div",{staticClass:"d-flex justify-center w-100"},[i("v-btn",{staticClass:"grey darken-4 mt-2 mb-2",attrs:{disabled:t.loading||!t.event,small:""},on:{click:t.submit}},[t._v("Submit")])],1)],1)],1),i("v-snackbar",{attrs:{timeout:3e3,color:t.snackbar.status},scopedSlots:t._u([{key:"action",fn:function(e){var n=e.attrs;return[i("v-btn",t._b({attrs:{dark:"",text:""},on:{click:function(e){t.snackbar.snack=!1}}},"v-btn",n,!1),[t._v(" Close ")])]}}]),model:{value:t.snackbar.snack,callback:function(e){t.$set(t.snackbar,"snack",e)},expression:"snackbar.snack"}},[t._v(" "+t._s(t.snackbar.message)+" ")])],1)},s=[],r=(i("4de4"),i("b0c0"),i("96cf"),i("1da1")),a=i("5530"),o=i("b899"),l=i("e0eb"),c=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("v-card",[i("ul",{staticClass:"toggle-switch",class:{square:t.defaultOptions.layout.squareCorners},style:t.toggleSwitchStyle},t._l(t.defaultOptions.items.labels,(function(e,n){return i("li",{key:n,style:t.itemStyle},[i("input",{attrs:{disabled:t.defaultOptions.items.disabled||t.disabled,id:e.id+t.group,name:t.name,type:"radio"},domProps:{value:e.id},on:{click:t.toggle}}),e.id==t.selectedItem?i("label",{staticClass:"selected",class:{active:!t.defaultOptions.items.disabled||t.disabled},style:t.labelStyleSelected(e.color,e.backgroundColor),attrs:{for:e.id+t.group,type:"radio"}},[t._v(" "+t._s(e.name)+" ")]):i("label",{class:{active:!t.defaultOptions.items.disabled||t.disabled},style:t.labelStyle,attrs:{for:e.id+t.group,type:"radio"}},[t._v(" "+t._s(e.name)+" ")])])})),0)])},u=[],d=(i("ac1f"),i("5319"),i("53ca")),h=function(t){return t+"s"},f=function(t){return t+"rem"},p={name:"ToggleSwitch",props:{options:{type:Object,required:!1},value:{type:String,required:!1},name:{type:String,required:!1},group:{type:String,required:!1,default:""},disabled:{type:Boolean,required:!1,default:!1}},created:function(){this.defaultOptions={layout:{color:"black",backgroundColor:"lightgray",selectedColor:"white",selectedBackgroundColor:"green",borderColor:"gray",fontFamily:"Arial",fontWeight:"normal",fontWeightSelected:"bold",squareCorners:!1,noBorder:!1},size:{fontSize:.8,height:2.25,width:8},items:{delay:.4,preSelected:"unknown",disabled:!1,labels:[{name:"Off",color:"white",backgroundColor:"red"},{name:"On",color:"white",backgroundColor:"green"}]}}},mounted:function(){null!==this.options&&void 0!==this.options&&this.mergeDefaultOptionsWithProp(this.options),"unknown"!==this.defaultOptions.items.preSelected?(this.selectedItem=this.defaultOptions.items.preSelected,this.$emit("input",this.selectedItem)):this.value&&(this.selectedItem=this.value,this.$emit("input",this.selectedItem))},data:function(){return{selected:!1,selectedItem:"unknown",defaultOptions:Object}},computed:{toggleSwitchStyle:function(){return{"min-width":f(this.defaultOptions.size.width),"min-height":f(this.defaultOptions.size.height)}},itemStyle:function(){return{width:f(this.defaultOptions.size.width),height:f(this.defaultOptions.size.height),fontFamily:this.defaultOptions.layout.fontFamily,fontSize:f(this.defaultOptions.size.fontSize),textAlign:"center"}},labelStyle:function(){return{padding:f(this.defaultOptions.size.padding),borderColor:this.defaultOptions.layout.noBorder?"transparent":this.defaultOptions.layout.borderColor,backgroundColor:this.defaultOptions.layout.backgroundColor,color:this.defaultOptions.layout.color,fontWeight:this.defaultOptions.layout.fontWeight,transition:h(this.defaultOptions.items.delay)}}},methods:{toggle:function(t){this.defaultOptions.items.disabled||(this.selected=!0,this.selectedItem=t.target.id.replace(this.group,""),this.$emit("selected",this.selected),this.$emit("input",this.selectedItem),this.$emit("change",{value:t.target.id.replace(this.group,""),srcEvent:t}))},labelStyleSelected:function(t,e){return{padding:f(this.defaultOptions.size.padding),borderColor:this.defaultOptions.layout.noBorder?"transparent":this.defaultOptions.layout.borderColor,fontWeight:this.defaultOptions.layout.fontWeightSelected,backgroundColor:void 0!==e?e:this.defaultOptions.layout.selectedBackgroundColor,color:void 0!==t?t:this.defaultOptions.layout.selectedColor,transition:h(this.defaultOptions.items.delay)}},mergeDefaultOptionsWithProp:function(t){var e=this.defaultOptions;for(var i in t)if(null!==t[i]&&"object"===Object(d["a"])(t[i]))for(var n in t[i])void 0!==t[i][n]&&null!==t[i][n]&&(e[i][n]=t[i][n]);else e[i]=t[i]}},watch:{value:function(t){this.selectedItem=t},options:function(t){null!==t&&void 0!==t&&this.mergeDefaultOptionsWithProp(t)}}},g=p,m=(i("28f7"),i("2877")),b=i("6544"),v=i.n(b),y=i("b0af"),O=Object(m["a"])(g,c,u,!1,null,"4583c6b9",null),k=O.exports;v()(O,{VCard:y["a"]});var _=i("2f62"),S={name:"Selection",components:{ToggleSwitch:k},data:function(){return{loading:!1,bouts:[],event:null,fighters:[],selectedItem:-1,contests:{},snackbar:{snack:!1,message:"",status:"success"}}},watch:{contests:{handler:function(t){},deep:!0}},computed:Object(a["a"])(Object(a["a"])(Object(a["a"])({},Object(_["d"])("auth",["authUser"])),Object(_["b"])("auth",["isAuthenticated"])),{},{bgHeight:function(){return this.$vuetify.breakpoint.height-147}}),filters:{beautifyDate:l["b"]},mounted:function(){var t=this;return Object(r["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return t.loading=!0,e.next=3,t.getFighters();case 3:return e.next=5,t.getLatestBouts();case 5:t.loading=!1;case 6:case"end":return e.stop()}}),e)})))()},methods:{authenticate:function(t){this.response=null;var e=this;this.$auth.authenticate(t).then((function(t){e.isAuthenticated=e.$auth.isAuthenticated(),e.response=t.body.profile})).catch((function(t){e.isAuthenticated=e.$auth.isAuthenticated(),e.response=t}))},getLatestBouts:function(){var t=this;return Object(r["a"])(regeneratorRuntime.mark((function e(){var i,n;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,o["a"].get("api/latest_event");case 2:i=e.sent,n=i.data,t.bouts=n.bouts,t.event=n.event;case 6:case"end":return e.stop()}}),e)})))()},getFighters:function(){var t=this;return Object(r["a"])(regeneratorRuntime.mark((function e(){var i,n;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,o["a"].get("api/fighters");case 2:i=e.sent,n=i.data,t.fighters=n.results;case 5:case"end":return e.stop()}}),e)})))()},_fighter:function(t){var e=this.fighters.filter((function(e){return e.id==t}));return e[0]},myOptions:function(t){var e=this._fighter(t.fighter1),i=this._fighter(t.fighter2);return{items:{delay:.4,preSelected:"unknown",disabled:!1,labels:[{name:e.name,id:e.id,color:"white",backgroundColor:"green"},{name:i.name,id:i.id,color:"white",backgroundColor:"green"}]}}},submit:function(){var t=this;return Object(r["a"])(regeneratorRuntime.mark((function e(){var i,n,s,r,l;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:if(t.isAuthenticated){e.next=3;break}return window.location.href="/pages/login",e.abrupt("return");case 3:for(s in i=t.bouts[0].event,n=[],t.contests)n.push({event:i,user:t.authUser.pk,bout:s,fighter:t.contests[s]});return e.next=8,o["a"].post("api/entries/",n);case 8:r=e.sent,l=r.data,t.snackbar=Object(a["a"])(Object(a["a"])({},l),{},{snack:!0});case 11:case"end":return e.stop()}}),e)})))()}}},w=S,C=(i("61b9"),i("8336")),j=i("99d9"),x=i("a523"),$=i("2db4"),I=i("0de5"),R=Object(m["a"])(w,n,s,!1,null,null,null);e["default"]=R.exports;v()(R,{VBtn:C["a"],VCard:y["a"],VCardText:j["b"],VCardTitle:j["c"],VContainer:x["a"],VSnackbar:$["a"],VVirtualScroll:I["a"]})},"96a9":function(t,e,i){},a523:function(t,e,i){"use strict";i("99af"),i("4de4"),i("b64b"),i("2ca0"),i("20f6"),i("4b85"),i("a15b"),i("498a");var n=i("2b0e");function s(t){return n["a"].extend({name:"v-".concat(t),functional:!0,props:{id:String,tag:{type:String,default:"div"}},render:function(e,i){var n=i.props,s=i.data,r=i.children;s.staticClass="".concat(t," ").concat(s.staticClass||"").trim();var a=s.attrs;if(a){s.attrs={};var o=Object.keys(a).filter((function(t){if("slot"===t)return!1;var e=a[t];return t.startsWith("data-")?(s.attrs[t]=e,!1):e||"string"===typeof e}));o.length&&(s.staticClass+=" ".concat(o.join(" ")))}return n.id&&(s.domProps=s.domProps||{},s.domProps.id=n.id),e(n.tag,s,r)}})}var r=i("d9f7");e["a"]=s("container").extend({name:"v-container",functional:!0,props:{id:String,tag:{type:String,default:"div"},fluid:{type:Boolean,default:!1}},render:function(t,e){var i,n=e.props,s=e.data,a=e.children,o=s.attrs;return o&&(s.attrs={},i=Object.keys(o).filter((function(t){if("slot"===t)return!1;var e=o[t];return t.startsWith("data-")?(s.attrs[t]=e,!1):e||"string"===typeof e}))),n.id&&(s.domProps=s.domProps||{},s.domProps.id=n.id),t(n.tag,Object(r["a"])(s,{staticClass:"container",class:Array({"container--fluid":n.fluid}).concat(i||[])}),a)}})},e8ab:function(t,e,i){},f977:function(t,e,i){"use strict";i.d(e,"a",(function(){return a}));var n=i("53ca");function s(t,e){var i=e.modifiers||{},s=i.self,r=void 0!==s&&s,a=e.value,o="object"===Object(n["a"])(a)&&a.options||{passive:!0},l="function"===typeof a||"handleEvent"in a?a:a.handler,c=r?t:e.arg?document.querySelector(e.arg):window;c&&(c.addEventListener("scroll",l,o),t._onScroll={handler:l,options:o,target:r?void 0:c})}function r(t){if(t._onScroll){var e=t._onScroll,i=e.handler,n=e.options,s=e.target,r=void 0===s?t:s;r.removeEventListener("scroll",i,n),delete t._onScroll}}var a={inserted:s,unbind:r};e["b"]=a}}]);
//# sourceMappingURL=chunk-241c8b2c.eff5d8cc.js.map