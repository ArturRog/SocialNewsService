$( document ).ready(function() {

    var post_id;
    var comment_id;
    function set_post_id(element) { post_id = $(element).closest('.post-navigation').attr('id'); }
    function get_html_post_id() { return '#'+post_id; }
    function get_post_id() { return post_id.replace('p', ''); }
    function set_comment_id(element) { comment_id = $(element).closest('.comment').attr('id'); }
    function get_html_comment_id() { return '#'+comment_id; }
    function get_comment_id() { return comment_id.replace('c', ''); }

    $('#posts-container')
        .on('click', '.add-comment', function() {
            set_post_id(this);
            new_comment();
        })
        .on('click', '.show-comments', function() {
            set_post_id(this);
            set_comment_id(this);
            show_comments();
        })
        .on('click', '.add-sub-comment', function() {
            set_post_id(this);
            set_comment_id(this);
            new_sub_comment();
        })
        .on('click', '.show-sub-comments', function() {
            set_post_id(this);
            set_comment_id(this);
            show_sub_comments();
        })
        .on('click', '#add-comment-close-button', function () {
            var $element = $( '#add-comment-form ');
            $element.slideUp(function () {
                $element.empty();
            });
        });

    function show_comments() {
        var element_id = get_html_post_id();
        var url = '/comments/show-comments/'+get_post_id();
        var element_class = '.comments-container';
        var $loadElement = $( element_id ).children( element_class );
        load_comments( $loadElement, url);
    }

    function new_comment() {
        var url = '/comments/new_comment/'+get_post_id();
        var $element = $( '#add-comment-form' );
        $element.load( url, function () {
            $element.slideDown();
        } );
    }

    function new_sub_comment() {
        var url = '/comments/new_comment/'+get_post_id()+'/'+get_comment_id();
        var $element = $( '#add-comment-form' );
        $element.load( url, function () {
            $element.slideDown();
        } );
    }

    function show_sub_comments() {
        var element_id = get_html_comment_id();
        var url = '/comments/show-comments/'+get_post_id()+'/'+get_comment_id();
        var element_class = '.sub-comments-container';
        var $loadElement = $( element_id ).children( element_class );
        load_comments($loadElement, url);
    }

    function load_comments($loadElement, url) {
        if( $loadElement.is(':empty') ) {
            $loadElement.css( "display", "none" ) ;
            $loadElement.load(url, function () {
                 $loadElement.slideDown('slow');
            });
        } else {
            $loadElement.slideToggle('medium');
        }
    }

});