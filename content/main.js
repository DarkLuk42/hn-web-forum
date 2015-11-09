$(function(){
    $("div.hidden-form form, div.hidden-form .hide-form").hide();
    $("div.hidden-form .show-form").click(function(e){
        e.preventDefault();
        var div = $(this).closest("div.hidden-form");
        div.find("form, .hide-form").show();
        div.find(".show-form").hide();
        div.css({display: "block"});
    });
    $("div.hidden-form .hide-form").click(function(e){
        e.preventDefault();
        var div = $(this).closest("div.hidden-form");
        div.find(".show-form").show();
        div.find("form, .hide-form").hide();
        div.css({display: "inline-block"});
    });

    //$("button.btn-edit").text("⛭");
    //$("input.btn-edit").val("⛭");
    //$("button.btn-delete").text("☓");
    //$("input.btn-delete").val("☓");

    $("form").submit(function(e){
        $(this).find("input.required, textarea.required, select.required").each(function(){
            if( $(this).val() == "" )
            {
                $(this).addClass("error");
                e.preventDefault();
            }
            else
            {
                $(this).removeClass("error");
            }
        });
    });
})