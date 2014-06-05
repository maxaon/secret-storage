/**
 * Created by Maxaon on 6/2/2014.
 */
(function (angular, undefined) {
  var module = angular.module('pages.myKeys', [
    'ui.router',
    'collections.publicKeys'
  ]);
  module.config(function ($stateProvider) {
    $stateProvider.state('AddMyKey', {
      url: "/my-keys/add",
      templateUrl: 'pages.myKeys/add-key.tpl.html',
      pageTitle: "Add key",
      breadcrumbTitle: "Add key",
      parent: 'base-dashboard',
      controller: 'AddMyKeyController'
    });
    $stateProvider.state('MyKeys', {
      url: "/my-keys",
      templateUrl: 'pages.myKeys/my-keys.tpl.html',
      pageTitle: "My keys",
      breadcrumbTitle: "Keys",
      parent: 'base-dashboarcd',
      controller: 'MyKeysController'
    });
  });

  module.controller('MyKeysController', function ($scope, LocalCryptoManager) {

  });
  module.controller('AddMyKeyController', function ($scope, $q, LocalCryptoManager, MessageBox, PublicKeysCollection) {
    $scope.key = null;
    $scope.generate = function () {
      var user = $scope.currentUser, userId;
      userId = user.display_name + " <" + user.email + ">";
      LocalCryptoManager.generateKey(prompt("Enter passphrase"), userId).then(function (data) {
        $scope.key = data;
      });
    };
    $scope.save = function () {
      PublicKeysCollection.find($scope.currentUser.id).$promise.then(function (resp) {
        return MessageBox.warning("Another key was added. Do you want to continue?", "Warning", ['Yes', 'No'], 'No').result.then(function (ans) {
          if (ans === "Yes") {
            return resp.resource;
          }
          return $q.reject();
        });
      }).catch(function (resp) {
        if (resp && resp.status === 404) {
          var resource = new PublicKeysCollection.model();
          resource.user = $scope.currentUser.id;
          return resource;
        }
        else {
          return $q.reject(resp);
        }
      }).then(function (resource) {
        var key = $scope.key;
        return LocalCryptoManager
          .setKey(key)
          .catch(function (reason) {
            MessageBox.error(reason);
          })
          .then(function () {
            return LocalCryptoManager.getPublicKey();
          })
          .then(function (key) {
            resource.public_key = key;
            return resource.mngr.save()
              .then(function (resp) {
                var localKeyid = openpgp.key.readArmored(key).keys[0].primaryKey.keyid.toHex();
                if (localKeyid.toLocaleLowerCase() !== resp.keyid.toLocaleLowerCase()) {
                  MessageBox.critical("Local key id mismatched from remote. Stop working!", "Critical error!!");
                }
                else {
                  MessageBox.show("You key was added to the system", "Success");
                }
              });
          });
      }).catch(function (err) {
        if (err) {
          return $q.reject(err);
        }
      })
        .done();
    };
  });
}(angular));