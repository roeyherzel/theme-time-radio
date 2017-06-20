import API from '../js/api';
import HBS from '../js/hbs';


! function () {
    const episode = $('h1[data-episode-id]').attr('data-episode-id');

    API.getEpisodeTracks(episode)
        .then((tracks) => {
            // extract uniq artists from tracks and render
            let artists = _.flatten(_.map(tracks, (t) => t.spotify_artists)); // TODO: change _.map to tracks.map
            artists = _.uniq(artists, (a) => a.name);
            HBS.renderArtists(artists);
        });
}();