//SET UP EXPRESS
var express = require('express');
var app = express();

//For config files
var fs = require('fs');
var path = require('path');

//var bodyParser = require('body-parser');
//app.use(bodyParser.urlencoded({extended:false}));
//app.use(bodyParser.json());

var engines = require('consolidate');
app.engine('html', engines.hogan); // tell Express to run .html files through Hogan
app.set('views', __dirname); // tell Express where to find templates, in this case the '/templates' directory
app.set('view engine', 'html'); //register .html extension as template engine so we can render .html pages 

app.use(express.static(__dirname + '/public')); //client-side js & css files

var stateCodes = {
			    "AL": "Alabama","AK": "Alaska","AS": "American Samoa","AZ": "Arizona","AR": "Arkansas","CA": "California","CO": "Colorado","CT": "Connecticut","DE": "Delaware","DC": "District Of Columbia","FM": "Federated States Of Micronesia","FL": "Florida","GA": "Georgia","GU": "Guam","HI": "Hawaii","ID": "Idaho","IL": "Illinois","IN": "Indiana","IA": "Iowa","KS": "Kansas","KY": "Kentucky","LA": "Louisiana","ME": "Maine","MH": "Marshall Islands","MD": "Maryland","MA": "Massachusetts","MI": "Michigan","MN": "Minnesota","MS": "Mississippi","MO": "Missouri","MT": "Montana","NE": "Nebraska","NV": "Nevada","NH": "New Hampshire","NJ": "New Jersey","NM": "New Mexico","NY": "New York","NC": "North Carolina","ND": "North Dakota","MP": "Northern Mariana Islands","OH": "Ohio","OK": "Oklahoma","OR": "Oregon","PW": "Palau","PA": "Pennsylvania","PR": "Puerto Rico","RI": "Rhode Island","SC": "South Carolina","SD": "South Dakota","TN": "Tennessee","TX": "Texas","UT": "Utah","VT": "Vermont","VI": "Virgin Islands","VA": "Virginia","WA": "Washington","WV": "West Virginia","WI": "Wisconsin","WY": "Wyoming"
			}

//ROUTING
app.get('/', function(req, res){
	console.log('- Request received:', req.method);
	res.render('index.html');
});

app.get('/state/:name', function(req, res){


	fs.readFile('states.json', function(err, data){
		var alldata = JSON.parse(data);
		var statedata = alldata.features.find(state => (state.properties.NAME == stateCodes[req.params.name])).geometry;//get the geometry/coordinates corresponding to the state in question
		console.log(statedata);
		console.log(err);
		res.send(JSON.stringify(statedata))
	});

})
//SERVER SET UP

app.listen(8080, function(){
	console.log('– Server listening on port 8080');
});

process.on('SIGINT', function(){
	console.log('\nI\'m closing');
	process.exit(0);
});