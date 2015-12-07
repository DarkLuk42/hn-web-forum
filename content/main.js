function showMessage(message){
    alert(message);
    /*
    var id = "alert-" + parseInt(Math.random()*1000);
    var alert = $("<p></p>").addClass("message").text(message).attr("id",id);
    $(".content").prepend(alert);
    //window.location.href = "#" + id;
};
function showError(message){
    alert(message);
    /*
    var id = "alert-" + parseInt(Math.random()*1000);
    var alert = $("<p></p>").addClass("message").addClass("message-error").text(message).attr("id",id);
    $(".content").prepend(alert);
    //window.location.href = "#" + id;*/
};

function createArticle( data ){
    $("tr[id^='article'").parent().append( data.html );
    registerHandlers("#article-" + data.article.alias);
};

function deleteArticle( data ){
    var $tr = $("#article-" + data.article.alias);
    $tr.replaceWith( data.html );
    registerHandlers("#article-" + data.article.alias);
};

function updateArticle( data ){
    var $tr = $("#article-" + data.article.alias);
    $tr.replaceWith( data.html );
    registerHandlers("#article-" + data.article.alias);
};

function snakeToCamel(s){
    return s.replace(/(\_\w)/g, function(m){return m[1].toUpperCase();});
}

function registerHandlers(element)
{
    var $ele = $(element);
    console.log($ele);
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
                    showMessage(data.message);
                    if( fn && window.hasOwnProperty(fn) )
                    {
                        window[fn](data.data);
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