<?php
echo "yolo\n";
$key='^$(expr substr $(grep ^W <(cat test)) 1 1)';
$key="$(grep '.' <(test))";
passthru("grep -i \"$key\" dictionary.txt");
