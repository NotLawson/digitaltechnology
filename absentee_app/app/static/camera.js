var width = 320;
var height = 0;
var streaming = false;


// play the camera output 
navigator.mediaDevices.getUserMedia({video: true, audio: false})
        .then(function (stream) {
            video.srcObject = stream;
            video.play();
        })
        .catch(function (err) {
            console.log("An error occured! " + err);
        });
video.addEventListener('canplay', function (ev) {
    if (!streaming) {
        height = video.videoHeight / (video.videoWidth / width);
        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);

        streaming = true;
    }
}, false);

//when the button clicked
startbutton.addEventListener('click', function (ev) {
    takepicture(); // take a picture
    ev.preventDefault();
}, false);

//when clicked not you
notyou.addEventListener('click', function (ev) {
    takepicture(); // retake picture
    ev.preventDefault();
}, false);

clearphoto(); // clear the photo canvas before anything



function clearphoto() { // clears the photo canvas
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);
}

function takepicture() {
    var context = canvas.getContext('2d');
    if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height); // draws the image capture on the canvas

        var dataURL = canvas.toDataURL("image/jpeg", 0.95); // 
        if (dataURL && dataURL != "data:,") {
            var fileName = generateImageName();
            uploadimage(dataURL, fileName);
        } else {
            alert("Image not available");
        }
    } else {
        clearphoto();
    }
}

function generateImageName() {
    let imageName = "image"
    return imageName;
}

function uploadimage(dataurl, filename) {
    const options = {
        method: 'POST',
        body: dataurl,
    };
      
    fetch('/subimage', options).then(async r => document.getElementById("name").value = await r.text())
    document.getElementById("action").removeAttribute("hidden")
    document.getElementById("startbutton").attributes.hidden = "true"
}
