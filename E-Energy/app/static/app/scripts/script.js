var data = {
        series : [JSON.parse(document.querySelector('.chart > input').value)],
        labels : ""
    }    
    new Chartist.Line(document.querySelector('.chart'), data)
