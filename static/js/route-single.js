
var LoginPage = Vue.extend({
    template: '#login-template'
});

var Services = Vue.extend({
    template: '#report-template'
})

var router = new VueRouter({
    routes: [
        {path: '/', component: LoginPage},
        {path: '/pullreport/:org_id/:service/:extension', name: 'report', component: Services}
    ]
})

new Vue({
    el: '#app',

    data: {

    },

    router: router,

    delimiters: ["<%", "%>"],

    template: '<router-view></router-view>'
});
