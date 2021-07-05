var slideIndex = 1;

function vidpause() {
    var vid = document.getElementsByTagName("video");
    for (z=0; z<vid.length; z++) {
        vid[z].pause();
    }
}


document.querySelectorAll(".slide")[0].style.display = "block";
document.querySelector(".next").addEventListener("click", function() {
    var n = 1;
    showSlides(slideIndex += n);
    vidpause();
});

document.querySelector(".prev").addEventListener("click", function() {
    var n = -1;
    showSlides(slideIndex += n);
    vidpause();
});

function showSlides(n) {
  var slides = document.querySelectorAll(".slide");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";
}
