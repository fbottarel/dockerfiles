function myprint(num) {
    out="-"$(num-1);
    for(i=num;i<=NF;i++){
        out=out"-"$i
    };
    print out
}

BEGIN { FS="-"} {
    if ($3 ~ "cudnn" || $3 ~ "test" || $3 ~ "deploy") {
        if (!length($4)) {
            exit
        }
        myprint(5)
    } else if ( NF > 2 ) {
        myprint(4)
    }
}
