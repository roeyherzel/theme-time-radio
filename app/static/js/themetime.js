
/* ThemeTime.js
 * ============
 *
 *
 */

const TTR = (function() {
/* =========================================================================
 * theme-time web server API
 * =========================================================================
 */
  const API = {
    _get: function(path, params) {
      return $.getJSON(path, params);
    },

    getArtists: function(params) {
      return API._get('/api/artists', params);
    },

    getArtistTracks: function(id) {
      return API._get(`/api/artists/${id}/tracklist`);
    },

    getGenres: function() {
      return API._get('/api/genres');
    },

    getGenreTracks: function(genre) {
      return API._get(`/api/genres/${genre}/tracklist`);
    },

    getGenreArtists: function(genre) {
      return API._get(`/api/genres/${genre}/artists`);
    },

    getEpisodeTracks: function(id) {
      return API._get(`/api/episodes/${id}/tracklist`);
    },

    getLastfmArtist: function(lastfmName) {
      return new Promise((resolve, reject) => {
        API._get(`/api/artists/${lastfmName}`, {lastfm: true})
           .catch(error => console.log(`${lastfmName} on not in theme-time`))
           .then(data => resolve(data));
      });
    },
  };

/* =========================================================================
 * Handlebars templates
 * =========================================================================
 */
  const HBS = {
    _get: function(file, data, ph) {
      return $.get(`/static/handlebars/${file}.hbs`)
             .then((template) => Handlebars.compile(template))
             .then((template) => $(ph).html(template(data)));
    },

    renderTracks: function(tracks, ph = '#tracklist_placeholder') {
      HBS._get('track_cards', {tracks}, ph);
      return tracks;
    },

    renderArtists: function(artists, ph = '#artists_placeholder') {
      HBS._get('artists_list', {artists}, ph);
    }
  };

/* =========================================================================
 * LastFM API
 * =========================================================================
 */
  const LastFM = {
    _get: function(method, resource) {
      const data = {
        api_key: 'aa570c383c5f26de24d4e2c7fd182c8e',
        format: 'json',
        method: method + '.getinfo',
      };
      data[method] = resource;
      return $.getJSON('http://ws.audioscrobbler.com/2.0/', data);
    },

    getArtistInfo: function(artist) {
      return LastFM._get('artist', artist);
    },

    getGenreInfo: function(genre) {
      return LastFM._get('tag', genre);
    },

    renderArtistBio: function(data, ph) {
      $(ph).html($('<p>').html(data.artist.bio.summary));
      return data;
    },

    renderGenreSummary: function(data, ph) {
      $(ph).html($('<p>').html(data.tag.wiki.summary));
    }
  };

/* =========================================================================
 * Components (jQuery rendered)
 * =========================================================================
 */
  const Components = {
    _createLinkItem: function(name, address) {
      return $('<li>').append(`<a href=${address}>${name}</a>`);
    },

    renderGroups: function(data) {
      // Group data by first char, if char is not a-Z then group = #
      data = _.groupBy(data, (a) => (/[a-z]/i).test(a.name.charAt(0)) ? a.name.charAt(0).toUpperCase() : "#");
      // Create group section with list of items
      for (let group in data) {
        const $section  = $(`<section id=${group}></section>`).append(`<h2>${group}</h2>`);
        const $group_ul = $('<ul>').appendTo($section);

        for (let i of data[group]) {
          $group_ul.append(Components._createLinkItem(i.name, i.view));
        }
        $('#groups').append($section);
      }
      // Create group navigation with dropdown and list of groups
      const $nav_container = $('#groups_nav');
      const $nav_checkbox  = $('<input id="toggle_group_nav" type="checkbox">');
      const $nav_label     = $('<label for="toggle_group_nav">A - Z</label>');
      const $nav_nav       = $('<nav>');
      const $nav_ul        = $('<ul>').appendTo($nav_nav);
      $nav_container.append($nav_checkbox, $nav_label, $nav_nav);

      for (let g of _.keys(data)) {
        $nav_ul.append(Components._createLinkItem(g, `#${g}`));
      }
    },
  };

/* =========================================================================
 * Export public methods
 * =========================================================================
 */
  return {
    API: {
      getArtists      : API.getArtists,
      getArtistTracks : API.getArtistTracks,
      getGenres       : API.getGenres,
      getGenreTracks  : API.getGenreTracks,
      getGenreArtists : API.getGenreArtists,
      getEpisodeTracks: API.getEpisodeTracks,
      getLastfmArtist : API.getLastfmArtist
    },
    HBS: {
      renderTracks : HBS.renderTracks,
      renderArtists: HBS.renderArtists
    },
    LastFM: {
      getArtistInfo     : LastFM.getArtistInfo,
      getGenreInfo      : LastFM.getGenreInfo,
      renderArtistBio   : LastFM.renderArtistBio,
      renderGenreSummary: LastFM.renderGenreSummary
    },
    Components: {
      renderGroups: Components.renderGroups
    }
  };
}()); // end module
