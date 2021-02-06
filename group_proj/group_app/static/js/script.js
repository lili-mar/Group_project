$(document).ready(function(){
    $("#SearchBox").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#myTable thead tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });