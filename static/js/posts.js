var post_id;
var comment_id;

$( document ).ready(function() {

    function set_post_id(element) {
        post_id = $(element).closest('div').attr('id');
        alert("Post id: "+post_id);
    }

    $('.add_comment').click(function (event) {
        set_post_id(this);
    });

    $('.show_comments').click(function (event) {
        set_post_id(this);
    });
});

//