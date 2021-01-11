for (let el of document.getElementByClass('chart')) {
    var data = {
        values = el.querySelector('.values').value,
        labels = el.querySelector('.labels').value
    }
    el.input
    new Chartist.Line(el.getAttrbute('id'), data)
}