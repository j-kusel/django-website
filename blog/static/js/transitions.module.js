$(document).ready(function () {
    init();
});

var init = function() {
    $('a').each(function (index) {
        $(this).hover(textFocusOn, textFocusOff);
    });

    $('h1')
        .css({left: '-30'})
        .animate({opacity: 1.0, left: '0'},
            'slow',
            'swing',
        );

    setTimeout(function () {
        $('a').each(textSlide);
    }, 200);

};

var textFocusOn = function () {
    $(this).animate({opacity: 1.0}, 'fast');
};

var textFocusOff = function () {
    $(this).animate({opacity: 0.6}, 'fast');
};

var textSlide = function(index) {
    var self = this;
    setTimeout(function () {
        $(self)
            .css({opacity: 0.0, left: '50'})
            .animate({opacity: 0.6, left: '0'},
                'slow',
                'swing');
    }, index * 100);
};

