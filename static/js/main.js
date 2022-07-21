 $( function() {
    $( "#tabs" ).tabs({
      collapsible: true
    });
  } );

  $document.getElementById("toggleVisibilityButton").addEventListener("click", function(button) {
   if (document.getElementById("displaytable").style.display == "block")
    document.getElementById("displaytable").style.display = "none";
   else document.getElementById("displaytable").style.display = "none";
});
$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
        $(this).toggleClass('active');
    });
});