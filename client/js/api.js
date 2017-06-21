/* -------------------------
 * theme-time web server API
 * -------------------------*/
import $ from 'jquery'

const _get = (path, params) => $.getJSON(path, params);

const getEpisodes      = (params) => _get('/api/episodes', params);
const getEpisodeTracks = (id)     => _get(`/api/episodes/${id}/tracklist`);
const getArtists       = (params) => _get('/api/artists', params);
const getArtistTracks  = (id)     => _get(`/api/artists/${id}/tracklist`);
const getGenres        = (params) => _get('/api/genres', params);
const getGenreArtists  = (genre)  => _get(`/api/genres/${genre}/artists`);
const getGenreTracks   = (genre)  => _get(`/api/genres/${genre}/tracklist`);

const getArtistByLastfm = (lastfmName) => {
    return new Promise((resolve) => {
        _get(`/api/artists/${lastfmName}`, { lastfm: true })
            .then((data) => resolve(data))
            .catch(() => {
                console.log(`${lastfmName} on not in theme-time`);
                resolve();
            });
    });
};

// Exports
export {
    getEpisodes,
    getEpisodeTracks,
    getArtists,
    getArtistTracks,
    getGenres,
    getGenreTracks,
    getGenreArtists,
    getArtistByLastfm
};