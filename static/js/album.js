var container = document.querySelectorAll(".slide_container");
var next = document.querySelectorAll(".next");
var prev = document.querySelectorAll(".prev");
var slideIndex = new Array(container.length);
for ( i=0; i<slideIndex.length; i++ ) { slideIndex[i] = 1 }
for ( i=0; i<container.length; i++ ) {
    next[i].setAttribute("data-slide-next", i);
    prev[i].setAttribute("data-slide-next", i);
    showSlides(slideIndex[i], i);
}

function vidpause() {
    var vid = document.getElementsByTagName("video");
    for (z=0; z<vid.length; z++) {
        vid[z].pause();
    }
}


document.querySelectorAll(".next").forEach( next => next.addEventListener("click", function(e) {
        var a = e.target.getAttribute("data-slide-next");
        plusSlides(1, a);
        vidpause();
    })
);

document.querySelectorAll(".prev").forEach( prev => prev.addEventListener("click", function(e) {
        var a = e.target.getAttribute("data-slide-next");
        plusSlides(-1, a);
        vidpause();
    })
);

function plusSlides(n, num) { showSlides(slideIndex[num] += n, num); }

function showSlides(n, no) {
    var i;
    var num_slides = document.getElementsByClassName("num-slides");
    var slides = container[no].querySelectorAll(".slide");
    if (n > slides.length) {slideIndex[no] = 1}
    if (n < 1) {slideIndex[no] = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    num_slides[no].innerHTML = slideIndex[no] + "/" + slides.length
    slides[slideIndex[no]-1].style.display = "block";
}
