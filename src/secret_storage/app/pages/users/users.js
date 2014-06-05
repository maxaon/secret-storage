/**
 * Created by Maxaon on 5/28/2014.
 */
(function (angular, undefined) {
  var module = angular.module('pages.users', [
    'ui.router',
    'collections.users',
    'sun.diff.components.adminCrud'
  ]);
  module.config(function ($stateProvider, CrudControllerGeneratorProvider) {
    var state = {
      name: 'UsersCrud',
      url: '/users',
      breadcrumbTitle: "Users",

      parent: 'base-dashboard',
      title: "Edit",
      abstract: true,
      views: {
        '': {
          template: '<div crud-table="crud"></div>'
        }
      }
    };
    var crudOptions = {
      resourceName: 'UsersCollection',
      list: {
        pageTitle: "Users",
        columns: {
        }
      },
      edit: {
        pageTitle: "Edit users '{{username}}'",
        breadcrumbTitle: "{{username}}",
        fields: {
          is_superuser: {inputType: 'yes-no'},
          is_staff: {inputType: 'yes-no'},
          password: {}

        }
      },
      create: {
        pageTitle: "Create new user",
        breadcrumbTitle: "New user",
        fields: {
          is_superuser: {inputType: 'yes-no'},
          is_staff: {inputType: 'yes-no'},
          id: {show: false},
          password: {}
        }
      }

    };
    var states = CrudControllerGeneratorProvider.register(state, crudOptions);
    states
      .base.merge({
        breadcrumbState: states.list.name
      })
      .list.merge({
        breadcrumbTitle: "Users",
        group: 'AdminCRUD',
        title: 'Users'
      })
      .register();
  });
}(angular));