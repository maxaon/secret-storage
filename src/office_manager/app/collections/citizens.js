/**
 * Created by Maxaon on 6/2/2014.
 */
(function (angular, undefined) {
  var module = angular.module('collections.citizens', [
    'sun.rest',
    'ui.router',
    'services.localCryptoManager.interceptors'
  ]);
  module.factory('CitizensCollection', function (sunRestRepository, LocalCryptoManager, $q) {
    var CitizensCollection = sunRestRepository.create('citizens', {
      route: '/payments/:id',
      properties: {
        id: {},
        citizen: {},
        amount: {},
        payment_date: {},
        last_name: {},
        payment_type: {},
        receiver: {}
      },
      encryptedDataKey: 'data'
    });
    return CitizensCollection;

  });

}(angular));