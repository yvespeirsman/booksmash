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
              <li><a href="/logout">Logout</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="center">
	<div class="margindiv">
	  <br>
	  <div class="row-fluid">
	    <div class="span6">
	      <h1><img src="/static/img/BookIcon.png" width="60"/>  Stemming</h1>
	    </div> 
	    <div class="span6">
	      <br>
	      <form action="/search"  method="post">
		<input type="text" class="input-large search-query" name="query"/>
		<button class="btn btn-primary" id="search-button" type="submit">Search</button>
	      </form>
	    </div>
	  </div>
	  <br>
	  %if len(r)==0:
	  <div class="alert alert-error">
	    <p>Sorry, we didn't find a Twitter user by that name</p>
	  </div>
	  %else:
	  <div class="row-fluid">
	    <div class="span6">
	      <!--
	      <ul class="breadcrumb">
		<li>Tweet analysis for {{q}}</li>
	      </ul>
	      <div class="row-fluid">
		<div class="span3 offset1">
		</div>
		<div class="span6">
		  <div class="progress progress-info">
		  </div>
		</div>
	      </div>
	      -->
	      
	      <ul class="breadcrumb">
		<li>{{len(r)}} most recent tweets for {{q}}</li>
	      </ul>
	      %for i in range(0, len(r)):
	      <blockquote>{{r[i]}}</blockquote>
	      %end
	    </div>
	    <div class="span6">
	      <ul class="breadcrumb">
		<li>Bookshelf for {{q}}</li>
	      </ul>
	      <div class="row-fluid">
		%for i in range(0, 3):
		<div class="span4">
		  <center>
		    <a href="/book/{{b[i]["isbn"]}}">
		      <img class="media-object margincover" src="{{b[i]["cover"]}}"/> 
		    </a>
		  </center>
		</div>
		%end
	      </div>
	      <div class="row-fluid">
		%for i in range(3, 6):
		<div class="span4">
		  <center>
		    <a href="/book/{{b[i]["isbn"]}}">
		      <img class="media-object margincover" src="{{b[i]["cover"]}}"/>		  
		    </a>
		    <center>
		</div>
		%end
	      </div>
	      
	      
	      <div class="row-fluid">
		%for i in range(6, 9):
		<div class="span4">
		  <center>
		    <a href="/book/{{b[i]["isbn"]}}">
		      <img class="media-object margincover" src="{{b[i]["cover"]}}"/>		  
		    </a>
		  </center>
		</div>
		%end
	      </div>
	      <div class="row-fluid">
		%for i in range(9, 12):
		<div class="span4">
		  <center>
		    <a href="/book/{{b[i]["isbn"]}}">
		      <img class="media-object margincover" src="{{b[i]["cover"]}}"/>		  
		    </a>
		  </center>
		</div>
		%end
	      </div>
	    </div>
	  </div>
	  %end
	</div>
      </div> <!-- /container -->
    </div>
    
    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.js"></script>
      <script type="text/javascript" src="/static/jquery.backstretch.min.js"></script>
    <script type="text/javascript" src="/static/test.js"></script>

</body></html>
