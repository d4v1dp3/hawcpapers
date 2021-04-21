
$(function() {

  $('#modal_author_list').on('shown.bs.modal', function (event) {
    var id_paper = $(event.relatedTarget).data('paper');

    $("#paper_modal_list").empty();

    $.getJSON('/signed/' + id_paper + '/', function (data) {
      data.users.forEach(function (item, index) {
        $("#paper_modal_list").append(
            $('<tr>').append($('<td>').text(item.name))
                .append($('<td>').text(item.date))
                .append($('<td>').text(item.status))
        );
      });

    });
  });

});

function publication(status){
  switch (status) {
    case 'A':
      return "Signed"
    case 'B':
      return "Reject"
  }
}