/*============================================================================================
Tag info page
============================================================================================*/

var tagName = $('#page header h1').attr('data-genre-name');

$.getJSON("/api/genres/" + tagName + "/tracklist", handlebarsRenderTracklist);
$.getJSON("/api/genres/" + tagName + "/artists", handlebarsRenderArtists);

// get artist info from LastFM API
lastFmAPIGet("tag", tagName, function(tagInfo) {
    console.log(tagInfo);
    $('<p>').html(tagInfo.tag.wiki.summary).appendTo('#desc');
});
