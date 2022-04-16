
// Only load hero videos if the browser width is greater than 800 pixels wide
// If its a small device, copy the poster-data value into the video element
// to reduce the flickering that occurs when things happen.
$(document).ready(function() {
    let screenWidth = $(window).width();
    let vid = $('#video-hero');
    if(vid && screenWidth > 800) {
        vid[0].play();
        vid.attr('poster', vid.attr('poster-data'));
    } else {
        vid.attr('poster', vid.attr('poster-data-small'));
    }
});
