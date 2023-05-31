function verify(selected) {
    if(selected.length==1){
        return true;
    }

    let selectedArr = new Array(selected.length);
    for(let i=0;i<selected.length;i++){
        selectedArr[i] = selected[i].split("_")
        selectedArr[i][1] = parseInt(selectedArr[i][1])
    }
    if(checkSameValue(selectedArr)){
        return true;
    }
    else if(checkStraight(selectedArr)){
        return true;
    }
    else{
        return false;
    }

}


// see if 6,6,6,6
function checkSameValue(selected){
    for(let i=0;i<selected.length-1;i++){
        if(selected[i][1]==selected[i+1][1]){
            continue;
        }
        else{
            return false;
        }
    }
    return true;
}

function checkStraight(selected){
    for(let i=0;i<selected.length-1;i++){
        if(selected[i][0]==selected[i+1][0]){
            continue;
        }
        else{
            return false;
        }
    }

    selected.sort(function(a, b) {
        return a[1] - b[1];
    });

    console.log(selected);
    if(selected[0][1]==1){
        let val = checkInSeries(selected);
        if(val){
            return true;
        }
        else if(!val){
            selected.shift();
            if(checkInSeries(selected) && selected[selected.length-1][1]==13){
                return true;
            }
            return false;
        }

    }
    else{
        checkInSeries(selected);
    }

}

function checkInSeries(selected){
    for(let i=0;i<selected.length-1;i++){
            if((selected[i+1][1]-selected[i][1])==1){
                continue;
            }
            else{
                return false;
            }
        }
        return true;
}

