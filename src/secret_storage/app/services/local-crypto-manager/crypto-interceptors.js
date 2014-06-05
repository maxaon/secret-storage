/**
 * Created by Maxaon on 6/4/2014.
 */
(function (angular, undefined) {
  'use strict';
  var module = angular.module('services.localCryptoManager.interceptors', [

  ]);
  module.factory('CryptoInterceptors', function (LocalCryptoManager, $q) {
    return {
      requestInterceptor: function (httpConfig) {
        var model = httpConfig.data;
        if (!model)
          return;
        var newData = {};
        var oldData = model.mngr.toJSON();
        var toCtypt = {};
        _.forEach(model.mngr.schema.properties, function (prop, name) {
          if (prop.forward) {
            newData[name] = oldData[name];
          }
          else {
            toCtypt[name] = oldData[name];
          }
        });
        return LocalCryptoManager
          .encrypt(angular.toJson(toCtypt))
          .then(function (encrypted) {
            newData[model.mngr.schema.encryptedDataKey] = encrypted;
            httpConfig.data = newData;
            return httpConfig;
          });
      },
      responseInterceptor: function (response, path) {
        var schema = this.schema || this.mngr.schema;
        if (_.isArray(response.data)) {
          return $q.all(_.map(response.data, processObject)).then(function (result) {
            response.data = result;
            return response;
          });
        }
        else {
          return processObject(response.data).then(function (result) {
            response.data = result;
            return response;
          });
        }

        function processObject(baseObj) {
          var encrypted = baseObj[schema.encryptedDataKey];
          return LocalCryptoManager.decrypt(encrypted).then(function (decrypted) {
            if (!decrypted) {
              return baseObj;
            }
            var obj = angular.fromJson(decrypted);
            var returnValue = baseObj;
            var parts = path && path.split('.') || [];
            for (var x = 0; x < parts.length; x += 1) {
              returnValue = angular.isObject(returnValue) ? returnValue[parts[x]] : undefined;
            }
            if (returnValue) {
              _.forEach(obj, function (value, key) {
                returnValue[key] = value;
              });
            }
            return returnValue;
          });
        }

      }
    };

  });
}(angular));