var app;

app = angular.module('ProfileApp', []);

app.controller('AppController', [
  '$scope', '$http', function($scope, $http) {
    return $scope.posts = [
      {
        author: {
          username: 'Joe'
        },
        title: 'Sample Post #1',
        body: 'This is the first sample post'
      }, {
        author: {
          username: 'Karen'
        },
        title: 'Sample Post #2',
        body: 'This is another sample post'
      }
    ];
  }
]);