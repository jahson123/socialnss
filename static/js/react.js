document.querySelector(".user_like_list").addEventListener("click", function(e) {
    $(".user_like_container").fadeIn(100);
    console.log(e.target.getAttribute("data-post-id"));
    document.body.style.overflow = "hidden";
    $.ajax({
        method: "GET",
        url: "/relatelist?react=like&cid=" +e.target.getAttribute("data-post-id") ,
        success: function(res) {
            var data = "<div>"
            $.each(res, function(index, value) {
                user = "<div class='user'>";
                user += "<a href='/admin_view_profile/" + value[2] + "'>"
                if ( value[0] != "" ) { user += "<img class='user-circle' src='" + value[0] + "'/>" }
                else { user += "<img class='user-circle' src='static/img/default-user.png'/>" }
                user += "<span class='user_name'>  " + value[1] + "</span>"
                user += "</a></div>"
                data += user;
            });
            data += "</div>"
            $(".list").html(data);
        }
    });
});
document.querySelector(".user_comment_list").addEventListener("click", function(e) {
    $(".user_comment_container").fadeIn(100);
    document.body.style.overflow = "hidden";
    $.ajax({
        method: "GET",
        url: "/relatelist?react=comment&cid=" +e.target.getAttribute("data-post-id") ,
        success: function(res) {
            var data = "<div>"
            $.each(res, function(index, value) {
                user = "<div class='user'>";
                if ( value[0] != "" ) { user += "<img class='user-circle' src='" + value[0] + "'/>" }
                else { user += "<img class='user-circle' src='static/img/default-user.png'/>" }
                user += "<span class='user_name'>  " + value[1] + "</span>"
                user += "</div>"
                data += user;
            });
            data += "</div>"
            $(".list").html(data);
        }
    });
});
document.querySelector(".user_share_list").addEventListener("click", function(e) {
    $(".user_share_container").fadeIn(100);
    document.body.style.overflow = "hidden";
    $.ajax({
        method: "GET",
        url: "/relatelist?react=share&cid=" +e.target.getAttribute("data-post-id") ,
        success: function(res) {
            var data = "<div>"
            $.each(res, function(index, value) {
                user = "<div class='user'>";
                user += "<a href='/admin_view_profile/" + value[2] + "'>"
                if ( value[0] != "" ) { user += "<img class='user-circle' src='" + value[0] + "'/>" }
                else { user += "<img class='user-circle' src='{{ url_for('static', filename='img/default-user.png') }}'/>" }
                user += "<span class='user_name'>  " + value[1] + "</span>"
                user += "</a></div>"
                data += user;
            });
            data += "</div>"
            $(".list").html(data);
        }
    });
});
document.querySelectorAll(".close").forEach( close => close.addEventListener("click", function() {
    $(".user_like_container, .user_comment_container, .user_share_container").fadeOut(100);
    document.body.style.overflow = "";
    document.querySelectorAll(".list div").remove();
}));
