(function () {
    "use strict";

    $.fn.extend({
        animateCss: function (animationName) {
            var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
            this.addClass('animated ' + animationName).one(animationEnd, function() {
                $(this).removeClass('animated ' + animationName);
            });
        }
    });

    AOS.init();

    $('.selectable').each(function () {
        var select = $(this);

        if (select.data('selectable-no-search')) {
            var theme = select.data('theme');
            select.select2({
                minimumResultsForSearch: -1
            });
        } else {
            select.select2();
        }
    });

    $('#testimonials-default-carousel').owlCarousel({
        loop: true,
        margin: 10,
        center: true,
        items: 1,
        autoplay: true,
        autoplayHoverPause: true,
        dots: true,
        navigation: true
    });

    $('#partners-default-carousel').owlCarousel({
        loop: true,
        margin: 15,
        items: 5,
        autoplay: true,
        autoplayHoverPause: true,
        responsiveClass:true,
        responsive : {
            0 : {
                items: 1
            },
            480 : {
                items: 2
            },
            800: {
                items: 3
            },
            1200: {
                items: 5
            }
        }
    });

    if ($('#page-contact-map').length) {
        var contactDefault = L.map('page-contact-map').setView([51.505, -0.09], 13);
         L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
         }).addTo(contactDefault);
        contactDefault.scrollWheelZoom.disable();
    }
})(jQuery);