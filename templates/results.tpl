<!DOCTYPE html>
<!-- saved from url=(0065)http://twitter.github.io/bootstrap/examples/starter-template.html -->
<html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <title>Stemming</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="http://twitter.github.io/bootstrap/assets/css/bootstrap.css" rel="stylesheet">
    <link href="/static/base.css" rel="stylesheet">
    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }
    </style>
    <link href="http://twitter.github.io/bootstrap/assets/css/bootstrap-responsive.css" rel="stylesheet">

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
          <a class="brand" href="http://0.0.0.0:5000">Stemming</a>
          <!--<div class="nav-collapse collapse">
            <ul class="nav">
              <li><a href="http://twitter.github.io/bootstrap/examples/starter-template.html#about">About</a></li>
            </ul>
          </div>/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container">

	<center>
	  <form action="/search"  method="post">
		  <input type="text" class="input-large search-query" name="query"/>
		  <button class="btn btn-primary" id="search-button" type="submit"><i class="icon-search icon-white"></i> Search</button>
	  </form>

	</center>

	%if len(r)==0:
	<div class="alert alert-error">
	  <p>Sorry, we didn't find a Twitter user by that name</p>
	</div>
	%else:
	<div class="row">
	  <div class="span6">
	    <ul class="breadcrumb">
	      <li>{{len(r)}} most recent tweets for {{q}}</li>
	    </ul>
	    <!--<table>
	      <tbody>
		<tr><td>-->
	            %for i in range(0, len(r)):
		    <blockquote>{{r[i]}}</blockquote>
		    %end
                <!--</td></tr>
	      </tbody>
	    </table>-->
	  </div>
	  <div class="span6">
	    <ul class="breadcrumb">
	      <li>10 best books</li>
	    </ul>
	    <ul class="media-list">
	      %for i in range(0, len(b)):
		<li class="media">
		  <a href="book/{{b[i]["isbn"]}}">
		  <div class="well">
		    <div class="media-body">
		    <div class="pull-left">
		      <img class="media-object margincover" src="{{b[i]["cover"]}}"/>
		    </div>
		    <div class="media-body">
		    <h4 class="media-heading">{{b[i]["title"]}}</h4>
		    <p>{{b[i]["author"]}} {{b[i]["isbn"]}}</p>
		    </div>
		    </div>
		  </a>
		</li>
	
		%end
	    </ul>	    
	  </div>
	    %end
    </div> <!-- /container -->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.js"></script>
    <script type="text/javascript" src="/static/script.js" charset="utf-8"></script>
  

</body></html>
