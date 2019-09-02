
app.controller('Main', function($scope){
    console.log('main ctrl');
    $scope.name = 'name';
});
app.controller('Data', function($scope){
    console.log('data ctrl');
    $scope.messages = [ {
            id : 0,
            sender : "jojo@sina.com",
            subject : "hi, boy.",
            date : "2014-6-9",
            recipient : [ "yaya@sina.com" ],
            message : "you baby is coming!"
        }, {
            id : 1,
            sender : "hexiaoweiff8@sina.com",
            subject : "hi, gril.",
            date : "2014-6-9",
            recipient : [ "yaya@sina.com" ],
            message : "you baby was coming!"
        }, {
            id : 2,
            sender : "hexiaoweiff7@sina.com",
            subject : "hi, gay.",
            date : "2014-6-9",
            recipient : [ "yaya@sina.com" ],
            message : "you baby was come!"
        } ];
});

app.controller('Grid', function($scope){
    console.log('grid ctrl');
    $scope.name = 'name';
});
