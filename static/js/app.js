(function() {

  var app = angular.module('peopleModule', [
    'ui.router',
    'restangular'
  ]).config(function(RestangularProvider, $httpProvider){
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    //set the base url for api calls on our RESTful services
    var newBaseUrl = "";
    if (window.location.hostname == "localhost") {
      newBaseUrl = "http://localhost:8000/api/";
    } else {
      var deployedAt = window.location.href.substring(0, window.location.href);
      newBaseUrl = deployedAt + "/api/";
    }
    RestangularProvider.setBaseUrl(newBaseUrl);
    RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response, deferred) {
      var extractedData;
      if (operation === "getList") {
        extractedData = data.results;
      } else {
        extractedData = data;
      }
      return extractedData;
    });
  });

  app.controller("PeopleController", ['$scope', '$rootScope', 'Restangular', function($scope, $rootScope, Restangular){
    this.current = 0;

    this.setCurrent = function(ModalNumber){
      $('.modal-trigger').leanModal();
      this.current = ModalNumber || 0;
    };

    var allEmployees = Restangular.all('employees').getList().then(function(response){
      $scope.employees = response;
    });

    var allProfiles = Restangular.all('profiles').getList().then(function(response){
      $scope.profiles = response;
    });

    this.save = function(employeePos){
      var employee = $scope.employees[employeePos];
      employee.save();
    };
    $rootScope.$broadcast('dataloaded');

  }]);

  app.directive('modalRefresh', ['$timeout', function ($timeout) {
    return {
      link: function ($scope, element, attrs) {
        $scope.$on('dataloaded', function () {
          $timeout(function () {
            console.log("PATO");
            $('.modal-trigger').leanModal();
          }, 0, false);
        });
      }
    };
  }]);

  var employees = [
    {
      "id": 1,
      "username": "doctor",
      "charge":"doctor",
      "profile": {
        "id": 3,
        "employee": 1,
        "first_name": "Doctor Romero",
        "last_name": "Doctor",
        "email": "doctor@doctor.com",
        "dni": 123123123123,
        "birth_date": "1980-05-03",
        "address": "Mi casa 1 piso 1",
        "phone": "351623213",
        "cellphone": "35123123123",
        "creation_date": "2016-06-21"
      }
    },
    {
      "id": 2,
      "username": "doctor1",
      "charge": "doctor",
      "profile": {
        "id": 4,
        "employee": 2,
        "first_name": "Doctor 1",
        "last_name": "Doctor",
        "email": "doctor@doctor.com",
        "dni": null,
        "birth_date": "1980-05-03",
        "address": null,
        "phone": "351623213",
        "cellphone": "35123123123",
        "creation_date": "2016-06-21"
      }
    },
    {
      "id": 3,
      "username": "secretaria",
      "charge": "secretary",
      "profile": {
        "id": 5,
        "employee": 3,
        "first_name": "Marta",
        "last_name": "Mocha",
        "email": null,
        "dni": null,
        "birth_date": null,
        "address": null,
        "phone": null,
        "cellphone": null,
        "creation_date": "2016-06-21"
      }
    }
  ];

  var profiles = [
    {
      "id": 1,
      "employee": null,
      "first_name": "El Brayan",
      "last_name": null,
      "email": "brayatan@jotmeil.com",
      "dni": 123123123,
      "birth_date": null,
      "address": null,
      "phone": null,
      "cellphone": null,
      "creation_date": "2016-06-21"
    },
    {
      "id": 2,
      "employee": null,
      "first_name": "Señor",
      "last_name": "Macaco",
      "email": "macacon@jotmeil.com",
      "dni": 333939392,
      "birth_date": "1980-06-05",
      "address": "A la vuelta de la esquina",
      "phone": "4851243",
      "cellphone": "351-222222",
      "creation_date": "2016-06-21"
    },
    {
      "id": 3,
      "employee": 1,
      "first_name": "Doctor Romero",
      "last_name": "Doctor",
      "email": "doctor@doctor.com",
      "dni": 123123123123,
      "birth_date": "1980-05-03",
      "address": "Mi casa 1 piso 1",
      "phone": "351623213",
      "cellphone": "35123123123",
      "creation_date": "2016-06-21"
    },
    {
      "id": 4,
      "employee": 2,
      "first_name": "Doctor 1",
      "last_name": "Doctor",
      "email": "doctor@doctor.com",
      "dni": null,
      "birth_date": "1980-05-03",
      "address": null,
      "phone": "351623213",
      "cellphone": "35123123123",
      "creation_date": "2016-06-21"
    },
    {
      "id": 5,
      "employee": 3,
      "first_name": "Marta",
      "last_name": "Mocha",
      "email": null,
      "dni": null,
      "birth_date": null,
      "address": null,
      "phone": null,
      "cellphone": null,
      "creation_date": "2016-06-21"
    }
  ];

var visits = [
        {
            "id": 1,
            "pacient": 1,
            "doctor": 1,
            "datetime": "2016-06-26T16:31:08.018697Z",
            "detail": "El brayan trajo una navaja metida en el pesguezo, se la saque y le di una bayaspirina,"
        },
        {
            "id": 2,
            "pacient": 1,
            "doctor": 1,
            "datetime": "2016-06-26T16:31:33.462942Z",
            "detail": "Otra vez vino el brayan con una navaja clavada en la pierna"
        },
        {
            "id": 3,
            "pacient": 1,
            "doctor": 2,
            "datetime": "2016-06-26T16:32:19.131782Z",
            "detail": "OTRA VEZ BRAYAN BASTA!!! le di una psicoinmunoneuroendomorfinacalmante"
        },
        {
            "id": 4,
            "pacient": 2,
            "doctor": 2,
            "datetime": "2016-06-26T16:40:35.797589Z",
            "detail": "Otra vez vino el mocaco"
        },
        {
            "id": 5,
            "pacient": 2,
            "doctor": 2,
            "datetime": "2016-06-26T16:41:17.305309Z",
            "detail": "el mocaco se hizo atender por cancer"
        }
    ];

})();
