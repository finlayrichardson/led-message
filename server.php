<?php
	if ($_POST['key'] == "") {
        $message = $_POST['message'];
		file_put_contents("messages.txt", $message);
	}
?>
