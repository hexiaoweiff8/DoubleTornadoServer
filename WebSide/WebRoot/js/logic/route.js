
// 定义路由
function routeConfig($routeProvider) {
	$routeProvider.when('/', {
		controller : 'Main',
		templateUrl : "/WebRoot/page/sub/main.html"
	}).when('/data', {
		controller : 'Data',
		templateUrl : "/WebRoot/page/sub/data.html"
	}).when('/grid', {
		controller : 'Grid',
		templateUrl : "/WebRoot/page/sub/grid.html"
	}).otherwise({
		redirectTo : "/"
	});
}