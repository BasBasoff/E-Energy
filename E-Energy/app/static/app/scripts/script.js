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
var tar = tarif.value
inp = inp[0] ? inp[0].value : '';

var data = {
	values: [],
	labels: []
};
try {
	parsed = JSON.parse(inp)	
}
catch (e) { console.error(e) }

var even = 0;
var odd = 0;
var x8 = [];
var x0 = [];
for (j = 0; j < parsed[0].length; j++) {
	for (i = 0; i < parsed.length; i++) {
		if (i % 2 == 0) {
			even += parsed[i][j];
		}
		else {
			odd += parsed[i][j];
        }
	}
	x0.push(odd);
	x8.push(even);
}
for (i in x0) {
	data.values.push(((x0[i] / x8[0]) * 100) - 100);
}

var chart = new Chart(cnvs, {
	type: 'line',
	data: {
		//labels: parsed['datetime'],
		datasets: [{			
			label: "Economy",
			data: data.values,
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