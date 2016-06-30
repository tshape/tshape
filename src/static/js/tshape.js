$(document).ready(function() {
    console.log("Tshape");

    var tshapeMiddle = null;
    var skillNodeList = $('#tshape .tshape__middle').children();
    var tshapeLength = $('#tshape .tshape__middle').children().length;
    var tshapeWidth = tshapeLength * 40 + "px";
    var timer = 100;

    (function getMiddleSkillset(){
        skillNodeList.each(function(index, element) {
            if (($(this)).hasClass('tshape__skillset--middle')) {
                tshapeMiddle = index;
            }
        });
        console.log(tshapeMiddle);
    })();

    var alignTshape = function() {
        skillNodeList.each(function(index, element) {
            var bottomRange = tshapeMiddle - 4;
            var topRange = tshapeMiddle + 4;
            $(this).hide();
            if (index >= bottomRange  && index <= topRange) {
                $(element).fadeIn(timer);
                timer += 100;
            } else {
                $(element).fadeOut();
            }
        });
        $('#tshape').css('width', '400px')
    };


    $('#show-all-skillsets').on('click',function() {
        $('#tshape .tshape__middle').children().fadeIn();
        $('#tshape').css('width', tshapeWidth)
    });

    $('#show-core-skillsets').on('click',function() {
        timer = 100;
        alignTshape();
    });

    alignTshape();

});
