video = ['mp4', 'mov', 'avi', 'webm'];
img = ['gif','png','jpg','jpeg'];
var result = "" ;
var a,b;

document.getElementById("file").addEventListener("change", function(e) {
    var files = e.target.files;
    var view = document.getElementById("view");
    a = b = result = "";
    if (files.length <= 6 ) {
        for (j=0; j<files.length; j++) {
            type = files[j].name.split(".")
            if (Number(files[j].size/1024/1024) > Number(30)) {
                var a = files[j].name;
                result = true;
            }
            else if (type[type.length-1] == "mp3" || type[type.length-1] == "pptx") {
                var b = files[j].name;
                result = true;
            }
        }
        if ( result == "" ) {
            for ( i=0; i<files.length; i++) {
                var reader = new FileReader();
                var file = files[i];
                type = file.name.split(".");
                if (img.includes(type[type.length-1])) {
                    reader.addEventListener("load", function(e) {
                        var data = e.target;
                        var img = document.createElement("img");
                        img.classList.add("image");
                        img.src= data.result;
                        view.insertBefore(img, null);
                    });
               }
               else if (video.includes(type[type.length-1])) {
                    reader.addEventListener("load", function(e) {
                        var data = e.target;
                        var vid = document.createElement("video");
                        vid.classList.add("video");
                        vid.src= data.result;
                        view.insertBefore(vid, null);
                    });
               }
               reader.readAsDataURL(file);
            }
            document.querySelector("#view").style.display = "inline";
            document.getElementsByClassName("upload_file")[0].style.display = "none";
            document.querySelector("input[type='submit']").disabled = false;
            document.querySelector(".err_message").style.display = "none";
        }
        else if ( result == true ) {
            if ( a != "" ) { alert("You cannot upload ''" + a + "'' that is more than 30mb."); }
            else if ( b != "" ) { alert("You cannot upload ''" + b  + "'' that is not image or video."); }
            document.querySelector("input[type='file']").value = "";
            document.querySelector("#view").style.display = "none";
        }
    }
    else {
        document.querySelector(".err_message").style.display = "inline";
    }
});

document.querySelector("#close").addEventListener("click", function() {
    var img = document.querySelectorAll(".image");
    var video = document.querySelectorAll(".video");
    for (i=0; i<img.length; i++) { img[i].remove(); }
    for (j=0; j<video.length; j++) { video[j].remove(); }
    document.querySelector("input[type='file']").value = "";
    document.querySelector("#view").style.display = "none";
    document.getElementsByClassName("upload_file")[0].style.display = "";
    document.querySelector("input[type='submit']").disabled = true;
});
