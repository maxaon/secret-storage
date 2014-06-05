/**
 * Created by Maxaon on 6/2/2014.
 */
(function (angular, undefined) {
  'use strict';
  var module = angular.module('collections.publicKeys', [
    'sun.rest'
  ]);
  module.factory('PublicKeysCollection', ['sunRestRepository', function (sunRestRepository) {
    return sunRestRepository.create('PublicKeys', {
      route: '/public-keys/:user',
      properties: {
        user: {},
        public_key: {},
        keyid: {}
      }
    });
  }]);

}(angular));