import $ from 'jquery';
import { Episodes } from '../app';
import EpisodePlayer from '../player_episode';

! function () {
    const episode = $('h1[data-episode-id]').attr('data-episode-id');
    Episodes.renderTracks(episode);
    EpisodePlayer();
}();