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

  app.filter('getEmployeePosById', function(){
    return function(employeeId, $scope){
      return $scope.employees.find(function(x){return x.id === employeeId;});
    };
  });
  app.directive('repeatDone', function() {
     return function(scope, element, attrs) {
         if (scope.$last) {
             scope.$eval(attrs.repeatDone);
         }
     };
 });

  app.controller("PeopleController", ['$scope', '$rootScope', 'Restangular', function($scope, $rootScope, Restangular){
    this.current = 0;
    $scope.employees = [];
    $scope.initModals = function() {
        $('.modal-trigger').leanModal(); // Initialize the modals
        Materialize.updateTextFields();
    };
    this.setCurrent = function(ModalNumber){
      this.current = ModalNumber || 0;
      this.editProfile = Restangular.copy($scope.profiles[this.current]);
      if (this.current <= $scope.employees.length-1){
        this.editEmployee = Restangular.copy($scope.employees[this.current]);
      }
    };

    var allEmployees = Restangular.all('employee');
    allEmployees.getList().then(function(response){
      $scope.employees = response;
    });

    var allProfiles = Restangular.all('profile');
    allProfiles.getList().then(function(response){
      $scope.profiles = response;
    });

    var allVisits = Restangular.all('visit');
    allVisits.getList().then(function(response){
      $scope.visits = response;
    });

    this.prepareJson = function(dic){
      var i = 0;
      for (i in dic){
        if (dic[i] === ""){
          dic[i] = null;
        }
      }
      return dic;
    };

    this.saveEmployee = function(employeePos){
      var employee = this.editEmployee;
      employee.profile = this.prepareJson(employee.profile);
      employee.save().then(function (response){
        $scope.employees[employeePos] = employee;
      });
    };

    this.saveProfile = function(profilePos){
      var profile = this.editProfile;
      profile = this.prepareJson(profile);
      profile.save().then(function (response){
        $scope.profiles[profilePos] = profile;
      });
    };

    this.deleteEmployee = function(employeePos){

      var employee = $scope.employees[employeePos];
      employee.remove().then(function() {
        $scope.employees = _.without($scope.employees, employee);
      });
    };

    this.deleteProfile = function(profilePos){
      var profile = $scope.profiles[profilePos];
      profile.remove().then(function() {
        $scope.profiles = _.without($scope.profiles, profile);
      });
    };

    this.deleteVisit = function(visitPos){
      var visit = $scope.visits[visitPos];
      visit.remove().then(function() {
        $scope.visits = _.without($scope.visits, visit);
      });
    };

    this.createEmployee = function(){
      this.addEmployee.assist_ed = [];
      allEmployees.post(this.addEmployee).then(function(postedUser) {
        allEmployees.getList().then(function(response){
          $scope.employees = response;
        });
      });
    };

    this.createProfile = function(){
      allProfiles.post(this.addProfile).then(function(postedUser) {
        allProfiles.getList().then(function(response){
          $scope.profiles = response;
        });
      });
    };

    this.createVisit = function(){
      this.addVisit.pacient = $scope.profiles[this.current].id;
      allVisits.post(this.addVisit).then(function(postedVisit) {
        allVisits.getList().then(function(response){
          $scope.visits = response;
        });
      });
    };

    $rootScope.$broadcast('dataloaded');

  }]);
})();
