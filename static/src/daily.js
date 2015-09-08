(function(obj) {
    obj.isRight = function() {
        console.log("isRight!");
    };
    obj.isFunction = function(para) {
        return Object.prototype.toString.call(para) == '[object Function]';
    };

    var PubSub = {
        subscribe: function(ev, callback) {
            // 创建 _callbacks 对象，除非它已经存在了
            var calls = this._callbacks || (this._callbacks = {});
            // 针对给定的事件key创建一个数组，除非这个数组已经存在
            // 然后将回调函数追加到这个数组中
            (this._callbacks[ev] || (this._callbacks[ev] = [])).push(callback);
            return this;
        },

        publish: function() {
            // 将arguments对象转换成真正的数组
            var args = Array.prototype.slice.call(arguments, 0);

            // 拿出第一个参数，作为事件名
            var ev = args.shift();

            // 如果不存在 _callbacks ，则返回
            // 或者如果不包含给定事情对应的数组
            var list, calls, i, l;
            if (!(calls = this._callbacks)) {
                return this;
            }
            if (!(list = this._callbacks[ev])) {
                return this;
            }

            // 触发回调
            for (i = 0, l = list.length; i < l; i++) {
                list[i].apply(this, args);
            }
            return this;
        }
    };

    obj.PubSub = PubSub;

})(window);

(function(obj) {

    var APIPaths = {
        "newsLatest": "/daily/api/news_latest",
        "newsHot": "/daily/api/news_hot",
        "newsSections": "/daily/api/news_sections",
        "startImage": "/daily/api/start_image"
    };

    obj.daily = {};

    obj.daily.getJSON = getJSON;
    obj.daily.getNewsLastest = getNewsLastest;
    obj.daily.getNewsHot = getNewsHot;
    obj.daily.getStartImage = getStartImage;

    function getJSON(url, success, fail, always) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.send(null);
        xhr.onreadystatechange = function() {
            if (xhr.status == 200 && xhr.readyState == 4) {
                var response = JSON.parse(xhr.responseText);
                if (isFunction(success)) {
                    success(response);
                }
            } else {
                if (isFunction(fail)) {
                    fail();
                }
            }
        };
    }

    function getNewsLastest(callback) {
        var url = APIPaths.newsLatest;
        getJSON(url, function(response) {
            console.log("success! new latest");
            if (callback) {
                callback(response);
            }
        });
    }

    function getNewsHot(callback) {
        var url = APIPaths.newsHot;
        getJSON(url, function(response) {
            console.log("success! new hot");
            callback(response);
        });
    }

    function getStartImage() {
        var url = APIPaths.startImage;
        getJSON(url, function(response) {
            console.log("success! start image");
            var img = new Image();
            var img_url = response.img;
            img.onload = function() {
                //                document.body.style.backgroundImage = 'url("' + img_url + '")';
            };
            img.src = img_url;

        });
    }

})(window);


(function(window) {

    function updateNewsLastest(response) {
        console.log(response);
        var tmpl_top = _.template($('#tmpl-stories').html());
        $("#stories_list").html(tmpl_top(response));

    }

    function updateNewsHot(response) {
        console.log(response);
        var tmpl_recent = _.template($('#tmpl-hot').html());
        $("#stories_list").html(tmpl_recent(response));
    }

    window.onload = function() {
        daily.getNewsLastest(updateNewsLastest);
        daily.getNewsHot(updateNewsHot);
        daily.getStartImage();

    };

    window.onhashchange = function() {
        // alert(window.location.hash);
        var hash = window.location.hash;
        switch (hash) {
            case '#news_lastest':
                PubSub.publish('show_lastest_news');
                break;
            case '#news_hot':
                PubSub.publish('show_hot_news');
                break;
            default:
                console.log('???');
                break;
        }
        //        PubSub.publish("changehash");

    };
    // 使用方法
    PubSub.subscribe("show_lastest_news", function() {
        daily.getNewsLastest(updateNewsLastest);
    });
    PubSub.subscribe("show_hot_news", function() {
        daily.getNewsHot(updateNewsHot);
    });
    PubSub.subscribe('changehash', function() {})

})(window);
