/*function set_openid(openid, id) {
    u = openid.search('<username>');
    if (u != -1) {
        // openid requires username
            user = prompt('Enter your ' + pr + ' username:');
            openid = openid.substr(0, u) + user;
        }
        form = document.forms['login'];
        form.elements['openid'].value = openid;
}*/

function change_class(old_tag, new_tag) {
    $(old_tag).attr('class', new_tag);
}
function set_data(tag, data) {
    console.log(" ==== tag: " + tag + " data: " + data.jobkey);
    $(tag).attr('id', data.jobkey);
    console.log(" now id name is: " + $(tag).attr('id'));
    $(tag).data(data);
    console.log(" saved data: " + JSON.stringify($(tag).data()) );
}

$(document).ready(function() {
    $("button").click(function(event) {
        //alert(event.target.id);
        var id = $(this).closest("div").attr("id");
        console.log(" class is: " + jkey + " data: " + JSON.stringify($('#' + id).data()) );
    });
});
/*$(".jkey").click(function(){
    alert('clicked!');
    var jkey = $("button").closest("div").attr("class");
});*/

