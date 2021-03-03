$('.chart').each(function () {
	var cnvs = $(this).children('canvas');
	var i = $(this).children('input');
	
	i = i[0] ? i[0].value : '';
	var data = {};

	var color;
	if (cnvs.attr('id') !== undefined) {
		if (cnvs.attr('id').includes('1')) {
			color = 'orange'
		} else if (cnvs.attr('id').includes('2')) {
			color = 'green'
		} else if (cnvs.attr('id').includes('3')) {
			color = 'blue'
		}
	}

	try {
		data.values = JSON.parse(i).map(function (d) {
			return d.y
		}).sort(
			//data = [JSON.parse(i).map(function (d) { return { x: moment(new Date(d.x)).format("DD/MM/YY HH:mm"), y: d.y } }).sort(
			function (a, b) {
				return a.x > b.x ? 1 : -1;
			}
		)
		data.labels = JSON.parse(i).map(function (d) { return moment(new Date(d.x)).format("DD/MM/YY HH:mm") })
	}
	catch (e) { console.error(e) }

	var chart = new Chart(cnvs, {
		type: 'line',
		data: {
			labels: data.labels,
			datasets: [{
				label: cnvs.attr('id'),
				data: data.values,
				borderColor: color,
				fill: false,
				radius: 0
			}]
		},
		options: {
			scales: {
				xAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Date time'
					}
				}],
				yAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Value'
					}
				}]
			}
		}
	})
})

var cnvs = $('.economy-chart').children('canvas');
var inp = $('.economy-chart').children('input');
var tarif = 
inp = inp[0] ? inp[0].value : '';
inp = inp.replace(/\'/g, '\"');

var data = {
	values: []
};
try {
	parsed = JSON.parse(inp)[0]	
	for (item = 0; item < parsed.length; item++) {
		data.values[item] = JSON.parse(parsed[item])
    }
}
catch (e) { console.error(e) }

var summ = 0;
var result = [];
for (i = 0; i < data.values[0].length; i++) {
	for (j = 0; j < data.values.length; j++) {
		summ += data.values[j][i];
	}
	result.push(summ);
}

var chart = new Chart(cnvs, {
	type: 'line',
	data: {
		//labels: data.labels,
		datasets: [{			
			label: "Ёкономи€",
			data: result,
			borderColor: 'orange',
			fill: false,
			radius: 0
		}]
	},
	options: {
		scales: {
			xAxes: [{
				display: true,				
			}],
			yAxes: [{
				display: true,				
			}]
		}
	}
})

tarif.onchange = function () {
	for (str of tbody.children) {
		str.children['XP_cost'].innerHTML = (tarif.value * str.children['XP'].innerHTML).toFixed(3)
		str.children['XP_percent'].innerHTML = ((str.children['XP_cost'].innerHTML / (str.children['total_power'].innerHTML*tarif.value))*100).toFixed(3)
    }
}