const sidebarBox = document.querySelector('#box'),
sidebarBtn = document.querySelector('#btn'),
btn_icon = document.querySelector('.fas.fa-users'),
pageWrapper = document.querySelector('#page-wrapper');

sidebarBtn.addEventListener('click', event => {
  sidebarBtn.classList.toggle('active');
  btn_icon.classList.remove("fa-users");
  /*.addClass("fas fa-globe-americas");*/
  sidebarBox.classList.toggle('active');
});

pageWrapper.addEventListener('click', event => {

  if (sidebarBox.classList.contains('active')) {
    sidebarBtn.classList.remove('active');
    sidebarBox.classList.remove('active');
  }
});

window.addEventListener('keydown', event => {

  if (sidebarBox.classList.contains('active') && event.keyCode === 27) {
    sidebarBtn.classList.remove('active');
    sidebarBox.classList.remove('active');
  }
});