
// Helper for converting \n to <br>
Handlebars.registerHelper('nl2br', function(string, options) {
  return string.replace(/\n/g,"<br>");
});


// helper for artists name
Handlebars.registerHelper('getArtistTitle', function(spotify_artists, parsed_artist, options) {

  if (spotify_artists.length > 0) {
    return _.map(spotify_artists, function(a) { return `<a href="/artists/${a.artist.id}">${a.artist.name}</a>` })
            .join('&#44;&#32;');  // comma;space;
  } else {
    return parsed_artist;
  }
});

// helper for song name
Handlebars.registerHelper('getSongTitle', function(spotify_song, parsed_song, episode_id, options) {

  var songName = (spotify_song.song.id) ? spotify_song.song.name : parsed_song;

  if (typeof(episode_id) === typeof(Number())) {
    songName = `<a href="/episodes/${episode_id}">${songName}</a>`;
  }
  return songName;
});

// helper for LastFM images
Handlebars.registerHelper('lastFmImage', function(imageArr, size, options) {
  if (typeof(size) !== "string") {
    console.error("size is missing, must be String", typeof(size));
  }
  return _.findWhere(imageArr, {'size': size})["#text"];
});


// helper for generating artist groups index
Handlebars.registerHelper('indexGroups', function(groups, options) {
  groups = _.map(Object.keys(groups), function(g) {
    return `<a href=#${g}>${g}</a>`;
  });

  var groupsLinks = groups.join(" | "),
      nav = `<nav>${groupsLinks}</nav>`;

  return nav;
});


// helper for return length in form of badge
Handlebars.registerHelper('badgeLength', function(data, options) {
  return `<span class="badge">${data.length}</span>`;
})
