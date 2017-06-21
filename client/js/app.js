import $ from 'jquery'
import _ from 'underscore'
import * as API from './api';
import * as LastFM from './lastfm';
import * as Templates from './templates';


const Episodes = {
    renderThumbs: (opt) => {
        API.getEpisodes(opt)
            .then((episodes) => Templates.renderThumbs('episodes', episodes, '#episodes_placeholder'));
    },
    renderTracks: (episode) => {
        API.getEpisodeTracks(episode)
            .then((tracks) => Templates.renderTracks(tracks))
            .then((tracks) => {
                // extract uniq artists from tracks and render
                let artists = _.flatten(tracks.map((t) => t.spotify_artists));
                artists = _.uniq(artists, (a) => a.name);
                Templates.renderThumbs('artists', artists, '#artists_placeholder');
            }
        );
    }
};

const Artists = {
    renderThumbs: (opt) => {
        API.getArtists(opt)
            .then((artists) => Templates.renderThumbs('artists', artists, '#artists_placeholder'));
    },
    renderGroups: () => {
        API.getArtists()
            .then((genres) => Templates.renderGroups(genres));
    },
    renderTracks: (artist) => {
        API.getArtistTracks(artist)
            .then((tracks) => Templates.renderTracks(tracks));
    },
    renderInfo: (artist) => {
        LastFM.getArtistInfo(artist)
            .then((info) => Templates.renderArtistBio(info, '#bio'))
            .then((info) => Artists._renderRelated(info))
            .catch((error) => console.error(error));
    },
    _renderRelated: (info) => {
        let apiCalls = [];
        info.artist.similar.artist.forEach((a) => {
            apiCalls.push(API.getArtistByLastfm(a.name));
        });
        Promise.all(apiCalls)
            .then(artists => {
                // filter unmatched artists
                artists = artists.filter(i => i !== undefined);
                if (artists.length === 0) {
                    console.log("theme-time Didn't find related artists");
                    $('#artists_placeholder').parent().hide();
                } else {
                    Templates.renderThumbs('artists', artists, '#artists_placeholder');
                }
            });
    },
}

const Genres = {
    renderThumbs: (opt) => {
        API.getGenres(opt)
            .then((genres) => Templates.renderThumbs('genres', genres, '#genres_placeholder'));
    },
    renderGroups: () => {
        API.getGenres()
            .then((genres) => Templates.renderGroups(genres));
    },
    renderTracks: (genre) => {
        API.getGenreTracks(genre)
            .then((tracks) => Templates.renderTracks(tracks));
    },
    renderArtists: (genre) => {
        API.getGenreArtists(genre)
            .then((artists) => Templates.renderThumbs('artists', artists, '#artists_placeholder'));
    },
    renderSummary: (genre) => {
        LastFM.getGenreInfo(genre)
            .then((data) => Templates.renderGenreSummary(data, '#desc'));
    },
}

export {Episodes, Artists, Genres};