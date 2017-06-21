/* ----------
 * LastFM API
 * ----------*/
import $ from 'jquery'

const _get = (method, resource) => {
    const data = {
        api_key: 'aa570c383c5f26de24d4e2c7fd182c8e',
        format: 'json',
        method: method + '.getinfo',
    };
    data[method] = resource;
    return $.getJSON('https://ws.audioscrobbler.com/2.0/', data);
};

const getArtistInfo = (artist) => _get('artist', artist);
const getGenreInfo  = (genre)  => _get('tag', genre);

// Exports
export {
    getArtistInfo,
    getGenreInfo
};