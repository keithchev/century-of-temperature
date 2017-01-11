(function () {

	"use strict";

	// global variable
	var TEMPS = {};

	// station metadata filename
	TEMPS.metadataFilename = './data/USHCN-network-metadata.clean-crop.txt';


	// region names/labels
	TEMPS.regions = [ {region: "wc", label: "West Coast"}, 
					{region: "mtw", label: "Mountain",}, 
					{region: "sw", label: "Southwest", },
				    {region: "miw", label: "Midwest", },
					{region: "gc", label: "Gulf Coast",},
					{region: "ec", label: "East Coast",} ];


	// hand-picked list of representative stations in each region
	TEMPS.roadTrip = [

		{id: "172765", text: "Farmington", region: "ec"},
		{id: "374266", text: "Kingston", region: "ec"},
		{id: "280325", text: "Atlantic City", region: "ec"},
		{id: "381549", text: "Charleston", region: "ec"},
		{id: "083186", text: "Fort Meyers", region: "gc"},
		{id: "410639", text: "Beeville", region: "gc"},
		{id: "291469", text: "Carlsbad", region: "sw"},
		{id: "029287", text: "Wickenburg", region: "sw"},
		{id: "046719", text: "Pasadena", region: "wc"},
		{id: "047916", text: "Santa Cruz", region: "wc"},
		{id: "450008", text: "Aberdeen", region: "wc"},
		{id: "241044", text: "Bozeman", region: "mtw"},
		{id: "052281", text: "Dillon", region: "mtw"},
		{id: "050848", text: "Boulder", region: "mtw"},
		{id: "145856", text: "Norton", region: "miw"},
		{id: "112193", text: "Decatur", region: "miw"},
	];


	// definition of tabs/parts 
	TEMPS.tabs = [{
					header: "Part 1",
					id: "highs-lows", 
					method: "loadTab1", 
					text: "Highs and lows",
					mapHeader: "The stations",
					histogramHeader: "Visualizing individual stations",
				}, 
	          	{
	              	header: "Part 2", 
	              	id: "changes", 
	              	method: "loadTab2", 
	              	text: "Changes over time",
	              	mapHeader: "Where have temperatures changed?",
	              	histogramHeader: "Visualizing changes",
	          	},
	          	{
	              	header: "Part 3", 
	              	id: "changes-all", 
	              	method: "loadTab3", 
	              	text: "Regional averages",
	              	mapHeader: "",
	              	histogramHeader: "",

	              },];


	window.TEMPS = TEMPS;

}());

