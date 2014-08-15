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

function get_data(url, job) {
    var obj = {
        jobkey: "{{job.jobkey}}",
        jobtitle: "{{job.jobtitle}}",
        company: "{{job.company}}",
        city: "{{job.city}}",
        state: "{{job.state}}",
        snippet: "{{job.snippet}}"
    }
    /*console.log(" url is: " + url + " data: " + JSON.stringify(job));
    $.ajax({
        url: "" + url,
        type: "GET",
        data: obj,
        success: function(data, status, xhr) {
            //console.log(data);
        },
        error: function(xhr, status, error) {
            console.log(xhr, status, error);
        }
    });*/
}
$(document).ready(function() {
    $("button").click(function(event) {
        //var request_path = event.target.id;
        var id = $(this).attr("id");
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
                },
                error: function(xhr, status, error) {
                    console.log(xhr, status, error);
                }
            });
        }
    });
});

