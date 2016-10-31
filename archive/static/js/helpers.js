
// Helper for converting \n to <br>
Handlebars.registerHelper('nl2br', function(string, options) {
  return string.replace(/\n/g,"<br>");
});


// helper for artists name
Handlebars.registerHelper('artistName', function(spotify_artists, parsed_artist, options) {

  if (spotify_artists.length === 0) {
    return parsed_artist;

  } else if (spotify_artists.length === 1) {
    return "<a href=/artists/" + spotify_artists[0].artist.id + ">" + spotify_artists[0].artist.name + "</a>";

  } else if (spotify_artists.length > 1) {
    var artists = [];
    for(var i=0, l=spotify_artists.length; i<l; i++) {
      artists.push("<a href=/artists/" + spotify_artists[i].artist.id + ">" + spotify_artists[i].artist.name + "</a>");
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


// helper for generating artist groups index
Handlebars.registerHelper('indexGroups', function(artists, options) {
  var groups = _.map(Object.keys(artists), function(g) {
    return `<a href=#${g}>${g}</a>`;
  });

  var groupsLinks = groups.join(" | "),
      nav = `<nav>${groupsLinks}</nav>`;

  return nav;
});
