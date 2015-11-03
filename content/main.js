window.onload = function () {
    var element_btn = document.getElementById("idKnopf");
    element_btn.onclick = switchView_p;
}

function switchView_p () {
    var element1_o = document.getElementById("idTabelle1");
    var element2_o = document.getElementById("idTabelle2");
    if (element1_o.style.display != "none") {
        element1_o.style.display = "none";
        element2_o.style.display = "table";
    } else {
        element2_o.style.display = "none";
        element1_o.style.display = "table";
    }
}