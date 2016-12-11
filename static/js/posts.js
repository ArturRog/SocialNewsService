$( document ).ready(function() {

    var post_id;
    var comment_id;

    function set_post_id(element) {
        post_id = $(element).closest('.comments').attr('id');
    }
    function get_html_post_id() {
        return "#"+post_id;
    }
    function get_post_id() {
        return post_id;
    }

    function set_comment_id(element) {
        comment_id = $(element).parent('.comment').attr('id');
    }
    function get_html_comment_id() {
        return "#"+comment_id;
    }
    function get_comment_id() {
        return comment_id;
    }

    $('.comments')
        .on('click', '.add-comment', function() {
            set_post_id(this);
            add_comment();
        })
        .on('click', '.show-comments', function() {
            set_post_id(this);
            show_comments();
        })
        .on('click', '.show-sub-comments', function() {
            set_post_id(this);
            set_comment_id(this);
            show_sub_comments();
        });

    function show_comments() {
        var element_id = get_html_post_id();
        var url = '/home/show-comments/'+get_post_id();
        var element_class = '.comments-container';
        $( element_id ).children( element_class ).load( url );
    }

    function add_comment() {

    }

    function show_sub_comments() {
        var element_id = get_html_comment_id();
        var url = '/home/show-comments/'+get_post_id()+'/'+get_comment_id();
        alert(url);
        var element_class = '.sub-comments-container';
        $( element_id ).children( element_class ).load( url );
    }

});

//