(function () {
    "use strict";

    $('.selectable').each(function () {
        var select = $(this);

        if (select.data('selectable-no-search')) {
            select.select2({
                minimumResultsForSearch: -1
            });
        } else {
            select.select2();
        }
    });

    var map = L.map('master-post-application-map').setView([51.505, -0.09], 13);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    map.scrollWheelZoom.disable();
})(jQuery);