$(document).ready(function () {
    
    $('li').each(function (index) {
        $(this)
            .attr('opacity', 0.6)
            .attr('child', 'a')
            .hover(transitions.textFocusOn, transitions.textFocusOff);
    });
});
