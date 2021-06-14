/*!
    * Start Bootstrap - Creative v6.0.4 (https://startbootstrap.com/theme/creative)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-creative/blob/master/LICENSE)
    */
    (function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 72)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 75
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-scrolled");
    } else {
      $("#mainNav").removeClass("navbar-scrolled");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Magnific popup calls
  $('#portfolio').magnificPopup({
    delegate: 'a',
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    mainClass: 'mfp-img-mobile',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0, 1]
    },
    image: {
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
    }
  });

})(jQuery); // End of use strict


/* fade in/out picture of Mihamm from https://stackoverflow.com/questions/48202389/fade-image-on-scrolling
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js">
  <script type="js/scripts.js">
    $(function (){
    var element = $('.mihamm');
    $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
    element.fadeIn();
  }

    else {
    element.fadeOut();
  }
  });
  });
  </script>
  <img th:src="@{/img/bc.jpg}" className="mihamm"/> */


function callModal(type) {
  $('#exampleModal').modal('show');
  var modal = $('#exampleModal');
  modal.find('.modal-title').text(type);
  var content;
  switch (type) {
    case "Mitmachen":
      content="Komm in eine unserer Gruppen (von Evangelisationsaktionen über Anspiel, Deko und Verpflegung, creative communications und Gebet und Seelsorge ist alles dabei!), " +
          "lerne neue Leute kennen und staune, wie sehr Gott dich in seinem Team will! " +
          "Du hast eine coole Idee für eine spontane Aktion in der Woche? Melde dich super gerne bei uns - deine Ideen können ganz viel Freude schenken, zum Nachdenken anregen und Großes bewirken!<br><br> " +
          "Nähere Infos findest du in diesem <a href='https://docs.google.com/spreadsheets/d/1YVP8OHQj3Si_5n6vt_YnAH2GnRiqlWTv15FCpt8We-U/edit#gid=0'>Spreadsheet</a>.";
      break;
    case "Watchparty":
      content="Du hast keine Lust, die abendlichen Livestreams alleine zu schauen? Du möchtest neue Leute kennenlernen? Dann stell deine WG zur Verfügung und starte eine Watchparty!" +
          "<!--<div style='display: flex; justify-content: center'><button class='btn btn-primary m-3' onclick=\"window.open('registration/new_watchparty')\">Watchparty starten</button></div>-->";
      break;
    case "Beten":
      content="Bei der Vorbereitung der Hochschultage wollen wir Gott aktiv mit einbeziehen und vertrauen darauf, dass unser Gebet Kraft hat, Veränderung bringt und die Hochschultage zum Strahlen bringt! <br>" +
          "Trag dich gerne fürs 24/7 Gebet während der Hochschultage in <a href='https://docs.google.com/spreadsheets/d/1skfjLmYJfClFqls8EgVtL6Cu5sfhe1QRXz3Zw5dzvFE/edit?usp=sharing'>diese Tabelle</a> ein.";
      break;
    case "Finanzieren":
      content="Falls du uns gerne auch finanziell bei der Bezahlung von Honoraren, Flyern, Technik & Material unterstützen willst, freuen wir uns sehr über eine Spende an <br><br>" +
          "<strong> Initiative Gemeinde und Gebetshaus e.V. Heidelberg </strong><br>" +
          "IBAN: DE56 6725 0020 0009 3020 77, <br>" +
          "BIC: SOLADES1HDB, <br>" +
          "Verwendungszweck: ConnAction";
      break;
  }
  modal.find('.modal-body').html(content);
}






