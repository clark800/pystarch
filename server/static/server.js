
var DIRTY = false;
var WAITING = false;

function update() {
    DIRTY = false;
    WAITING = true;
    var code = $('#input').val();
    $.post('/process', {source: code}).done(function(response) {
        $('#output').val(response);
        WAITING = false;
    }).fail(function() {
        $('#output').val('Syntax error in source code');
        WAITING = false;
    });
}

function onInterval() {
    if(DIRTY && !WAITING)
        update();
}

$(document).ready(function() {
    $('#input').bind('input propertychange', function() { DIRTY = true; });
    setInterval(onInterval, 1000);
    update();
});
