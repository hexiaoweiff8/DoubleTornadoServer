// 获取app
let app = angular.module('myApp', ['ngRoute', 'ngResource' ]);
// 配置路由
app.config(['$routeProvider', routeConfig]);
// 注入依赖
app.$inject = ['$scope', '$http'];
