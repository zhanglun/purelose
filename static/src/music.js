/**
 * Created by CrispElite on 2015/1/29 0029.
 */


var app = (function ($) {
    var _files, _context, _analyser, _ctx, _source, _gainNode, _Util, _init, _loadMusic, _playMusic, _visualizer, _initCanvas;
    var SIZE = 128;
    var _W, _H;
    _Util = (function () {
        var _getRandomInt = function (min, max) {
            return Math.floor(Math.random() * (max - min) + min);
        };

        var beforeLoaded = function(){

        };
        return {
            getRandomInt: _getRandomInt
        }
    })();

    _init = function () {
        var onListItemClickListener, onPlayButtonClickListener, onVolumeChangeListener, initalizeUi;
        _W = $(window).width();
        _H = $(window).height();
        _context = new (window.AudioContext || window.webkitAudioContext )();

        _source = null;
        _analyser = _context.createAnalyser();
        _analyser.fftSize = SIZE * 2;
        _gainNode = _context[_context.createGain ? 'createGain' : 'createGainNode']();
        _analyser.connect(_gainNode);
        _gainNode.connect(_context.destination);

        onListItemClickListener = function (name, url) {
            var a, file;
//            a = $(this);
            file = {
                name: name,
                uri: url
            };
            console.log('loadmusic');
            app.loadMusic(file, function () {
                console.log('loadmusic callback');
                app.playMusic(name);
                app.visualizer();
            });
        };

        onPlayButtonClickListener = function () {
            var url, file;

            url = $('#external').val();

            file = {
                name: 'external',
                uri: url
            };

            app.loadSound(file, function () {
                app.playSound('external');
            });
        };

        onVolumeChangeListener = function () {
            _gainNode.gain.value = parseInt(this.value, 10) / 100;
        };

        initalizeUi = (function () {

            var songListContainer = $('#songList'),
                songListArray = $('li', songListContainer);

            songListContainer.on('click', function (e) {

                var target = e.target;
                if (target.tagName.toLowerCase() !== 'li') {
                    return false;
                }
                songListArray.removeClass('selected');
                $(target).addClass('selected');

                var name = $(target).attr('title');
                var uri = '/static/media/' + name;
                onListItemClickListener(name, uri);
            });
            $('#adjustVol')[0].oninput = onVolumeChangeListener;
        })();
        _initCanvas();
    };

    _initCanvas = function () {
        var canvas = $('#canvas')[0];
        _ctx = canvas.getContext('2d');

        canvas.width = $(window).width();
        canvas.height = $(window).height();

        var line = _ctx.createLinearGradient(0, 0, 0, $(window).height() / 4 * 3);
        line.addColorStop(0, 'red');
        line.addColorStop(0.5, 'yellow');
        line.addColorStop(1, 'green');
        _ctx.fillStyle = line;
    };

    _loadMusic = function (file, successCallback, errorCallback) {
        var xhr,
            isLoaded,
            onRequestLoad,
            onDecodeAudioDataSuccess,
            onDecodeAudioDataError,
            doXHRRequest;

        _files = _files || [];

        successCallback = successCallback || function successCallback() {
        };
        errorCallback = errorCallback || function errorCallback(msg) {
            alert(msg);
        };

        isLoaded = false;
        $.each(_files, function isFileAlreadyLoaded(i) {
            if (_files[i].name === file.name) {
                isLoaded = true;
                return false;
            }
        });

        onDecodeAudioDataSuccess = function (buffer) {
            $('#layer').fadeOut();
            if (!buffer) {
                errorCallback('Error decoding file ' + file.uri + ' data.');
                return;
            }

            _files.push({
                name: file.name,
                uri: file.uri,
                buffer: buffer
            });
            successCallback();
        };

        onDecodeAudioDataError = function (error) {
            errorCallback('Error decoding file ' + file.uri + ' data.' + error);
        };

        onRequestLoad = function () {
            _context.decodeAudioData(xhr.response, onDecodeAudioDataSuccess, onDecodeAudioDataError);
        };
        onRequestError = function () {
            errorCallback('XHR error when loading file ' + file.uri + '.');
        };

        doXHRRequest = function () {
            xhr = new XMLHttpRequest();
            xhr.open('GET', file.uri, true);
            xhr.responseType = 'arraybuffer';
            xhr.onload = onRequestLoad;
            xhr.onerror = onRequestError;
            xhr.send();
        };
        if (isLoaded) {
            successCallback();
        } else {
            doXHRRequest();
        }
    };

    _playMusic = function (name) {
        if (_source && _source.playbackState === _source.PLAYING_STATE) {
            _source[_source.stop ? 'stop' : 'noteOff'](0); // stop()
            _source = null;
        }

        $.each(_files, function (i, file) {
            if (file.name === name) {
                /* Create SourceNode and add buffer to it. */
                _source = _context.createBufferSource();
                _source.buffer = file.buffer;
                /* Connect the SourceNode to the next node in the routing graph
                 * which is the PannerNode and play the sound. */
                _source.connect(_analyser);
                _source[_source.start ? 'start' : 'noteOn'](0); // start()

                return false;
            }
        });
    };

    _visualizer = function () {
        var arr = new Uint8Array(_analyser.frequencyBinCount);
        _analyser.getByteFrequencyData(arr);
        requestAnimationFrame = window.requestAnimationFrame ||
            window.webkitRequestAnimationFrame ||
            window.mozRequestAnimationFrame;

        function getDots() {
            var getRandom = app.Util.getRandomInt;
            var Dots = [];
            for (var i = 0; i < SIZE; i++) {
                var x = getRandom(0, _W),
                    y = getRandom(0, _H),
                    color = 'rgba(' + getRandom(0, 255) + ',' + getRandom(0, 255) + "," + getRandom(0, 255) + ", 0.5)";
                Dots.push({
                    x: x,
                    y: y,
                    color: color
                });
            }
            return Dots;
        }

        var Dots = getDots();

        drawType = 'column';
        function draw(points) {
            _ctx.clearRect(0, 0, _W, _H);
            if (drawType == 'column') {
                var w = _W / SIZE;
                for (var i = 0; i < SIZE; i++) {
                    var h = points[i] / 256 * _H;
                    _ctx.fillRect(w * i * 1.2, $(window).height() - h, w, h);
                }
            } else if (drawType == 'dot') {
                for (var i = 0; i < SIZE; i++) {
                    var o = Dots[i],
                        radius = points[i] / 256 * 50;
                    _ctx.beginPath();
                    _ctx.arc(o.x, o.y, radius, 0, Math.PI * 2, true);
                    var g = _ctx.createRadialGradient(o.x, o.y, 0, o.x, o.y, radius);
                    g.addColorStop(0, '#FFF');
                    g.addColorStop(1, o.color);
                    _ctx.fillStyle = g;
                    _ctx.fill();
                }
            }
        }

        function go() {
            _analyser.getByteFrequencyData(arr);
            draw(arr);
            requestAnimationFrame(go);
        }

        requestAnimationFrame(go);
    };
    return {
        init: _init,
        loadMusic: _loadMusic,
        playMusic: _playMusic,
        visualizer: _visualizer,
        Util: _Util
    }
})(jQuery);

window.onload = function () {
    app.init();
    $('#songList').find('li').eq(0).trigger('click');
};