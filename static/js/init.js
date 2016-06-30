(function($){
    $(function(){
        $('select').material_select();
        $('.button-collapse').sideNav();
        $('.modal-trigger').leanModal();
        $('.fixed-action-btn').openFAB();
        var h = window.innerHeight - 64;
        $('.slider').slider({
            full_width: true,
            height: h,
            indicators: false
        });
    }); // end of document ready
})(jQuery); // end of jQuery name space


/*$(document).ready(function(){

});*/
