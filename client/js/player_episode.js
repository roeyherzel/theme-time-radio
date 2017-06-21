/* -------------------------------
 * Episode Player
 * -------------------------------*/
import $ from 'jquery'

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

class Media {
    constructor($player) {
        this.$duration     = $player.find(".eplayer-duration");
        this.$current      = $player.find(".eplayer-current");
        this.$bufferedBar  = $player.find(".eplayer-buffered-bar");
        this.$playedBar    = $player.find(".eplayer-played-bar");
        this.$playedInput  = $player.find(".eplayer-played-input");
        this.$playPauseBtn = $player.find(".eplayer-playpause");

        this.audio = $player.find('audio').get(0);
        this.bindUIAction();
    }

    bindUIAction() {
        this.audio.addEventListener('loadedmetadata', (e) => this.onDataLoad(e));
        this.audio.addEventListener('loadeddata', (e)     => this.onDataLoad(e));
        this.audio.addEventListener('loadstart', (e)      => this.onBuffering(e));
        this.audio.addEventListener('loadeddata', (e)     => this.onBuffering(e));
        this.audio.addEventListener('progress', (e)       => this.onBuffering(e));
        this.audio.addEventListener('timeupdate', (e)     => this.onTimeUpdate(e));
        this.audio.addEventListener('play', ()            => this.onPlay());
        this.audio.addEventListener('pause', ()           => this.onPause());
        this.audio.addEventListener('seeking', ()         => this.onSeeking());
        this.audio.addEventListener('seeked', ()          => this.onSeeked());

        this.$playPauseBtn.on('click', ()  => this.toggolePlayPause());
        this.$playedInput.on('change', (e) => this.onSkip(e));
        this.$playedInput.on('input', (e)  => this.onSkip(e));
    }

    onDataLoad(e) {
        this.$playedBar.prop('max', e.target.duration);
        this.$playedInput.prop('max', e.target.duration);
        this.$bufferedBar.prop('max', e.target.duration);
        this.$duration.text(formatTime(e.target.duration));
    }

    onBuffering(e) {
        if (e.target.buffered.length) {
            this.$bufferedBar.prop('value', e.target.buffered.end(0));
        }
    }

    onTimeUpdate(e) {
        this.$playedBar.prop('value', e.target.currentTime);
        this.$playedInput.prop('value', e.target.currentTime);
        this.$current.text(formatTime(e.target.currentTime));
    }

    onSkip(e) {
        this.audio.currentTime = e.target.value;
        this.$current.text(formatTime(e.target.value));
    }

    onSeeking() {
        this.audio.pause();
    }

    onSeeked() {
        this.audio.play();
    }

    onPlay() {
        this.$playPauseBtn.attr('data-status', 'playing');
    }

    onPause() {
        this.$playPauseBtn.attr('data-status', 'paused');
    }

    toggolePlayPause() {
        if (this.audio.paused) {
            this.audio.play();
        } else {
            this.audio.pause();
        }
    }
};

const init = () => {
    const $player = $('#episode_player');
    if ($player.length) {
        const media = new Media($player);
        return media;
    }
};

export default init;