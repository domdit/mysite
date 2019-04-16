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

        var homeOff= $('.header').offset().top;

        if (scroll >= (homeOff / dist)) {
            $('#home-link').addClass('active');
            $('#port-link').addClass('active');
            $('#about-link').removeClass('active');
            $('#test-link').removeClass('active');

        } else {
            $('#home-link').removeClass('active');


        }


        if (scroll >= (aboutOff / (dist + .2))) {
            aboutText.removeClass('my-none');
            aboutText.addClass('animated slideInLeft');

            $('#about-link').addClass('active');
            $('#home-link').removeClass('active');

            if (window.innerWidth < 600) {
                $('.skill-item-container').removeClass('col-3');
                $('.skill-item-container').addClass('col');
            } else {
                $('.skill-item-container').addClass('col-3');
                $('.skill-item-container').removeClass('col');
            }


            setTimeout(function(){
                $('#skill1').removeClass('my-none');
                $('#skill-head').removeClass('my-none');
                $('#skill1').addClass('animated bounceIn');
                }, 250);
            setTimeout(function(){
                $('#skill2').removeClass('my-none');
                $('#skill2').addClass('animated bounceIn');
                }, 350);
            setTimeout(function(){
                $('#skill3').removeClass('my-none');
                $('#skill3').addClass('animated bounceIn');
                }, 450);
            setTimeout(function(){
                $('#skill4').removeClass('my-none');
                $('#skill4').addClass('animated bounceIn');
                }, 550);
            setTimeout(function(){
                $('#skill5').removeClass('my-none');
                $('#skill5').addClass('animated bounceIn');
                }, 650);
            setTimeout(function(){
                $('#skill6').removeClass('my-none');
                $('#skill6').addClass('animated bounceIn');
                }, 750);
            setTimeout(function(){
                $('#skill7').removeClass('my-none');
                $('#skill7').addClass('animated bounceIn');
                }, 850);
            setTimeout(function(){
                $('#skill8').removeClass('my-none');
                $('#skill8').addClass('animated bounceIn');
                }, 950);
            setTimeout(function(){
                $('#skill9').removeClass('my-none');
                $('#skill9').addClass('animated bounceIn');
                }, 1050);

            if (window.innerWidth < 600) {
                setTimeout(function(){
                    $('#about2').removeClass('my-none');
                    $('#about2').addClass('animated zoomInLeft');
                    }, 1150);

            } else {
                setTimeout(function(){
                    $('#about2').removeClass('my-none');
                    $('#about2').addClass('animated slideInRight');
                    }, 1150);

            }


        } else {
            $('#cont-link').removeClass('active')

        }

        if (scroll >= (portOff / (dist + 0.2 ))) {
            $('#work-head').removeClass('my-none');
            $('#port-1').removeClass('my-none');
            $('#port-1').addClass('animated flipInY');

            $('#port-link').addClass('active');
            $('#about-link').removeClass('active');
            $('#test-link').removeClass('active');



            setTimeout(function(){
                $('#port-2').removeClass('my-none');
                $('#port-2').addClass('animated flipInY');
                }, 250);


            setTimeout(function(){
                $('#port-3').removeClass('my-none');
                $('#port-3').addClass('animated flipInY');
                }, 500);

        } else {
            $('#port-link').removeClass('active');

        }

        if (scroll >=(testOff / dist)) {
            test.removeClass('my-none');
            $('#test-head').removeClass('my-none');
            test.addClass('animated flipInX');
            $('#test-link').addClass('active');
            $('#port-link').removeClass('active');
            $('#about-link').removeClass('active');

        } else {
            $('#test-link').removeClass('active')

        }

        if (scroll >= (contactOff / dist)) {
            $('#cont-link').addClass('active');
            $('#port-link').removeClass('active');
            $('#about-link').removeClass('active');
            $('#test-link').removeClass('active');
        } else {
            $('#cont-link').removeClass('active')


        }

    });
};
