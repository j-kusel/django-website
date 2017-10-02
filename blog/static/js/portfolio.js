$(document).ready(function () {
    
    $('h3').each(function (index) {
        $(this)
            .attr('opacity', 0.7)
            //.attr('child', 'a')
            .hover(transitions.textFocusOn, transitions.textFocusOff);
    });
});
