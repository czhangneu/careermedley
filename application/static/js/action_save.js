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
    console.log(" ==== tag: " + tag + " data: " + data);

    $(tag).data("job",data);
    console.log(" saved data: " + JSON.stringify($(tag).data("job")) );
}

function set_form(doc,obj) {
    var c_div = $(obj).closest("div");
    var parent = $(c_div).parent();
    var form_elem = $(parent).children("input")
    $(form_elem).val(doc);
}

function split_id(id) {

}
$(document).ready(function() {
    $(".datepicker").datepicker('update').on('changeDate', function(ev) {
        console.log(" got a change");
        $(this).datepicker('hide');
    });

    $(".delete_button").click(function(event) {
        var id = $(this).attr("id");
        id = id.split("_");
        if (id != undefined) {
            console.log(" delete job: " + id[2]);
            $.ajax({
                url: "/user/" + id[1] + "/bookmarked/" + id[2],
                type: "GET",
                success: function(data, status, xhr) {
                    //console.log(data);
                    $(document.body).html(data);
                },
                error: function(xhr, status, error) {
                    console.log(xhr, status, error);
                }
            });
        }
    });

    $(".apply_button").click(function(event) {
        var id = $(this).attr("id");
        id = id.split("_");
        if (id != undefined) {
            console.log(" apply for job: " + id[2]);
            /*alert(" Would you like to apply for job id: " + id[2] + " ?");
            var r = confirm("Press a button");
            if (r == true) {
                x = "You pressed OK!";
            } else {
                x = "You pressed Cancel!";
            }*/
            $.ajax({
                url: "/user/" + id[1] + "/apply/" + id[2],
                type: "GET",
                success: function(data, status, xhr) {
                    //console.log(data);
                },
                error: function(xhr, status, error) {
                    console.log(xhr, status, error);
                }
            });
        }
    });

    $(".save_button").click(function(event) {
        var id = $(this).attr("id");
        id = id.split("_");
        if (id != undefined) {
            $.ajax({
                url: "/user/" + id[1] + "/" + id[2],
                type: "GET",
                success: function(data, status, xhr) {
                    //console.log(data);
                },
                error: function(xhr, status, error) {
                    console.log(xhr, status, error);
                }
            });
        }
    });

    /*$("button").click(function(event) {
        //var request_path = event.target.id;
        var id = $(this).attr("id");
        console.log("id is: " + id);
        if(id != undefined) {
            id = id.split("_");
            console.log(" button: " + id[0] + " nickname: " + id[1] + " job: " + id[2]);
            if(id[0] == "save") {
                $.ajax({
                    url: "/user/" + id[1] + "/" + id[2],
                    type: "GET",
                    success: function(data, status, xhr) {
                        //console.log(data);
                    },
                    error: function(xhr, status, error) {
                        console.log(xhr, status, error);
                    }
                });
            }
            else if(id[0] == "delete") {
                console.log(" delete job: " + id[2]);
                $.ajax({
                    url: "/user/" + id[1] + "/bookmarked/" + id[2],
                    type: "GET",
                    success: function(data, status, xhr) {
                        //console.log(data);
                        $(document.body).html(data);
                    },
                    error: function(xhr, status, error) {
                        console.log(xhr, status, error);
                    }
                });
            }
            else if (id[0] == "apply") {
                console.log(" apply for job: " + id[2]);
                alert(" Would you like to apply for job id: " + id[2] + " ?");
                var r = confirm("Press a button");
                if (r == true) {
                    x = "You pressed OK!";
                } else {
                    x = "You pressed Cancel!";
                }
                $.ajax({
                    url: "/user/" + id[1] + "/apply/" + id[2],
                    type: "GET",
                    success: function(data, status, xhr) {
                        //console.log(data);
                    },
                    error: function(xhr, status, error) {
                        console.log(xhr, status, error);
                    }
                });
            }
        }
    });*/
});

