
$('.chart').each(function () {
	var i = $(this).children('input');
	i = i[0] ? i[0].value : ''; 
	var data = {
	    series : [],
	    labels : ""
	};
	try {data.series = [JSON.parse(i).map(function(d){return {x: new Date(d.x), y: d.y}}).sort(
		function(a,b){
			return a.x>b.x ? 1 : -1;
		}
	)]
	}
	catch (e) { console.error(e) }
	new Chartist.Line(this, data, {
		fullWidth: true, 
		height: '400px', 
		showPoint: false,
		axisX: {
			type: Chartist.FixedScaleAxis,
			divisor: 30,
			labelInterpolationFnc: function(value) {return moment(value).format('DD/MM hh:mm:ss')}
		}
	})
})

$('.chart').each(function () {
	var cnvs = $(this).children('canvas');
	var i = $(this).children('input');
	i = i[0] ? i[0].value : '';
	var data

	var color;
	if (cnvs.attr('id').includes('1')) {
		color = 'red'
	} else if (cnvs.attr('id').includes('2')) {
		color = 'green'
	} else if (cnvs.attr('id').includes('3')) {
		color = 'blue'
    }
		
	
	try {
		data = [JSON.parse(i).map(function (d) { return { x: moment(new Date(d.x)).format("DD/MM/YY HH:mm"), y: d.y } }).sort(
			function (a, b) {
				return a.x > b.x ? 1 : -1;
			}
		)]
	}
	catch (e) { console.error(e) }

	var chart = new Chart(cnvs, {
		type: 'scatter',
		data: {			
			datasets: [{
				label: cnvs.attr('id'),
				data: data,
				borderColor: color
			}]
		},
		options: {
			scales: {
				xAxes: [{
					type: 'linear',
					position: 'bottom'
                }]
            }
        }
	})
})