import { Episodes } from '../js/app';
import EpisodePlayer from '../js/player_episode';

! function () {
    const episode = $('h1[data-episode-id]').attr('data-episode-id');
    Episodes.renderTracks(episode);
    console.log(EpisodePlayer);
    EpisodePlayer();
}();