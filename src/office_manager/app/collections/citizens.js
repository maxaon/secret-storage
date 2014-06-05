/**
 * Created by Maxaon on 6/2/2014.
 */
(function (angular, undefined) {
  var module = angular.module('collections.citizens', [
    'sun.rest',
    'ui.router',
    'services.localCryptoManager.interceptors'
  ]);
  module.factory('CitizensCollection', function (sunRestRepository, CryptoInterceptors, $q) {
    var CitizensCollection = sunRestRepository.create('citizens', {
      route: '/citizens/:id',
      requestInterceptor: CryptoInterceptors.requestInterceptor,
      responseInterceptor: CryptoInterceptors.responseInterceptor,
      properties: {
        id: {forward: true},
        name: {forward: true},
        first_name: {},
        middle_name: {},
        last_name: {},
        birth_date: {inputType: 'date'},
        passport: {inputType: 'textarea'}
      },
      encryptedDataKey: 'data'
    });
    return CitizensCollection;

  });

}(angular));