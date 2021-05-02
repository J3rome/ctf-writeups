<!DOCTYPE html>
<html>
<head>

<link rel="stylesheet" href="style.css">

<title>USER</title>
<style>

.avatar {
   margin-left:10px;
   margin-top:80px;
   vertical-align: middle;
   width: 50px;
   height: 50px;
   border-radius: 50%;
   border:3px solid black;
}
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #333;
}

li {
  float: left;
}

li a {
  display: block;
  color: white;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}

li a:hover {
  background-color: #111;


}
</style>

</head>
<body style="background-color:black">
<ul>
  <li><a class="active" href="dashboard.php">Home</a></li>
  <li><a href="news.php">News</a></li>
  <li><a href="contact.php">Contact</a></li>
  <li><a href="detail.php">Details</a></li>
  <li><a href="logout.php">Logout</a></li>
</ul>


<br><br><br><br><br>
</body>
























































<!-- try to use "page" as GET parameter-->
</html>

<?php
$con=mysqli_connect("localhost","root","myrootpass","db");
session_start();
if(isset($_SESSION['IS_LOGIN']))
{
$is_admin=$_SESSION['isadmin'];
echo "<h2 style='color:Tomato;margin-left:100px;margin-top:-80px'>Find out who you are :) </h2>";
echo "<br><br><br>";
if($is_admin==="true")
{
echo '<div style="align:center;" class="divf">';
echo '<form class="box" method="POST" style="text-align:center">';
echo '<input required AUTOCOMPLETE="OFF" style="text-align:center;" type="text" placeholder="user" name="name"><br><br>';
echo '<input type="submit" value="whoami" name="sub">';
echo '</form>';
echo '</div>';
if(isset($_GET["page"]))
{
		$page=$_GET["page"];
		$file = str_replace(array( "../", "..\"" ), "", $page );
		echo $file;
		include($file);
}
$formuser=mysqli_real_escape_string($con,$_POST['name']);
if(isset($_POST['sub']))
	{
		$sql="select * from user where username='$formuser'";
                $details = mysqli_fetch_assoc(mysqli_query($con,$sql));
		$det=json_encode($details);
		echo "<pre style='color:red;font-size:14px'>$det</pre>";
		$msg="Details are saved in a file";
		echo "<script>alert('details saved in a file')</script>";
	}
}
else
{
echo "<h3 style='color:red;text-align:center'>You can't access this feature!'</h3>";
}
}
else
{
header('Location: index.php');
}

?>
