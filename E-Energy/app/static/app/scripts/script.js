$('.chart').each(function(){
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
	)]} catch (e) {console.error(e)}
	new Chartist.Line(this, data, {
		//fullWidth: true, 
		height: '400px', 
		showPoint: false,
		axisX: {
			type: Chartist.FixedScaleAxis,
			divisor: 30,
			labelInterpolationFnc: function(value) {return moment(value).format('DD hh:mm:ss')}
		}
	})
})
