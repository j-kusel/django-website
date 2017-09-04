$(document).ready(function () {
    $('a').each(function (index) {
        $(this).hover(transitions.textFocusOn, transitions.textFocusOff);
    });
});
