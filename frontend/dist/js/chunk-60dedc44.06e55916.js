(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-60dedc44"],{"3f8e":function(e,t,a){"use strict";a.r(t);var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("v-container",{staticClass:"d-flex justify-center",attrs:{id:"contest",fluid:"",tag:"section"}},[a("v-card",{staticClass:"px-5",attrs:{loading:e.loading,"min-width":"60%"}},[a("v-card-title",{staticClass:"justify-center font-weight-medium mb-md-3"},[e._v(" Score By User "),a("v-spacer"),a("v-text-field",{staticClass:"mb-5",attrs:{"append-icon":"mdi-magnify",label:"Search",clearable:"","single-line":"","hide-details":""},model:{value:e.search,callback:function(t){e.search=t},expression:"search"}})],1),a("v-card-text",[a("v-data-table",{attrs:{items:e.scores,loading:e.loading,headers:e.headers,"fixed-header":"","items-per-page":5,"item-key":"username",search:e.search}})],1)],1)],1)},n=[],s=(a("96cf"),a("1da1")),i=a("b899"),c={name:"Contest",data:function(){return{loading:!1,search:"",scores:[],headers:[{text:"User",value:"username",align:"center"},{text:"Surviving Fighters",value:"surviving_fighters",align:"center"},{text:"Wins",value:"wins",align:"center"},{text:"Losses",value:"losses",align:"center"},{text:"Dead",value:"dead",align:"center"}]}},mounted:function(){this.getScoresByUser()},methods:{getScoresByUser:function(){var e=this;return Object(s["a"])(regeneratorRuntime.mark((function t(){var a,r;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return e.loading=!0,t.next=3,i["a"].get("api/entries/score_by_user");case 3:a=t.sent,r=a.data,e.scores=r.scores,e.loading=!1;case 7:case"end":return t.stop()}}),t)})))()}}},o=c,d=a("2877"),l=a("6544"),u=a.n(l),f=a("b0af"),g=a("99d9"),p=a("a523"),v=a("8fea"),m=a("2fa4"),h=a("8654"),b=Object(d["a"])(o,r,n,!1,null,null,null);t["default"]=b.exports;u()(b,{VCard:f["a"],VCardText:g["b"],VCardTitle:g["c"],VContainer:p["a"],VDataTable:v["a"],VSpacer:m["a"],VTextField:h["a"]})},a523:function(e,t,a){"use strict";a("99af"),a("4de4"),a("b64b"),a("2ca0"),a("20f68"),a("4b85"),a("a15b"),a("498a");var r=a("2b0e");function n(e){return r["a"].extend({name:"v-".concat(e),functional:!0,props:{id:String,tag:{type:String,default:"div"}},render:function(t,a){var r=a.props,n=a.data,s=a.children;n.staticClass="".concat(e," ").concat(n.staticClass||"").trim();var i=n.attrs;if(i){n.attrs={};var c=Object.keys(i).filter((function(e){if("slot"===e)return!1;var t=i[e];return e.startsWith("data-")?(n.attrs[e]=t,!1):t||"string"===typeof t}));c.length&&(n.staticClass+=" ".concat(c.join(" ")))}return r.id&&(n.domProps=n.domProps||{},n.domProps.id=r.id),t(r.tag,n,s)}})}var s=a("d9f7");t["a"]=n("container").extend({name:"v-container",functional:!0,props:{id:String,tag:{type:String,default:"div"},fluid:{type:Boolean,default:!1}},render:function(e,t){var a,r=t.props,n=t.data,i=t.children,c=n.attrs;return c&&(n.attrs={},a=Object.keys(c).filter((function(e){if("slot"===e)return!1;var t=c[e];return e.startsWith("data-")?(n.attrs[e]=t,!1):t||"string"===typeof t}))),r.id&&(n.domProps=n.domProps||{},n.domProps.id=r.id),e(r.tag,Object(s["a"])(n,{staticClass:"container",class:Array({"container--fluid":r.fluid}).concat(a||[])}),i)}})}}]);
//# sourceMappingURL=chunk-60dedc44.06e55916.js.map