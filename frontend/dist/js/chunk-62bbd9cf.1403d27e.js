(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-62bbd9cf"],{"169a":function(t,e,n){"use strict";n("7db0"),n("caad"),n("45fc"),n("a9e3"),n("2532"),n("498a");var i=n("5530"),a=n("2909"),s=n("ade3"),o=(n("368e"),n("480e")),r=n("4ad4"),c=n("b848"),l=n("75eb"),d=n("1abc"),u=n("80d2"),h=n("2b0e"),v=h["a"].extend().extend({name:"overlayable",props:{hideOverlay:Boolean,overlayColor:String,overlayOpacity:[Number,String]},data:function(){return{animationFrame:0,overlay:null}},watch:{hideOverlay:function(t){this.isActive&&(t?this.removeOverlay():this.genOverlay())}},beforeDestroy:function(){this.removeOverlay()},methods:{createOverlay:function(){var t=new d["a"]({propsData:{absolute:this.absolute,value:!1,color:this.overlayColor,opacity:this.overlayOpacity}});t.$mount();var e=this.absolute?this.$el.parentNode:document.querySelector("[data-app]");e&&e.insertBefore(t.$el,e.firstChild),this.overlay=t},genOverlay:function(){var t=this;if(this.hideScroll(),!this.hideOverlay)return this.overlay||this.createOverlay(),this.animationFrame=requestAnimationFrame((function(){t.overlay&&(void 0!==t.activeZIndex?t.overlay.zIndex=String(t.activeZIndex-1):t.$el&&(t.overlay.zIndex=Object(u["t"])(t.$el)),t.overlay.value=!0)})),!0},removeOverlay:function(){var t=this,e=!(arguments.length>0&&void 0!==arguments[0])||arguments[0];this.overlay&&(Object(u["a"])(this.overlay.$el,"transitionend",(function(){t.overlay&&t.overlay.$el&&t.overlay.$el.parentNode&&!t.overlay.value&&(t.overlay.$el.parentNode.removeChild(t.overlay.$el),t.overlay.$destroy(),t.overlay=null)})),cancelAnimationFrame(this.animationFrame),this.overlay.value=!1),e&&this.showScroll()},scrollListener:function(t){if("keydown"===t.type){if(["INPUT","TEXTAREA","SELECT"].includes(t.target.tagName)||t.target.isContentEditable)return;var e=[u["w"].up,u["w"].pageup],n=[u["w"].down,u["w"].pagedown];if(e.includes(t.keyCode))t.deltaY=-1;else{if(!n.includes(t.keyCode))return;t.deltaY=1}}(t.target===this.overlay||"keydown"!==t.type&&t.target===document.body||this.checkPath(t))&&t.preventDefault()},hasScrollbar:function(t){if(!t||t.nodeType!==Node.ELEMENT_NODE)return!1;var e=window.getComputedStyle(t);return["auto","scroll"].includes(e.overflowY)&&t.scrollHeight>t.clientHeight},shouldScroll:function(t,e){return 0===t.scrollTop&&e<0||t.scrollTop+t.clientHeight===t.scrollHeight&&e>0},isInside:function(t,e){return t===e||null!==t&&t!==document.body&&this.isInside(t.parentNode,e)},checkPath:function(t){var e=t.path||this.composedPath(t),n=t.deltaY;if("keydown"===t.type&&e[0]===document.body){var i=this.$refs.dialog,a=window.getSelection().anchorNode;return!(i&&this.hasScrollbar(i)&&this.isInside(a,i))||this.shouldScroll(i,n)}for(var s=0;s<e.length;s++){var o=e[s];if(o===document)return!0;if(o===document.documentElement)return!0;if(o===this.$refs.content)return!0;if(this.hasScrollbar(o))return this.shouldScroll(o,n)}return!0},composedPath:function(t){if(t.composedPath)return t.composedPath();var e=[],n=t.target;while(n){if(e.push(n),"HTML"===n.tagName)return e.push(document),e.push(window),e;n=n.parentElement}return e},hideScroll:function(){this.$vuetify.breakpoint.smAndDown?document.documentElement.classList.add("overflow-y-hidden"):(Object(u["b"])(window,"wheel",this.scrollListener,{passive:!1}),window.addEventListener("keydown",this.scrollListener))},showScroll:function(){document.documentElement.classList.remove("overflow-y-hidden"),window.removeEventListener("wheel",this.scrollListener),window.removeEventListener("keydown",this.scrollListener)}}}),f=n("e4d3"),m=n("21be"),g=n("f2e7"),p=n("a293"),b=n("58df"),y=n("d9bd"),w=Object(b["a"])(r["a"],c["a"],l["a"],v,f["a"],m["a"],g["a"]);e["a"]=w.extend({name:"v-dialog",directives:{ClickOutside:p["a"]},props:{dark:Boolean,disabled:Boolean,fullscreen:Boolean,light:Boolean,maxWidth:{type:[String,Number],default:"none"},noClickAnimation:Boolean,origin:{type:String,default:"center center"},persistent:Boolean,retainFocus:{type:Boolean,default:!0},scrollable:Boolean,transition:{type:[String,Boolean],default:"dialog-transition"},width:{type:[String,Number],default:"auto"}},data:function(){return{activatedBy:null,animate:!1,animateTimeout:-1,isActive:!!this.value,stackMinZIndex:200,previousActiveElement:null}},computed:{classes:function(){var t;return t={},Object(s["a"])(t,"v-dialog ".concat(this.contentClass).trim(),!0),Object(s["a"])(t,"v-dialog--active",this.isActive),Object(s["a"])(t,"v-dialog--persistent",this.persistent),Object(s["a"])(t,"v-dialog--fullscreen",this.fullscreen),Object(s["a"])(t,"v-dialog--scrollable",this.scrollable),Object(s["a"])(t,"v-dialog--animated",this.animate),t},contentClasses:function(){return{"v-dialog__content":!0,"v-dialog__content--active":this.isActive}},hasActivator:function(){return Boolean(!!this.$slots.activator||!!this.$scopedSlots.activator)}},watch:{isActive:function(t){var e;t?(this.show(),this.hideScroll()):(this.removeOverlay(),this.unbind(),null==(e=this.previousActiveElement)||e.focus())},fullscreen:function(t){this.isActive&&(t?(this.hideScroll(),this.removeOverlay(!1)):(this.showScroll(),this.genOverlay()))}},created:function(){this.$attrs.hasOwnProperty("full-width")&&Object(y["e"])("full-width",this)},beforeMount:function(){var t=this;this.$nextTick((function(){t.isBooted=t.isActive,t.isActive&&t.show()}))},beforeDestroy:function(){"undefined"!==typeof window&&this.unbind()},methods:{animateClick:function(){var t=this;this.animate=!1,this.$nextTick((function(){t.animate=!0,window.clearTimeout(t.animateTimeout),t.animateTimeout=window.setTimeout((function(){return t.animate=!1}),150)}))},closeConditional:function(t){var e=t.target;return!(this._isDestroyed||!this.isActive||this.$refs.content.contains(e)||this.overlay&&e&&!this.overlay.$el.contains(e))&&this.activeZIndex>=this.getMaxZIndex()},hideScroll:function(){this.fullscreen?document.documentElement.classList.add("overflow-y-hidden"):v.options.methods.hideScroll.call(this)},show:function(){var t=this;!this.fullscreen&&!this.hideOverlay&&this.genOverlay(),this.$nextTick((function(){t.$nextTick((function(){t.previousActiveElement=document.activeElement,t.$refs.content.focus(),t.bind()}))}))},bind:function(){window.addEventListener("focusin",this.onFocusin)},unbind:function(){window.removeEventListener("focusin",this.onFocusin)},onClickOutside:function(t){this.$emit("click:outside",t),this.persistent?this.noClickAnimation||this.animateClick():this.isActive=!1},onKeydown:function(t){if(t.keyCode===u["w"].esc&&!this.getOpenDependents().length)if(this.persistent)this.noClickAnimation||this.animateClick();else{this.isActive=!1;var e=this.getActivator();this.$nextTick((function(){return e&&e.focus()}))}this.$emit("keydown",t)},onFocusin:function(t){if(t&&this.retainFocus){var e=t.target;if(e&&![document,this.$refs.content].includes(e)&&!this.$refs.content.contains(e)&&this.activeZIndex>=this.getMaxZIndex()&&!this.getOpenDependentElements().some((function(t){return t.contains(e)}))){var n=this.$refs.content.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'),i=Object(a["a"])(n).find((function(t){return!t.hasAttribute("disabled")}));i&&i.focus()}}},genContent:function(){var t=this;return this.showLazyContent((function(){return[t.$createElement(o["a"],{props:{root:!0,light:t.light,dark:t.dark}},[t.$createElement("div",{class:t.contentClasses,attrs:Object(i["a"])({role:"document",tabindex:t.isActive?0:void 0},t.getScopeIdAttrs()),on:{keydown:t.onKeydown},style:{zIndex:t.activeZIndex},ref:"content"},[t.genTransition()])])]}))},genTransition:function(){var t=this.genInnerContent();return this.transition?this.$createElement("transition",{props:{name:this.transition,origin:this.origin,appear:!0}},[t]):t},genInnerContent:function(){var t={class:this.classes,ref:"dialog",directives:[{name:"click-outside",value:{handler:this.onClickOutside,closeConditional:this.closeConditional,include:this.getOpenDependentElements}},{name:"show",value:this.isActive}],style:{transformOrigin:this.origin}};return this.fullscreen||(t.style=Object(i["a"])(Object(i["a"])({},t.style),{},{maxWidth:"none"===this.maxWidth?void 0:Object(u["g"])(this.maxWidth),width:"auto"===this.width?void 0:Object(u["g"])(this.width)})),this.$createElement("div",t,this.getContentSlot())}},render:function(t){return t("div",{staticClass:"v-dialog__container",class:{"v-dialog__container--attached":""===this.attach||!0===this.attach||"attach"===this.attach},attrs:{role:"dialog"}},[this.genActivator(),this.genContent()])}})},"1abc":function(t,e,n){"use strict";var i=n("a797");e["a"]=i["a"]},"368e":function(t,e,n){},"3c93":function(t,e,n){},"64b5":function(t,e,n){},"8fb6":function(t,e,n){"use strict";n("64b5")},"905f":function(t,e,n){"use strict";n.r(e);var i=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-container",{staticClass:"d-flex justify-center",attrs:{id:"contest",fluid:"",tag:"section"}},[n("v-card",{staticClass:"px-5",attrs:{loading:t.loading,"min-width":"60%"}},[n("v-card-title",{staticClass:"justify-center font-weight-medium mb-md-3 mt-5"},[n("div",{staticClass:"text-center"},[n("div",[t._v(t._s(this.event.name))]),n("div",{staticClass:"subtitle-2"},[t._v(t._s(t._f("beautifyDate")(this.event.date)))])])]),n("v-card-text",[n("v-tabs",{attrs:{"align-with-title":"","background-color":"transparent",color:"basil",grow:""},model:{value:t.tab,callback:function(e){t.tab=e},expression:"tab"}},[n("v-tab",[t._v(" Fights ")]),n("v-tab",[t._v(" Entries ")])],1),n("v-tabs-items",{model:{value:t.tab,callback:function(e){t.tab=e},expression:"tab"}},[n("v-tab-item",[n("v-card",{attrs:{color:"basil",flat:""}},[n("v-card-title",[n("v-text-field",{staticClass:"mb-5",attrs:{"append-icon":"mdi-magnify",label:"Search",clearable:"","single-line":"","hide-details":""},model:{value:t.boutSearch,callback:function(e){t.boutSearch=e},expression:"boutSearch"}}),n("v-spacer")],1),n("v-card-text",[n("v-data-table",{attrs:{items:t.bouts,loading:t.loading,headers:t.boutHeaders,"items-per-page":5,"fixed-header":"","item-key":"id",search:t.boutSearch},scopedSlots:t._u([{key:"item.fighter1",fn:function(e){var i=e.item;return[n("div",{staticClass:"contest-item",class:{"winner-item":i.fighter1==i.winner,"loser-item":i.fighter1==i.loser}},[n("b",[t._v(t._s(i.fighter1))])])]}},{key:"item.entries_1",fn:function(e){var i=e.item;return[n("span",[n("a",{attrs:{href:"#"},on:{click:function(e){return t.gotoEntry(i,i.entries_1)}}},[t._v(t._s(i.entries_1.length))])])]}},{key:"item.fighter2",fn:function(e){var i=e.item;return[n("div",{staticClass:"contest-item",class:{"winner-item":i.fighter2==i.winner,"loser-item":i.fighter2==i.loser}},[n("b",[t._v(t._s(i.fighter2))])])]}},{key:"item.entries_2",fn:function(e){var i=e.item;return[i.entries_2.length?n("a",{attrs:{href:""},on:{click:function(e){return t.gotoEntry(i,i.entries_2)}}},[t._v(t._s(i.entries_2.length))]):n("span",[t._v(t._s(i.entries_2.length))])]}}])})],1)],1)],1)],1)],1)],1),n("v-dialog",{attrs:{"max-width":"680"},model:{value:t.entryDlg,callback:function(e){t.entryDlg=e},expression:"entryDlg"}},[n("v-card",{attrs:{color:"basil",flat:""}},[n("v-card-title",[t._v(" "+t._s(t.curBout)+" ")]),n("v-card-text",[n("div",{staticClass:"d-flex"},[n("v-text-field",{staticClass:"mb-5",attrs:{"append-icon":"mdi-magnify",label:"Search",clearable:"","single-line":"","hide-details":""},model:{value:t.entrySearch,callback:function(e){t.entrySearch=e},expression:"entrySearch"}}),n("v-spacer")],1),n("v-data-table",{attrs:{items:t.entries,loading:t.loading,headers:t.entryHeaders,"items-per-page":5,"fixed-header":"","item-key":"id",search:t.entrySearch}})],1)],1)],1)],1)},a=[],s=(n("99af"),n("d3b7"),n("ddb0"),n("96cf"),n("1da1")),o=n("ade3"),r=n("b899"),c={getEntries:function(t){return r["a"].post("/api/entries/get_entries/",t)},getLatestContests:function(){return r["a"].get("api/entries/contest")}},l=n("e0eb"),d={name:"Contest",data:function(){var t;return t={loading:!1,contests:[],event:"",boutSearch:"",entrySearch:"",tab:null,boutHeaders:[{text:"Fighter1",value:"fighter1"},{text:"Entries",value:"entries_1"},{text:"Fighter2",value:"fighter2"},{text:"Entries",value:"entries_2"},{text:"Method",value:"method"},{text:"Round",value:"round"},{text:"Time",value:"time"}],bouts:[],entryDlg:!1,curBout:"",entries:[]},Object(o["a"])(t,"entrySearch",""),Object(o["a"])(t,"entryHeaders",[{text:"Event",value:"event"},{text:"User",value:"user"}]),t},filters:{beautifyDate:l["a"]},mounted:function(){this.getLatestContest()},methods:{getLatestContest:function(){var t=this;return Object(s["a"])(regeneratorRuntime.mark((function e(){var n,i;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return t.loading=!0,e.next=3,c.getLatestContests();case 3:n=e.sent,i=n.data,t.bouts=i.bouts,t.event=i.event,t.loading=!1;case 8:case"end":return e.stop()}}),e)})))()},gotoEntry:function(t,e){var n=this;return Object(s["a"])(regeneratorRuntime.mark((function i(){var a,s;return regeneratorRuntime.wrap((function(i){while(1)switch(i.prev=i.next){case 0:return n.entryDlg=!0,n.curBout="".concat(t.fighter1," vs. ").concat(t.fighter2),i.next=4,c.getEntries(e);case 4:a=i.sent,s=a.data,n.entries=s.entries;case 7:case"end":return i.stop()}}),i)})))()}}},u=d,h=(n("8fb6"),n("2877")),v=n("6544"),f=n.n(v),m=n("b0af"),g=n("99d9"),p=n("a523"),b=n("8fea"),y=n("169a"),w=n("2fa4"),x=n("71a3"),C=n("9d65"),T=n("4e82"),O=n("c3f0"),k=n("80d2"),S=n("58df"),_=Object(S["a"])(C["a"],Object(T["a"])("windowGroup","v-window-item","v-window")),E=_.extend().extend().extend({name:"v-window-item",directives:{Touch:O["a"]},props:{disabled:Boolean,reverseTransition:{type:[Boolean,String],default:void 0},transition:{type:[Boolean,String],default:void 0},value:{required:!1}},data:function(){return{isActive:!1,inTransition:!1}},computed:{classes:function(){return this.groupClasses},computedTransition:function(){return this.windowGroup.internalReverse?"undefined"!==typeof this.reverseTransition?this.reverseTransition||"":this.windowGroup.computedTransition:"undefined"!==typeof this.transition?this.transition||"":this.windowGroup.computedTransition}},methods:{genDefaultSlot:function(){return this.$slots.default},genWindowItem:function(){return this.$createElement("div",{staticClass:"v-window-item",class:this.classes,directives:[{name:"show",value:this.isActive}],on:this.$listeners},this.genDefaultSlot())},onAfterTransition:function(){this.inTransition&&(this.inTransition=!1,this.windowGroup.transitionCount>0&&(this.windowGroup.transitionCount--,0===this.windowGroup.transitionCount&&(this.windowGroup.transitionHeight=void 0)))},onBeforeTransition:function(){this.inTransition||(this.inTransition=!0,0===this.windowGroup.transitionCount&&(this.windowGroup.transitionHeight=Object(k["g"])(this.windowGroup.$el.clientHeight)),this.windowGroup.transitionCount++)},onTransitionCancelled:function(){this.onAfterTransition()},onEnter:function(t){var e=this;this.inTransition&&this.$nextTick((function(){e.computedTransition&&e.inTransition&&(e.windowGroup.transitionHeight=Object(k["g"])(t.clientHeight))}))}},render:function(t){var e=this;return t("transition",{props:{name:this.computedTransition},on:{beforeEnter:this.onBeforeTransition,afterEnter:this.onAfterTransition,enterCancelled:this.onTransitionCancelled,beforeLeave:this.onBeforeTransition,afterLeave:this.onAfterTransition,leaveCancelled:this.onTransitionCancelled,enter:this.onEnter}},this.showLazyContent((function(){return[e.genWindowItem()]})))}}),$=E.extend({name:"v-tab-item",props:{id:String},methods:{genWindowItem:function(){var t=E.options.methods.genWindowItem.call(this);return t.data.domProps=t.data.domProps||{},t.data.domProps.id=this.id||this.value,t}}}),A=n("fe57"),j=n("aac8"),I=n("8654"),B=Object(h["a"])(u,i,a,!1,null,null,null);e["default"]=B.exports;f()(B,{VCard:m["a"],VCardText:g["b"],VCardTitle:g["c"],VContainer:p["a"],VDataTable:b["a"],VDialog:y["a"],VSpacer:w["a"],VTab:x["a"],VTabItem:$,VTabs:A["a"],VTabsItems:j["a"],VTextField:I["a"]})},a797:function(t,e,n){"use strict";n("a9e3");var i=n("5530"),a=(n("3c93"),n("a9ad")),s=n("7560"),o=n("f2e7"),r=n("58df");e["a"]=Object(r["a"])(a["a"],s["a"],o["a"]).extend({name:"v-overlay",props:{absolute:Boolean,color:{type:String,default:"#212121"},dark:{type:Boolean,default:!0},opacity:{type:[Number,String],default:.46},value:{default:!0},zIndex:{type:[Number,String],default:5}},computed:{__scrim:function(){var t=this.setBackgroundColor(this.color,{staticClass:"v-overlay__scrim",style:{opacity:this.computedOpacity}});return this.$createElement("div",t)},classes:function(){return Object(i["a"])({"v-overlay--absolute":this.absolute,"v-overlay--active":this.isActive},this.themeClasses)},computedOpacity:function(){return Number(this.isActive?this.opacity:0)},styles:function(){return{zIndex:this.zIndex}}},methods:{genContent:function(){return this.$createElement("div",{staticClass:"v-overlay__content"},this.$slots.default)}},render:function(t){var e=[this.__scrim];return this.isActive&&e.push(this.genContent()),t("div",{staticClass:"v-overlay",class:this.classes,style:this.styles},e)}})}}]);
//# sourceMappingURL=chunk-62bbd9cf.1403d27e.js.map