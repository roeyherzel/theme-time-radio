/* -------------------------------
 * Episode Player
 * -------------------------------
 */

const episodePlayer = (function () {

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

        init: function () {
            const $player = $('#episode_player');

            if ($player.length) {
                this.$duration = $player.find(".eplayer-duration");
                this.$current = $player.find(".eplayer-current");
                this.$bufferedBar = $player.find(".eplayer-buffered-bar");
                this.$playedBar = $player.find(".eplayer-played-bar");
                this.$playedInput = $player.find(".eplayer-played-input");
                this.$playPauseBtn = $player.find(".eplayer-playpause");

                this.audio = $player.find('audio').get(0);
                this.bindUIAction();
                return this.audio;
            }

        },

        bindUIAction: function () {
            this.audio.addEventListener('loadedmetadata', this.onDataLoad);
            this.audio.addEventListener('loadeddata', this.onDataLoad);
            this.audio.addEventListener('loadstart', this.onBuffering);
            this.audio.addEventListener('loadeddata', this.onBuffering);
            this.audio.addEventListener('progress', this.onBuffering);
            this.audio.addEventListener('timeupdate', this.onTimeUpdate);
            this.audio.addEventListener('play', this.onPlay);
            this.audio.addEventListener('pause', this.onPause);
            this.audio.addEventListener('seeking', this.onSeeking);
            this.audio.addEventListener('seeked', this.onSeeked);

            this.$playPauseBtn.on('click', this.toggolePlayPause);
            this.$playedInput.on('change', this.onSkip);
            this.$playedInput.on('input', this.onSkip);

        },

        onDataLoad: function (event) {
            Media.$playedBar.prop('max', event.target.duration);
            Media.$playedInput.prop('max', event.target.duration);
            Media.$bufferedBar.prop('max', event.target.duration);
            Media.$duration.text(formatTime(event.target.duration));
        },

        onBuffering: function (event) {
            if (event.target.buffered.length) {
                Media.$bufferedBar.prop('value', event.target.buffered.end(0));
            }
        },

        onTimeUpdate: function (event) {
            Media.$playedBar.prop('value', event.target.currentTime);
            Media.$playedInput.prop('value', event.target.currentTime);
            Media.$current.text(formatTime(event.target.currentTime));
        },

        onSeeking: function (event) {
            Media.audio.pause();
        },

        onSeeked: function (event) {
            Media.audio.play();
        },

        onSkip: function (event) {
            Media.audio.currentTime = event.target.value;
            Media.$current.text(formatTime(event.target.value));
        },

        onPlay: function (event) {
            Media.$playPauseBtn.attr('data-status', 'playing');
        },

        onPause: function (event) {
            Media.$playPauseBtn.attr('data-status', 'paused');
        },

        toggolePlayPause: function (event) {
            if (Media.audio.paused) {
                Media.audio.play();
            } else {
                Media.audio.pause();
            }
        }

    };

    return Media.init();

})();

export default episodePlayer;