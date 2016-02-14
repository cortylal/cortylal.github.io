$( function() {

  var $container = $('#container').isotope({
    itemSelector: '.item',
    layoutMode: 'fitRows'
  }).isotope('shuffle');

  // filter with selects and checkboxes
  var $checkboxes = $('#form-ui input');
  
  $checkboxes.change( function() {
    // map input values to an array
    var inclusives = [];
    // inclusive filters from checkboxes
    $checkboxes.each( function( i, elem ) {
      // if checkbox, use value if checked
      if ( elem.checked ) {
        inclusives.push( elem.value );
      }
    });

    // combine inclusive filters
    var filterValue = concatValues(inclusives);
    $container.isotope({ filter: filterValue })
  });

});

// flatten object by concatting values
function concatValues( obj ) {
  var value = '';
  for ( var prop in obj ) {
    value += obj[ prop ];
  }
  return value;
};

$(".btn").change(function(){
    if ($('.btn:checked').length == $('.btn').length) {
       //do something
       setTimeout(function(){
        /*alert('they are all checked');*/
        $('#bring-popup').trigger('click');
      },700);
    }
});

// Popup Window
var scrollTop = '';
var newHeight = '300';
 
$(window).bind('scroll', function() {
  scrollTop = $( window ).scrollTop();
  newHeight = scrollTop + 100;
});
    
$('.popup-trigger').click(function(e) {
  e.stopPropagation();
  if(jQuery(window).width() < 767) {
    $(this).after( $( ".popup" ) );
    $('.popup').show().addClass('popup-mobile').css('top', 0);
    $('html, body').animate({
      scrollTop: $('.popup').offset().top
    }, 500);   
  } else {
    $('.popup').removeClass('popup-mobile').css('top', newHeight).toggle();
  };
});
    
$('html').click(function() {
  $('.popup').hide();
});
 
$('.popup-btn-close').click(function(e){
  $('.popup').hide();
});
 
$('.popup').click(function(e){
  e.stopPropagation();
});

