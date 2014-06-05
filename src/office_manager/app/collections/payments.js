/**
 * Created by Maxaon on 6/2/2014.
 */
(function (angular, undefined) {
  var module = angular.module('collections.payments', [
    'sun.rest',
    'ui.router',
    'services.localCryptoManager'
  ]);
  module.factory('PaymentsCollection', function (sunRestRepository, CryptoInterceptors) {
    var PaymentsCollection = sunRestRepository.create('payments', {
      route: '/payments/:id',
//      requestInterceptor: CryptoInterceptors.requestInterceptor,
//      responseInterceptor: CryptoInterceptors.responseInterceptor,
      properties: {
        id: {},
        citizen: {},
        amount: {},
        payment_date: {},
        payment_type: {},
        receiver: {},
      },
      relations: {
        user: {
          service: "UsersCollection",
          property: "user"
        },
        citizen: {

        }


      }
    });
    return PaymentsCollection;

  });

}(angular));