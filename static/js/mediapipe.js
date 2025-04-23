// import * as vision from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js";

// Setup Mediapipe
let handLandmarker, poseLandmarker, frameDataArray = [], collecting = false;
let holisticResults = null;
let video = null; // Make video accessible globally

const holistic = new Holistic({
    locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`;
    }
});

holistic.onResults(results => {
    // Store the full results object
    holisticResults = results;
});

async function setupMediapipe() {
    holistic.setOptions({
        modelComplexity: 1,
        smoothLandmarks: true,
        enableSegmentation: false,
        refineFaceLandmarks: true,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
    });
}

// extract_keypoints.js
function extractKeypoints(results) {
    // Helper to flatten arrays
    function flatten(arr) {
        return arr.reduce((acc, val) => acc.concat(val), []);
    }

    // Pose: 33 landmarks, each with x, y, z, visibility
    let pose = results.pose_landmarks
        ? flatten(results.pose_landmarks.map(res => [res.x, res.y, res.z, res.visibility]))
        : Array(33 * 4).fill(0);

    // Face: 468 landmarks, each with x, y, z
    let face = results.face_landmarks
        ? flatten(results.face_landmarks.map(res => [res.x, res.y, res.z]))
        : Array(468 * 3).fill(0);

    // Left hand: 21 landmarks, each with x, y, z
    let lh = results.left_hand_landmarks
        ? flatten(results.left_hand_landmarks.map(res => [res.x, res.y, res.z]))
        : Array(21 * 3).fill(0);

    // Right hand: 21 landmarks, each with x, y, z
    let rh = results.right_hand_landmarks
        ? flatten(results.right_hand_landmarks.map(res => [res.x, res.y, res.z]))
        : Array(21 * 3).fill(0);

    // Concatenate all arrays
    return pose.concat(face, lh, rh);
}

async function processFrame() {
    if (!collecting) return;
    if (!video || video.readyState < 2) return;

    await holistic.send({ image: video });

    // Push the full holistic results (or a deep copy if needed)
    let res = extractKeypoints(holisticResults ? { ...holisticResults } : {});
    frameDataArray.push(res);
    // console.log(res);
    if (frameDataArray.length >= 30) {
        $.ajax({
            url: '/api/model/predict/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ frames: frameDataArray }),
            success: function (response) {
                console.log('Data sent successfully:', response);
            },
            error: function (error) {
                console.error('Error sending data:', error);
            }
        });
        frameDataArray = [];
    }
    requestAnimationFrame(processFrame);
}

function mediapipeInit() {
    const mediapipe_template = `<div class="container-fluid" id="main-content">
    <div class="row">
      <div class="col-sm-12">
        <h1>Welcome to SLRPS</h1>
        <p>This is a simple Main page for managing SLRPS.</p>
      </div>
    </div>
    <div class="row justify-content-center align-items-center g-2 column-gap-3">
      <div class="col-md-6 col-sm-12">
        <h3>Recognition</h3>
        <div class="d-flex flex-column  justify-content-center align-items-center shadow-sm">
          <video id="video" class="img-fluid rounded z-1 w-75" autoplay style="transform: scaleX(-1);"></video>

          <div class="row d-flex justify-content-between align-items-center g-2 w-100 mt-2 ">
            <div class="col d-flex justify-content-center">
              <button id="start-recording" class="btn btn-success">Start Recording</button>
            </div>

            <div class="col d-flex justify-content-center">
              <button id="stop-recording" class="btn btn-danger" disabled>Stop Recording</button>
            </div>
          </div>
        </div>
        <p id="recognized-text" class="mt-3"></p>


      </div>

      <div class="col-sm-4 overflow-y-auto d-flex flex-column justify-content-start border rounded p-3 gap-2 "
        style="min-height: 40vh; max-height: 60vh;">
        <p class="fs-3">Results</p>
        <div class="card bg-light">
          <h4 class="text-capitalize">hi </h4>
        </div>
      </div>


    </div>

    <p id="recognized-text" class="mt-3">

    </p>
    <!-- <img src="/static/img/pngwing.com (1).png" alt="presentation"
                class="img-fluid rounded w-25 position-absolute bottom-0 end-0 z-n1 bg-opacity-10"> -->

  </div>`;
    $('main').html(mediapipe_template);

    setupMediapipe();

    video = document.getElementById('video');
    navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
        video.srcObject = stream;
        video.play();
    });

    const startButton = document.getElementById('start-recording');
    const stopButton = document.getElementById('stop-recording');

    document.getElementById('start-recording').onclick = () => {
        console.log('Recording started');
        collecting = true;
        startButton.disabled = true;
        stopButton.disabled = false;
        frameDataArray = [];
        requestAnimationFrame(processFrame);
    };
    document.getElementById('stop-recording').onclick = () => {
        collecting = false;
        startButton.disabled = false;
        stopButton.disabled = true;
        console.log('Recording stopped');
    };
}

window.mediapipeInit = mediapipeInit;

export { mediapipeInit, setupMediapipe, processFrame, handLandmarker, poseLandmarker };