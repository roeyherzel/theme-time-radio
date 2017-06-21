/* -------------------------------
 * Track Player
 * -------------------------------*/

const cachedAudio = new Map();
const getAudio = (previewBtn) => {

    if (cachedAudio.has(previewBtn)) {
        return cachedAudio.get(previewBtn);
    } else {
        const $btn = $(previewBtn);
        const audio = new Audio($btn.attr('data-media-url'));

        // bind handlers
        audio.addEventListener('play', () => $btn.attr('data-status', 'playing'));
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
};


export default { init };