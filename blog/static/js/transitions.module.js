var transitions = (function () {

    window.transitions = window.transitions || {};

    transitions.textFocusOn = function () {
        $(this).animate({opacity: 1.0}, 'fast');
    };

    transitions.textFocusOff = function () {
        $(this).animate({opacity: 0.6}, 'fast');
    };

    transitions.textSlide = function(index) {
        var self = this;
        setTimeout(function () {
            $(self)
                .css({opacity: 0.0, left: '50'})
                .animate({opacity: 0.6, left: '0'},
                    'slow',
                    'swing');
        }, index * 100);
    };

    return transitions;
})();

