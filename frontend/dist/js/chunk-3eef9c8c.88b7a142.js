(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-3eef9c8c"],{bd0c:function(t,e,n){},e402:function(t,e,n){"use strict";n.r(e);var a=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-content",{class:t.$vuetify.theme.dark?void 0:"grey lighten-3",attrs:{id:"pages"}},[n("v-responsive",{staticClass:"d-flex align-center",style:t.styles,attrs:{"min-height":"100vh"}},[n("router-view")],1)],1)},i=[],s=(n("99af"),{name:"PagesCoreView",data:function(){return{srcs:{"/pages/lock":"lock.jpg","/pages/login":"login.jpg","/pages/pricing":"pricing.jpg","/pages/register":"register.jpg"}}},computed:{src:function(){return this.srcs[this.$route.path]},styles:function(){var t=this.$vuetify.breakpoint.mdAndUp?75:10,e=this.$vuetify.breakpoint.mdAndUp?75:50;return{padding:"".concat(t,"px 0 ").concat(e,"px 0")}}}}),r=s,c=n("2877"),o=n("6544"),p=n.n(o),d=n("f6c4"),l=n("d9bd"),u=d["a"].extend({name:"v-main",created:function(){Object(l["d"])("v-content","v-main",this)},render:function(t){var e=d["a"].options.render.call(this,t);return e.data.staticClass+=" v-content",e.children[0].data.staticClass+=" v-content__wrap",t(e.tag,e.data,e.children)}}),g=n("6b53"),f=Object(c["a"])(r,a,i,!1,null,null,null);e["default"]=f.exports;p()(f,{VContent:u,VResponsive:g["a"]})},f6c4:function(t,e,n){"use strict";n("bd0c");var a=n("d10f");e["a"]=a["a"].extend({name:"v-main",props:{tag:{type:String,default:"main"}},computed:{styles:function(){var t=this.$vuetify.application,e=t.bar,n=t.top,a=t.right,i=t.footer,s=t.insetFooter,r=t.bottom,c=t.left;return{paddingTop:"".concat(n+e,"px"),paddingRight:"".concat(a,"px"),paddingBottom:"".concat(i+s+r,"px"),paddingLeft:"".concat(c,"px")}}},render:function(t){var e={staticClass:"v-main",style:this.styles,ref:"main"};return t(this.tag,e,[t("div",{staticClass:"v-main__wrap"},this.$slots.default)])}})}}]);
//# sourceMappingURL=chunk-3eef9c8c.88b7a142.js.map