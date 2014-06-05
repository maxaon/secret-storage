/**
 * Created by Maxaon on 5/27/2014.
 */
(function (angular) {
  'use strict';
  var module = angular.module('app', [
    'sun.diff.conponents.promise',
    'app.base',
    'ui.router',
    'templateCache',
    'sun.rest',
    'pages.users',
    'pages.dashboard',
    'pages.myKeys',
    'pages.citizens',
    'pages.payments'
  ]);
  module.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  });
  module.config(function (sunRestConfigProvider, $stateProvider, $urlRouterProvider) {
    sunRestConfigProvider.baseUrl = '/api';
    $urlRouterProvider.otherwise('/');
    $stateProvider
      .state('admin-dashboard', {
        abstract: true,
        url: '/admin',
        parent: 'base',
        views: {
          '': {
            template: '<div ui-view></div>'
          },
          'sidebar': {
            templateUrl: '/modules/admin/base/admin-sidebar.tpl.html'
          }
        }
      });
  });
}(window.angular));