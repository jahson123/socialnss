
    $(document).ready(function(){
        var x = document.getElementById("content");
        if ( $(".search").val() == "" ) {
              x.style.display = "none";
          }
        $(".search").on("input", function(e) {
            $(x).show();
            $.ajax({
                method: "POST",
                url: "/data",
                data: {text:$(".search").val()},
                success: function(res) {
                    var data = "<div class='list-group'>";
                    $.each(res, function(index, value) {
                        data += "<a href='/" + value[1] + "' style='text-decoration: none; color: black;' class='list-group-item list-group-item-action'>" + value[0] + "</a>";
                    });
                    data += "</div>";
                    $("#search_list").html(data);
                    }
                });
            if ( $(".search").val() == "" ) {
                x.style.display = "none";
            }
        });
        $(window).click(function() {
            $(x).hide();
        });
    });
