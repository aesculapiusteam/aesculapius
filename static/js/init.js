(function($){
    $(function(){

        $('.button-collapse').sideNav();
        $('.modal-trigger').leanModal();
        $('.fixed-action-btn').openFAB();
    }); // end of document ready
})(jQuery); // end of jQuery name space


$(document).ready(function(){
    $('.slider').slider({full_width: true});
    $('.slider').slider({indicators: false, height: 574});
});
