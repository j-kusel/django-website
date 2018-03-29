$(document).ready(function () {
    init();
});

var init = function() { 
    $('h3').each(function (index) { 
        $(this)
            .attr('opacity', 0.6)
            .attr('child', 'a')
            .hover(transitions.textFocusOn, transitions.textFocusOff);

    }); //.each(transitions.textSlide); 
 
    $('h1') 
        .css({'padding-right': '60px'}) 
        .animate({opacity: 1.0, 'padding-right': '30px'}, 
            'slow', 
            'swing' 
        );

    $('a')
        .each(function (index) {
            var $self = $(this).css({opacity: 0.0});
            setTimeout(function () {
                $self.css({opacity: 0.6});
            }, (index+1) * 100);
        });
 
};
