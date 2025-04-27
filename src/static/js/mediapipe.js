// import * as vision from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js";

// Setup Mediapipe
let handLandmarker, poseLandmarker, frameDataArray = [], collecting = false;
let holisticResults = null;
let video = null; // Make video accessible globally
let result_temp = null;

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
    // modelComplexity: 1,
    // smoothLandmarks: true,
    // enableSegmentation: false,
    // refineFaceLandmarks: true,
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
    let sp = false;
    if ($('#speech-switch').is(':checked')) {
      sp = true;
    }
    $.ajax({
      url: '/api/model/predict/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ frames: frameDataArray, speech_request: sp, target_language: $('#language-select').val() }),
      success: function (response) {
        console.log('Response:', response);
        if (response.result) {
          display_result(response);
        } else {
          console.error('No result in response:', response);
        }
      },
      error: function (xhr, status, error) {
        console.error('Error:', error);
      }
    });
    frameDataArray = [];
  }
  requestAnimationFrame(processFrame);
}

function mediapipeInit() {
  console.log('mediapipeInit called');
  setupMediapipe();

  video = document.getElementById('video');
  video.scaleX = -1; // Flip the video horizontally
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


function display_result(response) {
  if (result_temp == response.result) {
    return;
  }
  result_temp = response.result;
  const temp = `<div class="card bg-">
          <h4 class="text-capitalize ps-2">${response.result}</h4>
        </div>`;
  $('#results').prepend(temp);
  if (response.audio_b64) {
    const audio = new Audio('data:audio/mpeg;base64,' + response.audio_b64);
    audio.volume = 1;
    audio.play();
  }
}




window.mediapipeInit = mediapipeInit;

export { mediapipeInit, setupMediapipe, processFrame, handLandmarker, poseLandmarker };