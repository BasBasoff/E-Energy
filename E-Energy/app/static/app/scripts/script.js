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

tarif.onchange = function () {
	for (str of tbody.children) {
		str.children['XP_cost'].innerHTML = (tarif.value * str.children['XP'].innerHTML).toFixed(3)
		str.children['XP_percent'].innerHTML = ((str.children['XP_cost'].innerHTML / (str.children['XP'].innerHTML*tarif.value))*100).toFixed(3)
    }
}