a = document.querySelector("span").innerHTML;
document.querySelectorAll(".user_like_list").forEach( ulike => ulike.addEventListener("click", function(e) {
    $(".user_like_container").fadeIn(100);
    document.body.style.overflow = "hidden";
    $.ajax({
        method: "GET",
        url: "/relatelist?react=like&cid=" +e.target.getAttribute("data-post-id") ,
        success: function(res) {
            var data = "<div>"
            $.each(res, function(index, value) {
                user = "<div class='user'>";
                if ( value[0] != "" ) { user += "<img class='user-circle' src='" + value[0] + "'/>" }
                else { user += "<img class='user-circle' src='static/img/default-user.png'/>" }
                user += "<span class='user_name'>  " + value[1] + "</span>"
                if ( value[2] != a ) {
                    if ( value[2] == value[3] ) {
                        user += "<button class='following' type='button'>Unfollow</button>"
                    }
                    else {
                        user += "<button class='follow' type='button'>Follow</button>"
                    }
                }
                user += "</div>"
                data += user;
            });
            data += "</div>"
            $(".list").html(data);
        }
    });
}));
document.querySelectorAll(".user_comment_list").forEach( ucl => ucl.addEventListener("click", function(e) {
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
                if ( value[2] != a ) {
                    if ( value[2] == value[3] ) {
                        user += "<button class='following' type='button'>Unfollow</button>"
                    }
                    else {
                        user += "<button class='follow' type='button'>Follow</button>"
                    }
                }
                user += "</div>"
                data += user;
            });
            data += "</div>"
            $(".list").html(data);
        }
    });
}));
document.querySelectorAll(".user_share_list").forEach( sharelist => sharelist.addEventListener("click", function(e) {
    $(".user_share_container").fadeIn(100);
    document.body.style.overflow = "hidden";
    $.ajax({
        method: "GET",
        url: "/relatelist?react=share&cid=" +e.target.getAttribute("data-post-id") ,
        success: function(res) {
            var data = "<div>"
            $.each(res, function(index, value) {
                user = "<div class='user'>";
                if ( value[0] != "" ) { user += "<img class='user-circle' src='" + value[0] + "'/>" }
                else { user += "<img class='user-circle' src='static/img/default-user.png'/>" }
                user += "<span class='user_name'>  " + value[1] + "</span>"
                if ( value[2] != a ) {
                    if ( value[2] == value[3] ) {
                        user += "<button class='following' type='button'>Unfollow</button>"
                    }
                    else {
                        user += "<button class='follow' type='button'>Follow</button>"
                    }
                }
                user += "</div>"
                data += user;
            });
            data += "</div>"
            $(".list").html(data);
        }
    });
}));
document.querySelectorAll(".close").forEach( close => close.addEventListener("click", function() {
    $(".user_like_container, .user_comment_container, .user_share_container").fadeOut(100);
    document.body.style.overflow = "";
    document.querySelectorAll(".list div").remove();
}));
