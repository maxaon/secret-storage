/**
 * Created by Maxaon on 5/28/2014.
 */
(function (angular, undefined) {
  var module = angular.module('pages.dashboard', [
    'ui.router'
  ]);
  module.config(function ($stateProvider) {
      $stateProvider.state('dashboard', {
        url: '/',
        parent: 'base-dashboard',
        breadcrumbTitle: "Dashboard",
        templateUrl: 'pages.dashboard/dashboard.tpl.html'
      });
    }
  );
}(angular));