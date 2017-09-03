console.log(window.transitions !== false);

$(document).ready(function () {
    init();
});

var init = function() { 
    $('a').each(function (index) { 
        $(this).hover(transitions.textFocusOn, transitions.textFocusOff); 
    }); 
 
    $('h1') 
        .css({left: '-30'}) 
        .animate({opacity: 1.0, left: '0'}, 
            'slow', 
            'swing', 
        ); 
 
    setTimeout(function () { 
        $('a').each(transitions.textSlide); 
    }, 200); 
 
};
