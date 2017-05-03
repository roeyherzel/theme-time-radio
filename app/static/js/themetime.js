
/* ThemeTime.js
 * ============
 *
 */

const App = {};

/* -------------------------
 * theme-time web server API
 * -------------------------
 */

App.api = (function() {

  const _get = (path, params) => $.getJSON(path, params);

  const getArtists       = (params) => _get('/api/artists', params);
  const getGenres        = ()       => _get('/api/genres');
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
            .then(tracks => App.templates.renderTracks(tracks));
  };

  const getEpisodeTracks = (id) => {
    return _get(`/api/episodes/${id}/tracklist`)
            .then(tracks => App.templates.renderTracks(tracks));
  };

  const getGenreTracks = (genre) => {
    return _get(`/api/genres/${genre}/tracklist`)
            .then(tracks => App.templates.renderTracks(tracks));
  };


  // Exports
  return { getArtists, getArtistTracks, getGenres, getGenreTracks, getGenreArtists, getEpisodeTracks, getLastfmArtist };
})();


/* --------------------
 * Handlebars templates
 * --------------------
 */

App.templates = (function() {

  const _get = (file, data, ph) => {
    return $.get(`/static/handlebars/${file}.hbs`)
            .then((template) => Handlebars.compile(template))
            .then((template) => $(ph).html(template(data)))
            .then(() => data);
  };

  const _createLinkItem = (name, address) => $('<li>').append(`<a href=${address}>${name}</a>`);

  const renderTracks = (tracks, ph = '#tracklist_placeholder') => {
    return _get('track_cards', {tracks}, ph)
            .then((tracks) => {
              App.trackPlayer.init();
              return tracks.tracks;
            });
  };

  const renderArtists = (artists, ph = '#artists_placeholder') => {
    _get('artists_list', {artists}, ph);
  };

  const renderArtistBio = (data, ph) => {
    $(ph).html($('<p>').html(data.artist.bio.summary));
    return data; // returning data for chaining more promises
  };

  const renderGenreSummary = (data, ph) => $(ph).html($('<p>').html(data.tag.wiki.summary));

  const renderGroups = (data) => {
    // Group data by first char, if char is not a-Z then group = #
    data = _.groupBy(data, (a) => (/[a-z]/i).test(a.name.charAt(0)) ? a.name.charAt(0).toUpperCase() : "#");
    // Create group section with list of items
    for (let group in data) {
      const $section  = $(`<section id=${group}></section>`).append(`<h2>${group}</h2>`);
      const $group_ul = $('<ul>').appendTo($section);

      for (let i of data[group]) {
        $group_ul.append(_createLinkItem(i.name, i.view));
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
      $nav_ul.append(_createLinkItem(g, `#${g}`));
    }
  };

  // Exports
  return { renderTracks, renderArtists, renderArtistBio, renderGenreSummary, renderGroups };
})();


/* ----------
 * LastFM API
 * ----------
 */

App.lastFM = (function() {

  const _get = (method, resource) => {
    const data = {
      api_key: 'aa570c383c5f26de24d4e2c7fd182c8e',
      format: 'json',
      method: method + '.getinfo',
    };
    data[method] = resource;
    return $.getJSON('http://ws.audioscrobbler.com/2.0/', data);
  };

  const getArtistInfo = (artist) => _get('artist', artist);
  const getGenreInfo  = (genre)  => _get('tag', genre);

  // Exports
  return { getArtistInfo, getGenreInfo };
})();


/* -------------------------------
 * Episode Player
 * -------------------------------
 */

App.episodePlayer = (function() {

  const formatTime = (seconds) => {
    let minutes, minutes_float;
    minutes_float = seconds / 60;
    minutes = Math.floor(minutes_float);
    seconds = Math.floor((minutes_float - minutes) * 60);

    // Convert number to string and pad start with 0 if needed
    seconds = seconds.toString();
    seconds = seconds.length === 1 ? '0' + seconds : seconds;
    return minutes + ':' + seconds;
  };

  const Media = {
    init: function() {
      const $player  = $('#episode_player');
      const url      = $player.attr('data-media-url');

      if ($player && url) {
        this.$duration     = $player.find(".eplayer-duration");
        this.$current      = $player.find(".eplayer-current");
        this.$bufferedBar  = $player.find(".eplayer-buffered-bar");
        this.$playedBar    = $player.find(".eplayer-played-bar");
        this.$playedInput  = $player.find(".eplayer-played-input");
        this.$playPauseBtn = $player.find(".eplayer-playpause");

        this.url = $player.attr('data-media-url');
        this.audio = new Audio(this.url);

        this.bindUIAction();
        return this.audio;
      }

    },

    bindUIAction: function() {
      this.audio.addEventListener('loadedmetadata', this.onDataLoad);
      this.audio.addEventListener('loadeddata'    , this.onDataLoad);
      this.audio.addEventListener('loadstart'     , this.onBuffering);
      this.audio.addEventListener('loadeddata'    , this.onBuffering);
      this.audio.addEventListener('progress'      , this.onBuffering);
      this.audio.addEventListener('timeupdate'    , this.onTimeUpdate);
      this.audio.addEventListener('play'          , this.onPlay);
      this.audio.addEventListener('pause'         , this.onPause);

      this.$playPauseBtn.on('click', this.toggolePlayPause);
      this.$playedInput.on('input' , this.onSkip);
      this.$playedInput.on('change', this.onSkip);
    },

    onDataLoad: function(event) {
      Media.$playedBar.prop('max', event.target.duration);
      Media.$playedInput.prop('max', event.target.duration);
      Media.$bufferedBar.prop('max', event.target.duration);
      Media.$duration.text(formatTime(event.target.duration));
    },

    onBuffering: function(event) {
      if (event.target.buffered.length) {
        Media.$bufferedBar.prop('value', event.target.buffered.end(0));
      }
    },

    onTimeUpdate: function(event) {
      Media.$playedBar.prop('value', event.target.currentTime);
      Media.$playedInput.prop('value', event.target.currentTime);
      Media.$current.text(formatTime(event.target.currentTime));
    },

    onSkip: function(event) {
      if (event.type === 'input') {
        Media.audio.pause();
        Media.$current.text(formatTime(event.target.value));
      } else if (event.type === 'change') {
        // Trigger timeupdate
        Media.audio.currentTime = event.target.value;
        Media.audio.play();
      }
    },

    onPlay: function(event) {
      Media.$playPauseBtn.attr('data-status', 'playing');
    },

    onPause: function(event) {
      Media.$playPauseBtn.attr('data-status', 'paused');
    },

    toggolePlayPause: function(event) {
      if (Media.audio.paused) {
        Media.audio.play();
      } else {
        Media.audio.pause();
      }
    }

  };

  return Media.init();

})();


/* -------------------------------
 * Track Player
 * -------------------------------
 */

App.trackPlayer = (function() {

  const cachedAudio = new Map();
  const getAudio = (previewBtn) => {

    if (cachedAudio.has(previewBtn)) {
      return cachedAudio.get(previewBtn);
    } else {
      const $btn = $(previewBtn);
      const audio = new Audio($btn.attr('data-media-url'));

      // bind handlers
      audio.addEventListener('play' , (e) => $btn.attr('data-status', 'playing'));
      audio.addEventListener('pause', (e) => onPause(e, $btn));
      audio.addEventListener('ended', (e) => onPause(e, $btn));

      // Add to cache
      cachedAudio.set(previewBtn, audio);
      return audio;
    }
  };

  const onPause = (event, $btn) => {
    event.target.currentTime = 0;
    $btn.attr('data-status', 'paused');
  };

  const toggolePlayPause = (event) => {
    const previewBtn = event.currentTarget;
    const audio = getAudio(previewBtn);

    // Pause all other tracks
    for (let cached of cachedAudio.values()) {
      if (cached !== audio) {
        cached.pause();
      }
    }
    // Toggle state
    if (audio.paused) {
      audio.play();
    } else {
      audio.pause();
    }
  };

  const init = () => {
    const $tracks = $('.track-preview[data-media-url!=""]');
    if ($tracks) {
      $tracks.on('click', toggolePlayPause);
    }
    console.log($tracks);
  };

  return { init };

})();
