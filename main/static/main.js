$(document).ready(function() {

// setup socket connection
namespace = '/main';
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

var sortingOnlineBy = 0;
var sortingOfflineBy = 0;

// connect
socket.on('connect', function(){
    socket.emit('getTable');
});


// Update Main Now Playing playlist
socket.on('table', function(msg) {
    $('#online_table tr:gt(0)').remove();
    $('#offline_table tr:gt(0)').remove();

    $.each(msg, function(index, item) {
        if(item.online == 1){
            $('<tr>').html("<td>" + item.name + "</td><td>" + item.ip + "</td><td>" + index + "</td><td>" + genTime(item.upTime) + "</td><td>" + 
                "<button id='setName1' class='btn btn-sm btn-success'><span class='glyphicon glyphicon-option-horizontal'></span></button>" +
                "</td>").appendTo('#online_table');
        }
        else{
            $('<tr>').html("<td>" + item.name + "</td><td>" + item.ip + "</td><td>" + index + "</td><td>" + item.last + "</td><td>" + genTime(item.upTime) + "</td><td>" +
                "<button id='setName2' class='btn btn-sm btn-success'><span class='glyphicon glyphicon-option-horizontal'></span></button>" +
                "</td>").appendTo('#offline_table');
        }
    });
    sortTable(sortingOnlineBy, 'online_table');
    sortTable(sortingOfflineBy, 'offline_table');
});


$('#online_table').on('click', '#setName1', function() {
    var index = $(this).closest('tr').index();
    var val = $('table#online_table tr:eq(' + index + ') td:eq(' + 2 + ')').text();

    var userinput = window.prompt("Enter New Name For the device", "");

    if (userinput == null || userinput == ""){
        return false;
    }
    else {
        socket.emit('addUser', {'mac' : val, 'name' : userinput});
        return false;
    }
});

$('#offline_table').on('click', '#setName2', function() {
    var index = $(this).closest('tr').index();
    var val = $('table#offline_table tr:eq(' + index + ') td:eq(' + 2 + ')').text();

    var userinput = window.prompt("Enter New Name For the device", "");

    if (userinput == null || userinput == ""){
        return false;
    }
    else {
        socket.emit('addUser', {'mac' : val, 'name' : userinput});
        return false;
    }
});

});


function genTime(time){
    var h = Math.floor((time / 3600) % 24);
    var d = Math.floor(time / (3600*24));
    var m = Math.floor(time % 3600 / 60);

    var days = String(d) + ':';
    var hours = h > 9 ? String(h) + ':' :  '0' + String(h) + ':';
    var minutes = m > 9 ? String(m) : "0" + String(m);
    return (days + hours + minutes) ;
}


function sortTable(n, tableID) {
    if (tableID == 'online_table'){
        sortingOnlineBy = n;
    }
    else if (tableID == 'offline_table'){
        sortingOfflineBy = n;
    }
    
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById(tableID);
    switching = true;

    while (switching) {
        switching = false;

        rows = table.getElementsByTagName("TR");

        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;

            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];

            if (n == 1){
                var xip = x.innerHTML.toLowerCase().split(".");
                var yip = y.innerHTML.toLowerCase().split(".");

                if(parseInt(xip[0]) != parseInt(yip[0])){
                    if (parseInt(xip[0]) > parseInt(yip[0])){
                        shouldSwitch= true;
                        break;
                    }
                }
                else if (parseInt(xip[1]) != parseInt(yip[1])){
                    if (parseInt(xip[1]) > parseInt(yip[1])){
                        shouldSwitch= true;
                        break;
                    }
                }
                else if (parseInt(xip[2]) != parseInt(yip[2])){
                    if (parseInt(xip[2]) > parseInt(yip[2])){
                        shouldSwitch= true;
                        break;
                    }
                }
                else {
                    if (parseInt(xip[3]) > parseInt(yip[3])){
                        shouldSwitch= true;
                        break;
                    }
                }
            }
            else {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch= true;
                    break;
                }
            }
    
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}