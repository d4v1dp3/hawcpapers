
var url_csv = "/static/csv/hawc-personnel.csv";

var objAuthor = [];

$(document).ready(function() {
    //$.ajax({
    //    type: "get",
    //    url: url_csv,
    //    dataType : "text",
    //    success: function (data){
    //        objAuthor = $.csv.toObjects(data);
    //        loadData(objAuthor);
    //    },
    //});
});

function loadData(data){
    console.log(data);
    data.forEach(function(item,index){
        $("#author-list").find('tbody').append(
            $('<tr>').append($('<td>').text(item.givenName + " " + item.surName))
                .append($('<td>').text(item.institution))
                .append($('<td>').text(item.email))
                .append($('<td>').text(item.country))
        )
    });
}