  const swiper = new Swiper('.swiper', {
        slidesPerView: 1,
        spaceBetween: 10,
        loop: true,

        autoplay: {
        delay: 2000,
        disableOnInteraction: false,
        },
        pagination: {
          el: '.swiper-pagination',
           clickable: true
        },
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev',
        },
         breakpoints: {
             640: {
              slidesPerView: 2,
             spaceBetween: 20,
        },
      992:{
           slidesPerView: 3,
          spaceBetween: 20,
        }
  }
});
