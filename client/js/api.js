/* -------------------------
 * theme-time web server API
 * -------------------------
 */

import HBS from './hbs';

const API = (function() {

  const _get = (path, params) => $.getJSON(path, params);

  const getArtists       = (params) => _get('/api/artists', params);
  const getEpisodes      = (params) => _get('/api/episodes', params);
  const getGenres        = (params) => _get('/api/genres', params);
  const getGenreArtists  = (genre)  => _get(`/api/genres/${genre}/artists`);

  const getLastfmArtist = (lastfmName) => {
    return new Promise((resolve, reject) => {
      _get(`/api/artists/${lastfmName}`, {lastfm: true})
      .catch(error => console.log(`${lastfmName} on not in theme-time`))
      .then(data => resolve(data));
    });
  };

  const getArtistTracks = (id) => {
    return _get(`/api/artists/${id}/tracklist`)
            .then(tracks => HBS.renderTracks(tracks));
  };

  const getEpisodeTracks = (id) => {
    return _get(`/api/episodes/${id}/tracklist`)
            .then(tracks => HBS.renderTracks(tracks));
  };

  const getGenreTracks = (genre) => {
    return _get(`/api/genres/${genre}/tracklist`)
            .then(tracks => HBS.renderTracks(tracks));
  };

  // Exports
  return { getEpisodes, getArtists, getArtistTracks, getGenres, getGenreTracks, getGenreArtists, getEpisodeTracks, getLastfmArtist };
})();

export default API;