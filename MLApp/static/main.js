const password = $("#password").text();  
var list_label = $("#list_label").text();  
list_label = list_label.replace(/'/g, '"');
list_label = JSON.parse(list_label);
console.log(list_label)
console.log(typeof list_label)
console.log(password)
let model;
let modelLoaded = false;
async function loadModel() {
    console.log( "Loading model..." + (password) );
    const MODEL_URL = 'https://capture-static.s3.ca-central-1.amazonaws.com/models/'+(password)+'_model.json';
    model = await tf.loadLayersModel(MODEL_URL);
    console.log( "Model loaded." );
	$('.progress-bar').hide();
    modelLoaded = true;
};
loadModel();

let imageLoaded = false;
$("#image-selector").change(function () {
	imageLoaded = false;
	let reader = new FileReader();
	reader.onload = function () {
		let dataURL = reader.result;
		$("#selected-image").attr("src", dataURL);
		$("#prediction-list").empty();
		imageLoaded = true;
	}
	
	let file = $("#image-selector").prop('files')[0];
	reader.readAsDataURL(file);
});

$("#predict-button").click(async function () {
	if (!modelLoaded) { alert("The model must be loaded first"); return; }
	if (!imageLoaded) { alert("Please select an image first"); return; }
	
	let image = $('#selected-image').get(0);
	
	// Pre-process the image
	console.log( "Loading image..." );
	let tensor = tf.browser.fromPixels(image, 3)
		.resizeNearestNeighbor([180, 180]) // change the image size
		.expandDims()
		.toFloat()
		.reverse(-1); // RGB -> BGR
        
	let predictions = await model.predict(tensor).data();
	console.log(predictions);
	let top5 = Array.from(predictions)
		.map(function (p, i) { // this is Array.map
			return {
				probability: p,
				className: list_label[i] // we are selecting the value from the obj
			};
		}).sort(function (a, b) {
			return b.probability - a.probability;
		}).slice(0, 2);

	$("#prediction-list").empty();
	top5.forEach(function (p) {
		$("#prediction-list").append(`<li>${p.className}: ${p.probability.toFixed(6)}</li>`);
		});
});