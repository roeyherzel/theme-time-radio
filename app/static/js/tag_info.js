/*============================================================================================
Tag info page
============================================================================================*/

var tagName = $('#page header h1').attr('data-tag-name');

$.getJSON("/api/tags/" + tagName + "/tracklist", handlebarsRenderTracklist);
$.getJSON("/api/tags/" + tagName + "/artists", handlebarsRenderArtists);

// get artist info from LastFM API
lastFmAPIGet("tag", tagName, function(tagInfo) {
    console.log(tagInfo);
    $('<p>').html(tagInfo.tag.wiki.summary).appendTo('#desc');
});
