import cgi, cgitb
import os

cgitb.enable()

form=cgi.FieldStorage()

u=form.getvalue("user","Guest")

print("Content-Type: text/html\n\n")
print("""
<!DOCTYPE html>
<html lang="en" dir="ltr">
    <head>
        <meta charset="utf-8">
        <title>BUCC Academic Database</title>
        <link rel="stylesheet" href="assets/stylesheets/bootstrap.min.css" >
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.5.0/css/all.css" integrity="sha384-B4dIYHKNBt8Bc12p+WXckhzcICo0wtJAoU8YZTY5qE0Id1GSseTk6S+L3BlXeVIU" crossorigin="anonymous">
        <link rel="stylesheet" href="assets/stylesheets/default.css" >
        <style>
            .loader {
            border: 16px solid #f3f3f3;
            border-radius: 50%;
            border-top: 16px solid #3498db;
            width: 40px;
            height: 40px;
            -webkit-animation: spin 2s linear infinite; /* Safari */
            animation: spin 2s linear infinite;
            }

            /* Safari */
            @-webkit-keyframes spin {
            0% { -webkit-transform: rotate(0deg); }
            100% { -webkit-transform: rotate(360deg); }
            }

            @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
            }
            .animate-bottom {
            position: relative;
            -webkit-animation-name: animatebottom;
            -webkit-animation-duration: 1s;
            animation-name: animatebottom;
            animation-duration: 1s
            }

            @-webkit-keyframes animatebottom {
            from { bottom:-100px; opacity:0 } 
            to { bottom:0px; opacity:1 }
            }

            @keyframes animatebottom { 
            from{ bottom:-100px; opacity:0 } 
            to{ bottom:0; opacity:1 }
            }
        </style>
	    <script src="assets/js/jquery-3.2.1.min.js" ></script>
        <script src="assets/js/popper.min.js" ></script>
        <script src="assets/js/bootstrap.min.js" ></script>
        <script src="assets/js/default.js" ></script>
	    <script>
			function searchKey(that){
				$.ajax({
					url: 'predict.py',
					method: 'post',
					data: { search_item: that.value },
					success: function(hh){
						var f = hh.split(",");
						f.sort();
						var myNode = document.getElementById("data");
						while (myNode.firstChild) {
							myNode.removeChild(myNode.firstChild);
						}
						f.forEach(funk);
						function funk(value){	
							var z = document.createElement("OPTION");
							z.setAttribute("value",value);
							document.getElementById("data").appendChild(z);
						}
							
					}
				});
			}
        </script>
        <script>
            function searched(){
                document.getElementById("history").removeAttribute("class");
                $("#search_item").blur();
                var myNode = document.getElementById("history");
                while (myNode.firstChild) {
					myNode.removeChild(myNode.firstChild);
				}
                var load = document.createElement("div");
                load.setAttribute("class","loader");
                var b =document.createElement("center");
                b.appendChild(load);
                document.getElementById("history").appendChild(b);
                $.ajax({
                    url: 'search.py',
                    method: 'post',
                    data: { search_item: $("#search_item").val() },
                    success: function(fin){
                        var myNode = document.getElementById("history");
                        while (myNode.firstChild) {
							myNode.removeChild(myNode.firstChild);
						}
                        if(fin.length == 2){
                            var n = document.createElement("h4");
                            n.setAttribute("class","display-4");
                            var v = document.createTextNode("No match for search query.");
                            n.appendChild(v);
                            myNode.appendChild(n);
                            return;
                        }
                        var f = fin.split("|");
                        var n = document.createElement("h4");
                        n.setAttribute("class","display-4");
                        var h=document.createTextNode("Results");
                        n.appendChild(h);
                        myNode.appendChild(n);
                        var p = document.createElement("ul");
                        p.setAttribute("class","list-group");
                        f.forEach(funk);
                        function funk(value){
                            a = value.split(":");
                            var x = document.createElement("li");
                            var i = document.createElement("i");
                            var d1 = document.createElement("div");
                            var d2 = document.createElement("div");
                            var d3 = document.createElement("div");
                            var d4 = document.createElement("div");
                            var l = document.createElement("a");
                            l.setAttribute("href",a[0]);
                            i.setAttribute("class","fas fa-history");
                            var t1=document.createTextNode(a[1]);
                            var t2=document.createTextNode("time accessed");
                            x.setAttribute("class","list-group-item");
                            d1.setAttribute("class","row");
                            d2.setAttribute("class","col");
                            d3.setAttribute("class","col-md-7");
                            d4.setAttribute("class","col-md-3");
                            x.appendChild(l);
                            l.appendChild(d1);
                            d1.appendChild(d2);
                            d1.appendChild(d3);
                            d1.appendChild(d4);
                            d2.appendChild(i);
                            d3.appendChild(t1);
                            d4.appendChild(t2);
                            p.appendChild(x);
                        }
                        myNode.setAttribute("class","animate-bottom");
                        myNode.appendChild(p);
                    }
                });
            }
        </script>
    </head>
    <body>
        <div id="wrapper" >
            <div class="container" >
                <div class="row" id="home">
                    <div class="col-md-8 mx-auto">
                        <h4 class="display-4 mt-5 text-center" >B.U.C.C. Academic Database</h4>
""")
print("""
                        <h5 class="display-5 text-center">Hello {}</h5>
""".format(u))
print("""
                        <form id="search-form" method="post" onsubmit="return false;">
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <i class="fas fa-search"></i>
                                </div>
                                <input type="text" name="search_item" placeholder="What are you looking for?" autocomplete="off" id="search_item" autofocus onkeyup=searchKey(this) list= "data" class="form-control" >
                                <div class="input-group-append">
                                    <button type="submit" name="button" onclick=searched() class="btn btn-primary">SEARCH</button>
				                <datalist name="sugg" id="data"></datalist>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>

                <div id="history">
                </div>
            </div>
        </div>
    </body>
</html>
""")
