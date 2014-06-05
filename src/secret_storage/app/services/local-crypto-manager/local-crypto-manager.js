/**
 * Created by Maxaon on 6/2/2014.
 */
(function (angular, undefined) {
  'use strict';
  var module = angular.module('services.localCryptoManager', [
  ]);
  module.factory('LocalCryptoManager', function ($q, PublicKeysCollection, $log) {
    openpgp.initWorker("/static/openpgp.worker.js");
    var keyring = new openpgp.Keyring();
    var keys = PublicKeysCollection.find().$promise.then(function (resp) {
      return _.map(resp.resource, function (model) {
        var res = openpgp.key.readArmored(model.public_key);
        if (res.err) {
          $log.error(res.err[0]);
          throw new Error(res.err[0]);
        }
        var keys = res.keys;
        if (keys.length === 0) {
          throw new Error("Received record with no key");
        }
        if (keys.length > 1) {
          throw new Error("Too many keys in one record");
        }
        return keys[0];
      });
    });
    var myKey = null;
    var decrypted = false;
    var passphrase = null;

    function getKey(decrypt) {
      var deferred = $q.defer();
      if (!myKey) {
        var keys = keyring.getAllKeys();
        if (keys.length === 0) {
          deferred.reject("Keys not found");
          return deferred.promise;
        }
        if (keys.length !== 1) {
          deferred.reject("Multiple keys found! Not implemented");
          throw new Error("Multiple keys found! Not implemented");
        }
        if (keys[0].isPrivate() === false) {
          deferred.reject("Key doesn't have private part");
          return deferred.promise;
        }
        myKey = keys[0];
      }
      if (decrypt && !decrypted) {
        if (!passphrase) {
          passphrase = window.prompt("Enter your key passphrase");
        }
        myKey.decrypt(passphrase);
      }
      deferred.resolve(myKey);
      return deferred.promise;


    }

    return {
      generateKey: function (passphrase, userId) {
        var deferred = $q.defer();
        openpgp.generateKeyPair({numBits: 512, userId: userId, passphrase: passphrase}, function (err, data) {
          if (err) {
            deferred.reject(err);
          }
          else {
            deferred.resolve(data.privateKeyArmored);
          }
        });
        return deferred.promise;
      },
      hasKey: function () {
        return getKey().then(function () {
          return true;
        }).catch(function () {
          return false;
        });

      },
      setKey: function (armored) {
        var deferred = $q.defer();
        keyring.clear();
        var res = keyring.privateKeys.importKey(armored);
        if (res) {
          deferred.reject(res[0].message);
          return deferred.promise;
        }
        keyring.store();
        return $q.when();
      },
      getPublicKey: function () {
        var res = keyring.privateKeys.keys;
        if (res.length === 0) {
          return $q.reject("Keys not found in keyring");
        }
        res = res[0];
        return  $q.when(res.toPublic().armor());
      },
      decrypt: function (text) {
        if (!text) {
          return $q.when(null);
        }
        return $q
          .all([getKey(true), keys])
          .then(function (res) {
            var myKey = res[0], pks = res[1];
            var deferred = $q.defer();
            var msg = openpgp.message.readArmored(text);
            openpgp.decryptAndVerifyMessage(myKey, pks, msg, function (err, resp) {
              if (err) {
                deferred.reject(err);
              }
              else {
                if (resp.text) {
                  for (var i = 0; i < resp.signatures.length; i++) {
                    if (!resp.signatures[i].valid) {
                      deferred.reject("Signature for id '" + resp.signatures[i].keyid.toHex() + "' is not valid");
                    }
                  }
                }
                deferred.resolve(resp.text);
              }
            });
            return deferred.promise;
          });
      },
      encrypt: function (text) {
        return $q
          .all([getKey(true), keys])
          .then(function (res) {
            var myKey = res[0], pks = res[1];
            var promises = [];
            _.forEach(pks, function (pk) {
              var localDeferred = $q.defer();
              openpgp.signAndEncryptMessage([pk], myKey, text, function (err, encrypted) {
                if (err) {
                  localDeferred.reject(err);
                }
                else {
                  var id = pk.primaryKey.keyid.toHex();
                  localDeferred.resolve([id, encrypted]);
                }
              });
              promises.push(localDeferred.promise);
            });
            return $q
              .all(promises)
              .then(function (res) {
                var normalized = {};
                for (var i = 0; i < res.length; i++) {
                  normalized[res[i][0]] = res[i][1];
                }
                return normalized;
              });
          });
      }
    };
  });
}(angular));