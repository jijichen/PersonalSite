(function(angular) {
  'use strict';

  var app = angular.module("HomePage", []);

  app.controller("ExpLoader", function($scope, $http) {
    $http.get('experience.json').
        success(function(data, status, headers, config) {
            $scope.exps = data;
        }).
        error( function(data, status, headers, config) {

        })
  })
})(window.angular);
