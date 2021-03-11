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
				radius: 0,
				hitRadius: 3,
				hoverRadius: 3
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
})

var cnvs = $('.economy-chart').children('canvas');
var inp = $('.economy-chart').children('input');
inp = inp[0] ? inp[0].value : '';

var data = {
	values: [],
	labels: []
};
try {
	parsed = JSON.parse(inp)	
}
catch (e) { console.error(e) }

for (d in parsed) {
	data.labels.push(d)
}
data.labels.sort()
for (d of data.labels) {
	data.values.push(parsed[d])
}

var chart = new Chart(cnvs, {
	type: 'line',
	data: {
		labels: data.labels,
		datasets: [{			
			label: "Economy",
			data: data.values,
			borderColor: 'orange',
			fill: false,
			radius: 1,
			hitRadius: 7,
			hoverRadius: 5
		}]
	},
	options: {		
		lineTension: 0
	}
})

if (tarif) {
	tarif.onchange = function () {
		for (str of tbody.children) {
			str.children['XP_cost'].innerHTML = (tarif.value * str.children['XP'].innerHTML).toFixed(3)
			str.children['XP_percent'].innerHTML = ((str.children['XP_cost'].innerHTML / (str.children['total_power'].innerHTML*tarif.value))*100).toFixed(3)
	    }
	}
}