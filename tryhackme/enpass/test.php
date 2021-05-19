<?php

$title = $argv[1];

$val = explode(",",$title); // Splitted on ','
$sum = 0;

for($i = 0 ; $i < 9; $i++){
    if ( (strlen($val[0]) == 2) and (strlen($val[8]) ==  3 ))  {
        // First element len = 2
        // Ninth element len = 3
        echo $sum;
        if ( $val[5] !=$val[8]  and $val[3]!=$val[7] ) {
            // elements must not
            $sum = $sum+ (bool)$val[$i]."<br>"; 
            }
    }
}

echo $sum;

if(($sum) == 9){
    echo "OK";
}else{
    echo "NOP";
}
?>
