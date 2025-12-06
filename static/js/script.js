document.addEventListener("DOMContentLoaded", () => {
    const flash = document.querySelector('.flash');
    if (flash) {
      setTimeout(() => {
        flash.classList.add('hide');
        setTimeout(() => flash.remove(), 800);
      }, 4000);
    }
  });


  