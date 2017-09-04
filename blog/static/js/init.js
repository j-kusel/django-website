$(document).ready(function () {
    init();
});

var init = function() { 
    $('a').each(function (index) { 
        $(this)
            .attr('opacity', 0.6)
            .hover(transitions.textFocusOn, transitions.textFocusOff); 
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
