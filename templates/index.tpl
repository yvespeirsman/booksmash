<!DOCTYPE html>
<!-- saved from url=(0065)http://twitter.github.io/bootstrap/examples/starter-template.html -->
<html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <title>Stemming</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="/static/bootstrap.css" rel="stylesheet">
    <link href="/static/base.css" rel="stylesheet">
    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }
    </style>
    <link href="/static/bootstrap-responsive.css" rel="stylesheet">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="../assets/js/html5shiv.js"></script>
    <![endif]-->

  </head>

  <body style="">

    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="brand" href="/">Stemming</a>
          <div class="nav-collapse collapse">
            <ul class="nav">
              <li><a href="/Logout">Logout</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="container">

      <center>
	<br><br><br>
	<h1>Stemming</h1>
	<h3>Find books that <em>move</em> you.</h3>
	<br><br><br>
	Enter a Twitter user name or a list of search terms.
	<br><br>
	<form action="/search"  method="post">
	  <input type="text" class="input-large search-query" name="query"/>
	  <button class="btn btn-primary" id="search-button" type="submit"><i class="icon-search icon-white"></i> Search</button>
	</form>

	<br><br>
	Or let these people inspire you:<br><br>
        <img src="/static/img/barack_obama.jpg" />Barack Obama
      </center>
    </div> 

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.js"></script>

</body></html>
