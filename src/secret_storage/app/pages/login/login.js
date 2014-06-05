/**
 * Created by Maxaon on 5/28/2014.
 */
(function (angular, undefined) {
  var module = angular.module('pages.login', [
    'ui.router'
  ]);
  module.config(function ($stateProvider) {
    $stateProvider.state('login', {
      url: '/login',
      templateUrl: 'pages.login/login.tpl.html',
      controller: "LoginController"
    });
  });
  module.controller('LoginController', function ($scope, UsersCollection, $location) {
    $scope.credentials = {};

    $scope.login = function () {
      UsersCollection.authorize($scope.credentials).$promise.then(function () {
        $location.url("/");
      }).done();
    };

  });
}(angular));