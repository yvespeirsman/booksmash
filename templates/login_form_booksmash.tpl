<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta content="text/html; charset=utf-8" http-equiv="content-type">
<title>ReadTweet</title>

     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <meta name="description" content="">
     <meta name="author" content="">
     <link href="/static/bootstrap.css" rel="stylesheet">
     <link href="/static/base.css" rel="stylesheet">
     <link href="/static/bootstrap-responsive.css" rel="stylesheet">
     <link href="http://fonts.googleapis.com/css?family=Rosario" rel="stylesheet" type="text/css">
     <style>
       body {
	 padding-top: 40px;
	 padding-bottom: 40px;
	 background-color: #f5f5f5;
       }      .form-signin {
	 max-width: 300px;
	 padding: 19px 29px 29px;
	 margin: 0 auto 20px;
	 background-color: #fff;
	 border: 1px solid #e5e5e5;
	 -webkit-border-radius: 5px;
	    -moz-border-radius: 5px;
		 border-radius: 5px;
	 -webkit-box-shadow: 0 1px 2px rgba(0,0,0,.05);
	    -moz-box-shadow: 0 1px 2px rgba(0,0,0,.05);
		 box-shadow: 0 1px 2px rgba(0,0,0,.05);
       }
       .form-signin .form-signin-heading,
       .form-signin .checkbox {
	 margin-bottom: 10px;
       }
       .form-signin input[type="text"],
       .form-signin input[type="password"] {
	 font-size: 16px;
	 height: auto;
	 margin-bottom: 15px;
	 padding: 7px 9px;
       }

     </style>
 </head>
 <body style="">

   <div class="container">
     <form class="form-signin" action="login" method="post" name="login">
       <h2 class="form-signin-heading">Please sign in</h2>
       <input type="text" class="input-block-level" placeholder="username" name="username" />
       <input type="password" class="input-block-level" placeholder="password" name="password" />
       <br/><br/>
       <button type="submit" class="btn btn-large btn-primary"> OK </button>
     </form>
   </div>
 </body>
</html>
