/**
 * Created by maxaon on 09.01.14.
 */
(function (angular) {
  'use strict';
  var module = angular.module('app.base', [
    'ui.router',
    'pages.login',
    'collections.users',
    'ui.gravatar',
    'sun.diff.filters.textFormatter',
    'services.localCryptoManager'
  ]);
  module.config(function ($stateProvider) {
    $stateProvider
      .state('base', {
        abstract: true,
        templateUrl: 'app.base/base.tpl.html',
        controller: 'BaseController',
        resolve: {
          user: ["UsersCollection", "$state", "$q", function (UsersCollection, $state, $q) {
//            return 123
            return UsersCollection.find('current').$promise
              .catch(function (exp) {
                if (exp.status === 401 || exp.status === 403) {
                  $state.go('login');
                }
                return $q.reject();
              })
              .then(function (resp) {
                return resp.resource;
              })
              .done();
          }
          ]        }
      });
    $stateProvider
      .state('base-dashboard', {
        abstract: true,
        parent: 'base',
        breadcrumbState: 'dashboard',
        breadcrumbTitle: 'Dashboard',
        views: {
          '': {
            template: '<div ui-view></div>'
          },
          'sidebar': {
            templateUrl: 'app.base/sidebar.tpl.html',
            controller: 'SidebarController'
          }
        }
      });
  });
  module.controller('BaseController', function ($scope, LocalCryptoManager, user) {
    $scope.currentUser = user;
    LocalCryptoManager.hasKey($scope.currentUser.email)
      .then(function (hasKey) {
        $scope.hasKey = hasKey;
      }).done();

  });
  module.controller('SidebarController', function ($scope, $state) {
    $scope.states = $state.get();
  });
  module.controller('HeaderController', function ($scope, $rootScope, $state, $filter) {
    $scope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
      $scope.state = toState;
      $scope.breadcrumb = [];
      var state = toState;
      var breadcrumb = [];

      while (state) {
        if (state['abstract'] && state['breadcrumbState']) {
          if (_.isString(state['breadcrumbState']))
            breadcrumb.push($state.get(state['breadcrumbState']));
          else
            breadcrumb.push(state['breadcrumbState']);
        }
        if (!state['abstract']) {
          breadcrumb.push(state);
        }
        state = $state.get(state['parent']);
      }

      var unique = [];
      _.forEach(breadcrumb, function (st) {
        if (unique.indexOf(st.name) > -1) {
          return;
        }
        unique.push(st.name);
//        {
//                  name: st.name,
//                  title: st.breadcrumbTitle || $filter('toHuman')(st.name)
//                }
        $scope.breadcrumb.push(st);
      });
      $scope.breadcrumb = $scope.breadcrumb.reverse();
    });
  });
}(angular) );