$(document).ready(function() {
    $(window).scroll(function () {

        var scroll = $(this).scrollTop();
        var dist = 1.3;

        //offsets
        var homeOff = $('.header').offset().top;
        var aboutOff = $('#about').offset().top;
        var portOff = $('#port').offset().top;
        var testOff = $('.testimonial-container').offset().top;
        var contactOff = $('#contact').offset().top;

        //animated classes
        //about section
        var skillItemContainer = $('.skill-item-container');
        var skillItemHeader = $('#skill-head');
        var aboutText = $('.about-text');
        var aboutText2 = $('#about2');

        //portfolio section
        var portfolioHeader = $('#work-head');
        var portfolioLink = $('#port-link-view');
        var portfolioItem1 = $('#port-1');
        var portfolioItem2 = $('#port-2');
        var portfolioItem3 = $('#port-3');

        //testimonial section
        var test = $('.testimonial');
        var testHeader = $('#test-head');

        //navlinks
        var homeLink = $('#home-link');
        var aboutLink = $('#about-link');
        var portLink = $('#port-link');
        var testLink = $('#test-link');
        var contactLink = $('#cont-link');




        if (scroll >= (homeOff / dist)) {
            homeLink.addClass('active');
            aboutLink.removeClass('active');
            portLink.addClass('active');
            testLink.removeClass('active');

        } else {
            homeLink.removeClass('active');
        }


        if (scroll >= (aboutOff / (dist + .2))) {
            homeLink.removeClass('active');
            aboutLink.addClass('active');

            aboutText.removeClass('my-none');
            aboutText.addClass('animated slideInLeft');



            if (window.innerWidth < 600) {
                skillItemContainer.removeClass('col-3');
                skillItemContainer.addClass('col');
            } else {
                skillItemContainer.addClass('col-3');
                skillItemContainer.removeClass('col');
            }


            setTimeout(function(){
                skillItemHeader.removeClass('my-none');
                //leave these as actual id names, no need to create variables for each one
                $('#skill1').removeClass('my-none');
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
                    aboutText2.removeClass('my-none');
                    aboutText2.addClass('animated zoomInLeft');
                    }, 1150);

            } else {
                setTimeout(function(){
                    aboutText2.removeClass('my-none');
                    aboutText2.addClass('animated slideInRight');
                    }, 1150);
            }

        } else {
            contactLink.removeClass('active')

        }

        if (scroll >= (portOff / (dist + 0.2 ))) {
            portfolioHeader.removeClass('my-none');
            portfolioLink.removeClass('my-none');
            portfolioItem1.removeClass('my-none');
            portfolioItem1.addClass('animated flipInY');

            portLink.addClass('active');
            aboutLink.removeClass('active');
            testLink.removeClass('active');

            setTimeout(function(){
                portfolioItem2.removeClass('my-none');
                portfolioItem2.addClass('animated flipInY');
                }, 250);


            setTimeout(function(){
                portfolioItem3.removeClass('my-none');
                portfolioItem3.addClass('animated flipInY');
                }, 500);

        } else {
            portLink.removeClass('active');

        }

        if (scroll >=(testOff / dist)) {
            test.removeClass('my-none');
            testHeader.removeClass('my-none');
            test.addClass('animated flipInX');
            testLink.addClass('active');
            portLink.removeClass('active');
            aboutLink.removeClass('active');

        } else {
            testLink.removeClass('active')

        }

        if (scroll >= (contactOff / dist)) {
            contactLink.addClass('active');
            portLink.removeClass('active');
            aboutLink.removeClass('active');
            testLink.removeClass('active');
        } else {
            contactLink.removeClass('active')


        }

    });
});