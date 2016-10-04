$(document).ready(function() {
    $('.slider').slick({
        centerMode: true,
        centerPadding: '60px',
        slidesToShow: 3,
        dots: true
    });
    $('body.page-profile-skillsets').on('click', '#add-skillset-javascript', function(e) {
        e.preventDefault();
        $('.skillsets--added li').remove();
        $('.skillsets--added').prepend("<li><a href='/profile/skillsets/javascript/' class='badge active'>Javascript</a></li>")
    })
    $('#show-tshape').on('click', function(e) {
        e.preventDefault();
        $('#preview').toggleClass('open');
    })
});
