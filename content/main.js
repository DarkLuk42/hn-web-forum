function showMessage(message){
    alert(message);
    /*
    var id = "alert-" + parseInt(Math.random()*1000);
    var alert = $("<p></p>").addClass("message").text(message).attr("id",id);
    $(".content").prepend(alert);
    //window.location.href = "#" + id;*/
};
function showError(message){
    alert(message);
    /*
    var id = "alert-" + parseInt(Math.random()*1000);
    var alert = $("<p></p>").addClass("message").addClass("message-error").text(message).attr("id",id);
    $(".content").prepend(alert);
    //window.location.href = "#" + id;*/
};

function updateDiscussion( data ){
    $(".discussion-title").text(data.title);
};

function createArticle( data ){
    $("tr[id^='article'").parent().append( data.html );
    registerHandlers("#article-" + data.article.alias);
};

function updateArticle( data ){
    var $tr = $("#article-" + data.article.alias);
    $tr.replaceWith( data.html );
    registerHandlers("#article-" + data.article.alias);
};

function deleteArticle( data ){
    var $tr = $("#article-" + data.article.alias);
    $tr.replaceWith( data.html );
    registerHandlers("#article-" + data.article.alias);
};

function createUser( data ){
    data.html = '<li id="user-' + data.user.alias + '">' +
                '<span class="user-name"></span>';
    if( user && user.role == "ADMIN" )
    {
        data.html += '(Rolle: <span class="user-role"></span>)' +
                     '<ul class="inline">' +
                     '<li>' +
                     '<form class="ajax inline-form" action="/delete_user" method="post">' +
                     '<input type="hidden" name="alias">' +
                     '<input class="btn-delete" type="submit" value="Benutzer löschen"/>' +
                     '</form>' +
                     '</li>' +
                     '<li>' +
                     '<div class="hidden-form">' +
                     '<button class="show-form btn-edit">bearbeiten</button>' +
                     '<button class="hide-form">abbrechen</button>' +
                     '<form class="ajax" action="/update_user" method="post">' +
                     '<input type="hidden" name="alias">' +
                     '<select name="role" class="required">' +
                     '<option value="ADMIN">Administrator</option>' +
                     '<option value="USER">Benutzer</option>' +
                     '<option value="USER_READONLY">Benutzer (nur lesen)</option>' +
                     '</select>' +
                     '<input type="text" name="name" placeholder="Name" class="required"/>' +
                     '<input type="text" name="password" placeholder="Passwort"/>' +
                     '<input type="submit" value="Benutzer bearbeiten"/>' +
                     '</form>' +
                     '</div>' +
                     '</li>' +
                     '</ul>';
    }
    data.html += '</li>';
    $("[id^='user'").parent().append( data.html );
    $("#user-" + data.user.alias).find("[name='alias']").val(data.user.alias);
    $("#user-" + data.user.alias).find("[name='name']").val(data.user.name);
    $("#user-" + data.user.alias).find("[name='role']").val(data.user.role);
    $("#user-" + data.user.alias).find(".user-role").text(data.user.role);
    $("#user-" + data.user.alias).find(".user-name").text(data.user.name);
    registerHandlers("#user-" + data.user.alias);
};

function updateUser( data ){
    var $tr = $("#user-" + data.user.alias);
    $tr.find(".user-name").text(data.user.name);
    $tr.find(".user-role").text(data.user.role);
};

function deleteUser( data ){
    $("#user-" + data.user.alias).remove();
};

function snakeToCamel(s){
    return s.replace(/(\_\w)/g, function(m){return m[1].toUpperCase();});
}

function registerHandlers(element)
{
    var $ele = $(element);
    $ele.find("div.hidden-form form, div.hidden-form .hide-form").hide();
    $ele.find("div.hidden-form .show-form").click(function(e){
        e.preventDefault();
        var div = $(this).closest("div.hidden-form");
        div.find("form, .hide-form").show();
        div.find(".show-form").hide();
        div.css({display: "block"});
    });
    $ele.find("div.hidden-form .hide-form").click(function(e){
        e.preventDefault();
        var div = $(this).closest("div.hidden-form");
        div.find(".show-form").show();
        div.find("form, .hide-form").hide();
        div.css({display: "inline-block"});
    });

    //$ele.find("button.btn-edit").text("⛭");
    //$ele.find("input.btn-edit").val("⛭");
    //$ele.find("button.btn-delete").text("☓");
    //$ele.find("input.btn-delete").val("☓");

    $ele.find("form").submit(function(e){
        $(this).find("input.required, textarea.required, select.required").each(function(){
            if( $(this).val() == "" )
            {
                $(this).addClass("error");
                e.preventDefault();
                e.stopPropagation();
            }
            else
            {
                $(this).removeClass("error");
            }
        });
    });

    $ele.find("form.ajax").submit(function(e){
        e.preventDefault();
        e.stopPropagation();
        var $this = $(this);
        if( $this.find(".required.error").length == 0 )
        {
            $("p.message").remove();
            var data = {};
            $this.find("input, textarea, select").each(function(i,ele){
                var $ele = $(ele);
                data[$ele.attr("name")] = $ele.val();
            });
            $.ajax({
                url: $this.attr("action"),
                type: $this.attr("method"),
                data: data,
                dataType: "json",
                success: function(data){
                    if( data.success )
                    {
                        var fn = snakeToCamel($this.attr("action").substring(1));
                        if( fn && window.hasOwnProperty(fn) )
                        {
                            window[fn](data.data);
                            showMessage(data.message);
                        }
                        else
                        {
                            showMessage(data.message);
                            if( data.redirect )
                            {
                                window.location.href = data.redirect
                            }
                            else
                            {
                                window.location.reload();
                            }
                        }
                    }
                    else
                    {
                        showError(data.message);
                    }
                },
                error: function(error){
                    if( error.responseJSON && error.responseJSON.message )
                    {
                        showError( error.responseJSON.message );
                    }
                    else
                    {
                        console.log( error );
                        showError( "Es ist leider etwas schief gelaufen..." );
                    }
                }
            });
        }
    });

    $ele.find(".btn-delete").click(function(e){
        if( !confirm("Wirklich löschen?") )
        {
            e.preventDefault()
        }
    });
}

$(function(){
    registerHandlers(document);
})