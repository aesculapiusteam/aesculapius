(function() {
    var app = angular.module('peopleModule', []);

    app.controller('PeopleController', function(){
        this.employees = employees;
        this.profiles = profiles;
        this.current = 0;

        this.setCurrent = function(ModalNumber){
            this.current = ModalNumber || 0;
        };
    });


var employees = [
  {
    "url": "http://localhost:8000/api/employees/1/",
    "username": "doctor",
    "profile": {
      "url": "http://localhost:8000/api/profiles/3/",
      "employee": "http://localhost:8000/api/employees/1/",
      "first_name": "Doctor Romero",
      "last_name": "Doctor",
      "email": "doctor@doctor.com",
      "dni": 40815251,
      "birth_date": "1980-05-03",
      "address": "Mi casa 1 piso 1",
      "phone": "351623213",
      "cellphone": "35123123123",
      "creation_date": "2016-06-21"
    }
  },
  {
    "url": "http://localhost:8000/api/employees/2/",
    "username": "doctor1",
    "profile": {
      "url": "http://localhost:8000/api/profiles/4/",
      "employee": "http://localhost:8000/api/employees/2/",
      "first_name": "Doctor 1",
      "last_name": "Doctor",
      "email": "doctor@doctor.com",
      "dni": 40815252,
      "birth_date": "1980-05-03",
      "address": null,
      "phone": "351623213",
      "cellphone": "35123123123",
      "creation_date": "2016-06-21"
    }
  },
  {
    "url": "http://localhost:8000/api/employees/3/",
    "username": "secretaria",
    "profile": {
      "url": "http://localhost:8000/api/profiles/5/",
      "employee": "http://localhost:8000/api/employees/3/",
      "first_name": "Marta",
      "last_name": "Mocha",
      "email": null,
      "dni": 40815253,
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
    "url": "http://localhost:8000/api/profiles/1/",
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
    "url": "http://localhost:8000/api/profiles/2/",
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
    "url": "http://localhost:8000/api/profiles/3/",
    "employee": "http://localhost:8000/api/employees/1/",
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
    "url": "http://localhost:8000/api/profiles/4/",
    "employee": "http://localhost:8000/api/employees/2/",
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
    "url": "http://localhost:8000/api/profiles/5/",
    "employee": "http://localhost:8000/api/employees/3/",
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

})();
