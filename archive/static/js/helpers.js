
// Helper for converting \n to <br>
Handlebars.registerHelper('nl2br', function(string, options) {
  return string.replace(/\n/g,"<br>");
});


// helper for artists name
Handlebars.registerHelper('artistName', function(spotify_artists, parsed_artist, options) {
  if (spotify_artists.length === 0) {
    return parsed_artist;

  } else if (spotify_artists.length === 1) {
    return "<a href=/artists/" + spotify_artists[0].data.id + ">" + spotify_artists[0].data.name + "</a>";

  } else if (spotify_artists.length > 1) {
    var artists = [];
    for(var i=0, l=spotify_artists.length; i<l; i++) {
      artists.push("<a href=/artists/" + spotify_artists[i].data.id + ">" + spotify_artists[i].data.name + "</a>");
    }
    return artists.join('&#44;&#32;');  // comma;space
  }
});


// helper for LastFM images
Handlebars.registerHelper('lastFmImage', function(imageArr, size, options) {
  if (typeof(size) !== "string") {
    console.error("size is missing, must be String", typeof(size));
  }
  return _.findWhere(imageArr, {'size': size})["#text"];
});


// helper for geting artist image from LastFM and returning image url
Handlebars.registerHelper('getArtistImageUrl', function(artistName, size, options) {

  return '#'
    /*getArtistInfo(artistName, function(artistInfo) {
        console.log(artistName);
        return _.findWhere(artistInfo.artist.image, {'size': size})["#text"];
      });*/

});