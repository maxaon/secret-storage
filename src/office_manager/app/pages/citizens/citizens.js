/**
 * Created by Maxaon on 6/2/2014.
 */
(function (angular, undefined) {
  var module = angular.module('pages.citizens', [
    'ui.router',
    'collections.citizens'
  ]);
  module.config(function ($stateProvider, CrudControllerGeneratorProvider) {
    var state = {
      name: 'CitizensCrud',
      url: '/citizens',
      breadcrumbTitle: "Citizens",

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
      resourceName: 'CitizensCollection',
      list: {
        pageTitle: "Citizens",
        columns: {
        }
      },
      edit: {
        pageTitle: "Edit citizen '{{name}}'",
        breadcrumbTitle: "{{name}}",
        fields: {

        }
      },
      create: {
        pageTitle: "Add new citizen",
        breadcrumbTitle: "New citizen",
        fields: {
          id: {show: false}

        }
      }

    };
    var states = CrudControllerGeneratorProvider.register(state, crudOptions);
    states
      .base.merge({
        breadcrumbState: states.list.name
      })
      .list.merge({
        breadcrumbTitle: "Citizens",
        group: 'AdminCRUD',
        title: 'Citizens'
      })
      .register();
  });
}(angular));