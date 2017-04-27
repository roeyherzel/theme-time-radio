
/*
 * JS functionality per page
 * =========================
 */
const Pages = (function(){

  const ArtistInfo = () => {
    const artistId = $('#page header h1').attr('data-artist-id');
    const artistName = $('#page header h1').attr('data-artist-lastfm');

    TTR.API.getArtistTracks(artistId).then(tracks => TTR.HBS.renderTracks(tracks));
    TTR.LastFM.getArtistInfo(artistName)
              .then(data => TTR.LastFM.renderArtistBio(data,'#bio'))
              .then(data => {
                let apiCalls = [];
                for (let a of data.artist.similar.artist) {
                  apiCalls.push(TTR.API.getLastfmArtist(a.name));
                }
                Promise.all(apiCalls)
                      .then(data => {
                        // filter unmatched artists
                        data = data.filter(i => i !== undefined);
                        if (data.length === 0) {
                          console.log(`${artistName} - Don't have related artists on theme-time`);
                          $('#artists_placeholder').parent().hide();
                        } else {
                          TTR.HBS.renderArtists(data, '#artists_placeholder');
                        }
                      });
                });
  };

  const Artists = () => {
    TTR.API.getArtists({ limit: 6, random: true }).then(TTR.HBS.renderArtists);
    TTR.API.getArtists().then(TTR.Components.renderGroups);
  };

  const EpisodeInfo = () => {
    const episode = $('h1[data-episode-id]').attr('data-episode-id');

    TTR.API.getEpisodeTracks(episode)
        .then((tracks) => TTR.HBS.renderTracks(tracks))
        .then((tracks) => {
          // extract uniq artists from tracks and render
          let artists = _.flatten(_.map(tracks, (t) => t.spotify_artists));
          artists = _.uniq(artists, (a) => a.name);
          TTR.HBS.renderArtists(artists);
        });
  };

  const GenreInfo = () => {
    const genre = $('#page header h1').attr('data-genre-name');

    TTR.API.getGenreTracks(genre).then((tracks) => TTR.HBS.renderTracks(tracks));
    TTR.API.getGenreArtists(genre).then((artists) => TTR.HBS.renderArtists(artists));
    TTR.LastFM.getGenreInfo(genre).then((data) => TTR.LastFM.renderGenreSummary(data, '#desc'));
  };

  const Genres = () => {
    TTR.API.getGenres().then(TTR.Components.renderGroups);
  };

  return {
    ArtistInfo,
    Artists,
    EpisodeInfo,
    GenreInfo,
    Genres
  };

}());
