window.onload = function() {
    $(window).scroll(function () {

        var scroll = $(this).scrollTop();
        var dist = 1.3;

        var contactOff = $('#contact').offset().top;
        var contact = $('.contact_form');

        var aboutOff = $('#about').offset().top;
        var aboutText = $('.about-text');

        var portOff = $('#port').offset().top;

        var testOff = $('.testimonial-container').offset().top;
        var test = $('.testimonial');



        if (scroll >= (contactOff / dist)) {
            contact.removeClass('d-none');
            contact.addClass('animated jackInTheBox');
            $('#cont-link').addClass('active')
        }

        if (scroll >= (aboutOff / (dist + .2))) {
            aboutText.removeClass('d-none');
            aboutText.addClass('animated slideInLeft');

            setTimeout(function(){
                $('#skill1').removeClass('d-none');
                $('#skill-head').removeClass('d-none');
                $('#skill1').addClass('animated bounceIn');
                }, 250);
            setTimeout(function(){
                $('#skill2').removeClass('d-none');
                $('#skill2').addClass('animated bounceIn');
                }, 350);
            setTimeout(function(){
                $('#skill3').removeClass('d-none');
                $('#skill3').addClass('animated bounceIn');
                }, 450);
            setTimeout(function(){
                $('#skill4').removeClass('d-none');
                $('#skill4').addClass('animated bounceIn');
                }, 550);
            setTimeout(function(){
                $('#skill5').removeClass('d-none');
                $('#skill5').addClass('animated bounceIn');
                }, 650);
            setTimeout(function(){
                $('#skill6').removeClass('d-none');
                $('#skill6').addClass('animated bounceIn');
                }, 750);
            setTimeout(function(){
                $('#skill7').removeClass('d-none');
                $('#skill7').addClass('animated bounceIn');
                }, 850);
            setTimeout(function(){
                $('#skill8').removeClass('d-none');
                $('#skill8').addClass('animated bounceIn');
                }, 950);
            setTimeout(function(){
                $('#about2').removeClass('d-none');
                $('#about2').addClass('animated slideInRight');
                }, 1050);
        }

        if (scroll >=(testOff / dist)) {
            test.removeClass('my-none');
            $('#test-head').removeClass('d-none');
            test.addClass('animated flipInX');

        }

        if (scroll >= (portOff / (dist + 0.2 ))) {
            $('#work-head').removeClass('d-none');
            $('#port-1').removeClass('d-none');
            $('#port-1').addClass('animated flipInY');

            setTimeout(function(){
                $('#port-2').removeClass('d-none');
                $('#port-2').addClass('animated flipInY');
                }, 250);


            setTimeout(function(){
                $('#port-3').removeClass('d-none');
                $('#port-3').addClass('animated flipInY');
                }, 500);

        }
    });
};
