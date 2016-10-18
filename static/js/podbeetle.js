$(function() {
    function progress() {
        var srcElem = $('div[data-url="' + $(this).attr('src') + '"]');
        if ($(srcElem).attr('data-start-time') > 0) {
            this.currentTime = $(srcElem).attr('data-start-time');
        }
        $(this).unbind('progress');
    }
    $('.item-container').on('click', '.item img', function(e) {
        var parent = $(this).parent();
        var audio = $('.player audio')[0];
        $('.player').show();
        $(audio).attr('src', parent.attr('data-url'));
        $(audio).attr('data-new', 1);
        audio.play();
    });
    $('.player audio').on('play', function(e) {
        if ($('img.play-active')) {
            $('img.play-active').remove();
        }
        var url = $(this).attr('src');
        var srcTileImg = $('div[data-url="' + url + '"] img');
        $(srcTileImg).after(
            $('<img/>').attr(
                'src', '/static/img/sound-wave-icon.gif'
            ).addClass('play-active img-responsive')
        );
        $('body').animate({
            scrollTop: $(srcTileImg).offset().top
        }, 2000);
        if ($(this).attr('data-new') > 0) {
            $(this).attr('data-new', 0);
            $(this).bind('progress', progress);
        }
    });
    $('.player audio').on('pause', function(e) {
        $('img.play-active').remove();
    });
    var spinner = new Spinner({
        lines: 11,
        length: 23,
        width: 29,
        radius: 0,
        scale: 1,
        corners: 0.5,
        color: '#ECECEC',
        opacity: 0,
        rotate: 0,
        direction: 1,
        speed: 1,
        trail: 75,
        fps: 20,
        zIndex: 2e9,
        className: 'spinner',
        top: '50%',
        left: '50%',
        shadow: false,
        hwaccel: false,
        position: 'absolute'
    });
    $('.search-bar form button').click(function(event) {
        event.preventDefault();
        var itemContainer = $('.item-container');
        var query = $('.search-bar form input[name="query"]').val();
        if (query) {
            itemContainer.css({
                'min-height': ($(window).height() - $('.upper').outerHeight()) + 'px'
            }).empty();
            spinner.spin($('.lower')[0]);
            $.get('/search?query=' + query, function(data) {
                if (data.result.length > 0) {
                    data.result.forEach(function(item) {
                        var newResult = $('<div/>').addClass('col-xs-6 col-sm-4 col-md-2 item').append(
                            $('<div/>').addClass('row').append(
                                $('<div/>').addClass('col-xs-12').attr('data-url', item.url).attr(
                                    'data-start-time', item.start_time
                                ).append(
                                    $('<img/>').addClass('img-responsive').css({
                                        'display': 'inline-block'
                                    }).attr('src', item.image)
                                )
                            )
                        ).append(
                            $('<div/>').addClass('row').append(
                                $('<div/>').addClass('col-xs-12').append(
                                    $('<strong/>').html(item.title)
                                )
                            )
                        ).append(
                            $('<div/>').addClass('row').append(
                                $('<div/>').addClass('col-xs-12').append(
                                    $('<strong/>').html(item.name + " by " + item.author)
                                )
                            )
                        );
                        $(itemContainer).append(newResult.fadeIn('slow'));
                    });
                } else {
                    var noResult = $('<div/>').addClass('col-xs-10 col-xs-offset-1 text-center no-result').append(
                        $('<h2/>').html('No results were found for your search. Please try again.')
                    );
                    $(itemContainer).append(noResult.fadeIn('slow'));
                }
                spinner.stop();
            });
        } else {
            $('.search-bar form input[name="query"]').focus();
            setTimeout(function() {
                $('.search-bar form input[name="query"]').blur();
                setTimeout(function() {
                    $('.search-bar form input[name="query"]').focus();
                    setTimeout(function() {
                        $('.search-bar form input[name="query"]').blur();
                    }, 200);
                }, 200);
            }, 200);
        }
    });
});