/**
 * Created by Maxaon on 5/28/2014.
 */
/* global openpgp */
(function (angular, undefined) {
  'use strict';
  var module = angular.module('pages.login', [
    'ui.router',
    'sun.diff.components.messageBox'
  ]);
  module.config(function ($stateProvider) {
    $stateProvider.state('login', {
      url: '/login',
      templateUrl: 'pages.login/login.tpl.html',
      controller: 'LoginController'
    });
    $stateProvider.state('Logout', {
      url: '/logout',
      controller: 'LogoutController'
    });
  });
  module.constant('PrivateKey', "-----BEGIN PGP PRIVATE KEY BLOCK-----\r\nVersion: OpenPGP.js v0.6.0\r\nComment: http://openpgpjs.org\r\n\r\nxcBmBFOQtcEBAgDpqEGVJxPd4KigConibcwT9tMLF5t6V7MoJ4d/4jw0HWqa\nTsH03VoNZF9D90usnbOliae10Mjk0JeNDChzaDZrABEBAAH+CQMIsgrtksoc\n3M1gWTtvIFblK7eN295AZnLXqnpAhY1YoP0qrNTPLP5LH03zl9r3TkEgTtnN\nRqRm3FK7DnXBLQCdzqNI17MkfjddCX1bNcRldQIW0XWrbF3dx8CTXZEW0dYH\nOxFSpWKWROCwa6nxz1D+oUgRIyKTBOzlYoQ2vs9A2u4q08nGfo85zyzB4id4\nekwz3cR45PwZFH5g9BjSieMfqz/wFue7d1WIx0P/IQUv8g4DVRyLLaG/cgCK\nMuj9bmcoi8pXa6XwlVH3rH+nH2rFhc2ChmRfzRdBZG1pbiA8bWF4YW9uQHhh\na2VwLnJ1PsJyBBABCAAmBQJTkLXBBgsJCAcDAgkQwM+Qs2HBhdkEFQgCCgMW\nAgECGwMCHgEAAGzPAgC/AlGn5xxszMlZTQBCu6lCdZGACssSS6OQMwLTwE9/\nH6XlrQASYztxUsCm2GrjZXMmt+YLHwTF/3D14W3FGYOsx8BmBFOQtcEBAf9v\nDatTmT7A2Ksd9Hi9NFbbov0u27blIwDTyv81QndsKYpyr5FtKI8DNVwX2fwe\nCXyNqcktGNkk94SMYYJL7aGXABEBAAH+CQMIUGrtm1RaxPFgBBd6dCxQ9EZB\nIykmkLNYJGDoxSANJrZWPdw1oC+jdpgLEaT14C3x0iMYvNVN9KLHLnQOqRB5\nM2FNYmYo5Otzho4kqggzR9hYYzDUosnAxQCn31IhmWU5PZLGAbIkzy7yEYHG\nNYC1Zuz0JeSPzOHt8kxfRu+mqjfBT6ElmIUGSTXLdj6ZokTMJM0kfXeBQjjk\nvMlWWJzs4TVPOF8P8C2YRT2/W+xS4laXMA24T0SrPkdeIadU1bxN5U6Cw4KZ\nl605BOSxb6/0LSK/3T3dwl8EGAEIABMFAlOQtcEJEMDPkLNhwYXZAhsMAADT\nuAIAmVlkgK/QQhwfD4u3A6zno4c9ywb/4Q/FcSAE0U/IuQKahVvGLbvBz4Uu\npOzM97fQuGmedfTpEGSaiou7kVAoig==\r\n=eKzF\r\n-----END PGP PRIVATE KEY BLOCK-----\r\n");
  module.controller('LoginController', function ($scope, $state, UsersCollection, $location, PrivateKey, $browser, LocalCryptoManager, MessageBox) {
    $scope.credentials = {};

    $scope.login = function () {
      UsersCollection.authorize($scope.credentials).$promise
        .then(function () {
          return $state.go('dashboard');
        })
        .catch(function (resp) {
          if (resp.data && resp.data.detail) {
            $scope.error = resp.data.detail;
          }
        })
        .done();
    };
    $scope.startDemo = function () {
      MessageBox.show('Demo database will be created for you. You will have all access to the site. <br>You password is <span class="label label-info">admin</span>', "Start demo", ['Ok', 'Cancel']).ok(function () {
        if (!$browser.cookies('demo_db')) {
          $browser.cookies('demo_db', btoa(openpgp.crypto.random.getRandomBytes(64)));
        }
//        $document.cookie = 'demo_db=' + btoa(openpgp.crypto.random.getRandomBytes(64));
        LocalCryptoManager.setKey(PrivateKey).then(function () {
          $scope.credentials = {'username': 'admin', 'password': 'admin'};
          $scope.login();
        });
      });
    };

  });
  module.controller('LogoutController', function (UsersCollection, $state, LocalCryptoManager) {
    LocalCryptoManager.armor()
      .then(function () {
        return UsersCollection.logout();
      })
      .catch(function () {

      })
      .finally(function () {
        return $state.go('login');
      })
      .done();

  });
}(angular));