$(document).ready(function () {
    $('a').each(function (index) {
        $(this)
            .attr('opacity', 0.7)
            .hover(transitions.textFocusOn, transitions.textFocusOff);
    });
});
