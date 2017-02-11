/*============================================================================================
Artist info page
============================================================================================*/

var artistId = $('header h1').attr('data-artist-id'),
    artistName = $('header h1').text();

$.getJSON("/api/artists/" + artistId + "/episodes", handlebarsRenderEpisodes);
$.getJSON("/api/artists/" + artistId + "/tracklist", handlebarsRenderTracklist);

// get artist info from LastFM API
lastFmAPIGet("artist", artistName, function(artistInfo) {

    console.log(artistInfo);
    // render bio
    $('<p>').html(artistInfo.artist.bio.summary).appendTo('#bio');

    // get a list of all artists lastfm_names
    $.getJSON("/api/helper/all-lastfm-artists", function(allArtistsLastfmNames) {

        // filter-out related artists that don't exist in the DB
        var relatedArtists = _.filter(artistInfo.artist.similar.artist, function(a) {
            return _.contains(allArtistsLastfmNames, a.name);
        });

        // normalize lastFM relatedArtists to my artist object model
        var myRelatedArtists = [];
        for (var i=0 ; i < relatedArtists.length ; i++ ) {
            var artist = {};
            artist.view = "/artists/lastfm/" + relatedArtists[i].name;
            artist.lastfm_name = relatedArtists[i].name;
            artist.lastfm_image = _.find(relatedArtists[i].image, function(image) {
                return image.size === "extralarge"; }
            )['#text'];

            myRelatedArtists.push(artist);
        }
        // render relatedArtists
        handlebarsRenderArtists(myRelatedArtists);
    });
});
