$( document ).ready(function() {

    var post_id;
    var comment_id;

    function set_post_id(element) {
        post_id = $(element).closest('div').attr('id');
        alert("Post id: "+post_id);
    }

    $('.add-comment').click(function() {
        set_post_id(this);
    });

    $('.show-comments').click(function() {
        set_post_id(this);
    });
});

//