var id;
var opt_value = document.querySelectorAll(".opt_value");
var report_type = document.querySelectorAll("input[type='radio']");
document.querySelectorAll(".post-opt").forEach(opt=>opt.addEventListener("click", function(e) {
    id = e.target.getAttribute("data-opt");
    $(".option").fadeIn(300);
    document.body.style.overflow = "hidden";
    document.querySelector(".report").addEventListener("click", function() {
        $(".option").fadeOut(100);
        $(".report_form_container").fadeIn(300);
    }, {once: true});
    document.querySelector(".close_report").addEventListener("click", function() {
        report_type.forEach( label => label.checked = false);
        document.querySelector(".report_submit").disabled = true;
        $(".report_form_container").fadeOut(100);
        document.body.style.overflow = "";
    });
    document.querySelector(".post").addEventListener("click", function() {
        var uid = document.querySelector("span");
        var type = document.querySelector("#"+id+" .pic").getAttribute("data-type");
        location.href='/post/' + id + '?id=' + uid + '&type=' + type;
    });
}));
document.querySelector(".report_submit").addEventListener("click", function() {
    var report = document.querySelector("[name='report_type']:checked").value;
    $.ajax({
        method: "POST",
        data: {
            id: id,
            report: report,
        },
        url: "/report",
        success: function() {
            alert("report success");
            report_type.forEach( label => label.checked = false);
            document.querySelector(".report_submit").disabled = true;
            $(".report_form_container").fadeOut(100);
            document.body.style.overflow = "";
        },
    });
}, {once: true});
document.querySelector(".cancel").addEventListener("click", function() {
    $(".option").fadeOut(100);
    document.body.style.overflow = "";
});
opt_value.forEach(label => label.addEventListener("click", function() {
    document.querySelector(".report_submit").disabled = false;
}), {once: true});
