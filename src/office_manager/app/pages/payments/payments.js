/**
 * Created by Maxaon on 6/2/2014.
 */
(function (angular, undefined) {
  var module = angular.module('pages.payments', [
    'ui.router',
    'collections.payments'
  ]);
  module.config(function ($stateProvider, CrudControllerGeneratorProvider) {
    var state = {
      name: 'PaymentsCrud',
      url: '/payments',
      breadcrumbTitle: "Payments",

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
      resourceName: 'PaymentsCollection',
      list: {
        pageTitle: "Payments",
        columns: {
          payment_date: {
            inputType: "date"
          }
        }
      },
      edit: {
        pageTitle: "Edit payments '{{name}}'",
        breadcrumbTitle: "{{name}}",
        fields: {

        }
      },
      create: {
        pageTitle: "Add new payment",
        breadcrumbTitle: "New payment",
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
        breadcrumbTitle: 'Payments',
        group: 'AdminCRUD',
        title: 'Payments',
        sidebarIcon:'fa fa-money'
      })
      .register();
  });
}(angular));