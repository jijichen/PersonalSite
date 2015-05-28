(function(angular) {
    'use strict';
    var app = angular.module("HomePage", ['angular.filter']);
    app.config(function($interpolateProvider) {
      $interpolateProvider.startSymbol('{[{');
      $interpolateProvider.endSymbol('}]}');
    });
    app.controller("ExpLoader", function($scope, $http) {
        var processCSVRaw = function(data) {
            Papa.parse(data, {
                complete: function(results) {
                    results.data.forEach( function(element) {
                        element.desRows = element.des.split('\\\\#');
                        console.log(element);
                        console.log(element.desRows.length);
                    });
                    $scope.csvData = results.data;
                },
                header: true
            });
        }
        $http.get('static/depData/exp.csv').
        success(processCSVRaw);
    })


})(window.angular);
