$(document).ready(function(){
    $('.banner-slider').slick({
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        draggable: true,
        swipe: true,
        arrows: false,
        autoplay: true,
        autoplaySpeed: 10000,
        touchThreshold: 10
    });

    $('#prev').click(function(){
        $('.banner-slider').slick('slickPrev');
    });

    $('#next').click(function(){
        $('.banner-slider').slick('slickNext');
    });
});