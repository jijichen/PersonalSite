(

  var processCSVRaw = function(data) {
      $scope.csvdata = data;
      Papa.parse($scope.csvdata,  {
          complete: function(results) {
              console.log("Finished:", results.data);
          },
          header:true
      });
  }

  function(angular) {
      'use strict';

      var app = angular.module("HomePage", []);

      app.controller("ExpLoader", function($scope, $http) {
        $http.get('depData/exp.csv').
            success(processCSVRaw(data));
      })

  }
)(window.angular);
