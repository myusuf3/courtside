$('#search_map').submit(function(e){
    e.preventDefault();
});

$('#search').keyup(function(e) {
    if (e.keyCode == 13) {
        codeAddress();
    }
});