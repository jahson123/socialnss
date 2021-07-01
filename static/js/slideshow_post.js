var slideIndex = 1;
document.querySelectorAll(".slide")[0].style.display = "block";
document.querySelector(".next").addEventListener("click", function() {
    var n = 1;
    showSlides(slideIndex += n);
});

document.querySelector(".prev").addEventListener("click", function() {
    var n = -1;
    showSlides(slideIndex += n);
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