/**
 * Created by Maxaon on 5/28/2014.
 */
(function (angular, undefined) {
  'use strict';
  var module = angular.module('collections.users', [
    'sun.rest'
  ]);
  module.factory('UsersCollection', ['sunRestRepository', function (sunRestRepository) {
    var UsersCollection = sunRestRepository.create('Users', {
      route: '/users/:id',
      inherit: {
        toString: function () {
          var res = "User";
          if (this.username)
            res += " \"" + this.username + "\"";
          if (this.id)
            res += " (" + this.id + ")";
          return res;
        }
      },
      properties: {
        id: {},
        username: {},
        password: {
          show: false
        },
        is_superuser: {
          default: false
        },
        is_staff: {
          default: false
        },
        first_name: {},
        last_name: {},
        email: {},
        display_name: {
          getter: function () {
            if (this.first_name && this.last_name)
              return this.first_name + " " + this.last_name;
            else if (this.first_name)
              return this.first_name;
            else
              return this.username
          },
          show: false
        }
      }
    });
    UsersCollection.authorize = function (authObject) {
      return UsersCollection.find("authorize", authObject);
    };

    return UsersCollection;
  }])
  ;
}(angular));