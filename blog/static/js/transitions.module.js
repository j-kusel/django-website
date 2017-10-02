var transitions = (function () {

    window.transitions = window.transitions || {};

    transitions.textFocusOn = function () {
        $(this).toggleClass('h3Tr');
        var $self = $(this).attr('child') ? $(this).find($(this).attr('child')) : $(this);
        $self.animate({opacity: 1.0}, 'fast');
        $self.toggleClass('aTr');
    };

    transitions.textFocusOff = function () {
        $(this).toggleClass('h3Tr');
        var $self = $(this).attr('child') ? $(this).find($(this).attr('child')) : $(this);
        $self.animate({opacity: $self.attr('opacity')}, 'fast');
        $self.toggleClass('aTr');
    };

    transitions.textSlide = function(index) {
        var $self = $(this);
        console.log($self.attr('opacity'));
        setTimeout(function () {
            $self
                .css({opacity: 0.0, 'padding-left': '60px'})
                .animate({opacity: $self.attr('opacity'), 'padding-left': '30px'},
                    'slow',
                    'swing');
        }, index * 100);
    };

    return transitions;
})();

