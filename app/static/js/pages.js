
/*
 * JS functionality per page
 * =========================
 */

const Pages = {};

Pages.ArtistInfo = () => {

  const artistId = $('#page header h1').attr('data-artist-id');
  const artistName = $('#page header h1').attr('data-artist-lastfm');

  App.api.getArtistTracks(artistId);

  App.lastFM.getArtistInfo(artistName)
            .then(data => App.templates.renderArtistBio(data,'#bio'))
            .then(data => {
              let apiCalls = [];
              for (let a of data.artist.similar.artist) {
                apiCalls.push(App.api.getLastfmArtist(a.name));
              }
              Promise.all(apiCalls)
                    .then(data => {
                      // filter unmatched artists
                      data = data.filter(i => i !== undefined);
                      if (data.length === 0) {
                        console.log(`${artistName} - Don't have related artists on theme-time`);
                        $('#artists_placeholder').parent().hide();
                      } else {
                        App.templates.renderArtists(data);
                      }
                    });
              });
};

Pages.Artists = () => {
  App.api.getArtists({ limit: 6, random: true })
        .then(artists => App.templates.renderArtists(artists));
  App.api.getArtists()
        .then(artists => App.templates.renderGroups(artists));
};

Pages.EpisodeInfo = () => {
  const episode = $('h1[data-episode-id]').attr('data-episode-id');

  App.api.getEpisodeTracks(episode)
        .then((tracks) => {
          // extract uniq artists from tracks and render
          let artists = _.flatten(_.map(tracks, (t) => t.spotify_artists));
          artists = _.uniq(artists, (a) => a.name);
          App.templates.renderArtists(artists);
        });
};

Pages.GenreInfo = () => {
  const genre = $('#page header h1').attr('data-genre-name');

  App.api.getGenreTracks(genre);
  App.api.getGenreArtists(genre)
        .then((artists) => App.templates.renderArtists(artists));
  App.lastFM.getGenreInfo(genre)
        .then((data) => App.templates.renderGenreSummary(data, '#desc'));
};

Pages.Genres = () => {
  App.api.getGenres()
        .then(App.templates.renderGroups);
};
