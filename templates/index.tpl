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
    <link href="http://fonts.googleapis.com/css?family=Rosario" rel="stylesheet" type="text/css">
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

  <body style="" bgcolor="#A9F5BC">

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
              <li><a href="/logout">Logout</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="row center">
	<div class="span8 offset2">

	  <center>
	    <br><br>
	    <h1><img src="/static/img/BookIcon.png" width="60"/>  Stemming</h1>
	    <h3>Great minds read alike.</h3>
	    <br><br><br>
	    Enter a Twitter user name or a list of search terms.
	    <br><br>
	    <form action="/search"  method="post">
	      <input type="text" class="input-large search-query" name="query"/>
	      <button class="btn btn-primary" id="search-button" type="submit">Search</button>
	    </form>

	    <br><br>
	    Or let these people inspire you:<br><br>
	    <div class="row-fluid">
	      <div class="span3 offset3">
		<p align="left"><img src="/static/img/BarackObama.jpg" />  <a href="search/BarackObama">Barack Obama</a></p>
		<p align="left"><img src="/static/img/Pontifex.jpg" />  <a href="search/Pontifex">Pope Francis I</a></p>
		<p align="left"><img src="/static/img/Cristiano.jpg" />  <a href="search/Cristiano">Cristiano Ronaldo</a></p>
	      </div>
	      <div class="span5 offset1">
		<p align="left"><img src="/static/img/PerezHilton.jpg" />  <a href="search/PerezHilton">Perez Hilton</a></p>
		<p align="left"><img src="/static/img/AmericanCancer.jpg" />  <a href="search/AmericanCancer">American Cancer Society</a></p>
		<p align="left"><img src="/static/img/AlGore.jpg" />  <a href="search/AlGore">Al Gore</a></p>
	      </div>
	    </div>
	    <br><br><br>
	  </center>
	</div>
      </div>
    </div>

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.js"></script>
    <script type="text/javascript" src="/static/jquery.backstretch.min.js"></script>
    <script type="text/javascript" src="/static/test.js"></script>
</body></html>
