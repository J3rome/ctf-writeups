function XMLFunction(nb, search){
    var xml = '' +
        '<?xml version="1.0" encoding="UTF-8"?>' +
        '<root>' +
        '<name>' + nb + '</name>' +
        '<search>' + search + '</search>' +
        '</root>';
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if(xmlhttp.readyState == 4){
            console.log(xmlhttp.readyState);
            console.log(xmlhttp.responseText);
            document.getElementById('errorMessage').innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("POST","forms.php",true);
    xmlhttp.send(xml);
};