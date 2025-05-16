// main.js
let holistic, holisticResults = null;
let video = null;
let canvas = null, ctx = null;
let frameDataArray = [];
let collecting = false;
let result_temp = null;
let audioPlayer = new Audio();

// Initialize Mediapipe Holistic
async function setupMediapipe() {
  holistic = new Holistic({
    locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`,
  });

  holistic.setOptions({
    modelComplexity: 1,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5,
    smoothLandmarks: true,
    refineFaceLandmarks: true,
  });

  holistic.onResults(results => {
    holisticResults = results;
  });
}

// Flatten keypoints for frame sending
function extractKeypoints(results) {
  const flatten = (arr) => arr.reduce((acc, val) => acc.concat(val), []);

  const pose = results.poseLandmarks
    ? flatten(results.poseLandmarks.slice(0, 33).map(lm => [lm.x, lm.y, lm.z, lm.visibility]))
    : Array(33 * 4).fill(0);  // 132

  const face = results.faceLandmarks
    ? flatten(results.faceLandmarks.slice(0, 468).map(lm => [lm.x, lm.y, lm.z]))
    : Array(468 * 3).fill(0);  // 1404

  const leftHand = results.leftHandLandmarks
    ? flatten(results.leftHandLandmarks.map(lm => [lm.x, lm.y, lm.z]))
    : Array(21 * 3).fill(0);  // 63

  const rightHand = results.rightHandLandmarks
    ? flatten(results.rightHandLandmarks.map(lm => [lm.x, lm.y, lm.z]))
    : Array(21 * 3).fill(0);  // 63

  return pose.concat(face, leftHand, rightHand); // Total: 1662
}

// Utility function to add sleep functionality
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Drawing functions
function drawConnectors(ctx, landmarks, connections, color = 'white', lineWidth = 2) {
  for (const [startIdx, endIdx] of connections) {
    const start = landmarks[startIdx];
    const end = landmarks[endIdx];
    if (start && end) {
      ctx.beginPath();
      ctx.moveTo(start.x * canvas.width, start.y * canvas.height);
      ctx.lineTo(end.x * canvas.width, end.y * canvas.height);
      ctx.strokeStyle = color;
      ctx.lineWidth = lineWidth;
      ctx.stroke();
    }
  }
}

function drawLandmarks(ctx, landmarks, color = 'red', radius = 3) {
  for (const landmark of landmarks) {
    ctx.beginPath();
    ctx.arc(landmark.x * canvas.width, landmark.y * canvas.height, radius, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();
  }
}

function drawResults(results) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (!results) return;

  if (results.poseLandmarks) {
    drawConnectors(ctx, results.poseLandmarks, PoseConnections, 'white', 4);
    drawLandmarks(ctx, results.poseLandmarks, 'cyan', 4);
  }
  if (results.leftHandLandmarks) {
    drawConnectors(ctx, results.leftHandLandmarks, HandConnections, 'yellow', 3);
    drawLandmarks(ctx, results.leftHandLandmarks, 'yellow');
  }
  if (results.rightHandLandmarks) {
    drawConnectors(ctx, results.rightHandLandmarks, HandConnections, 'green', 3);
    drawLandmarks(ctx, results.rightHandLandmarks, 'green');
  }
  if (results.faceLandmarks) {
    drawLandmarks(ctx, results.faceLandmarks, 'pink', 1);
  }
}

// Define simple Pose/Hand connections (minimal, for now)
const PoseConnections = [
  [11, 13], [13, 15], [12, 14], [14, 16], // arms
  [11, 12], [23, 24], [23, 25], [24, 26], // torso
  [25, 27], [26, 28], [27, 29], [28, 30]  // legs
];
const HandConnections = [
  [0, 1], [1, 2], [2, 3], [3, 4], // Thumb
  [0, 5], [5, 6], [6, 7], [7, 8], // Index
  [0, 9], [9, 10], [10, 11], [11, 12], // Middle
  [0, 13], [13, 14], [14, 15], [15, 16], // Ring
  [0, 17], [17, 18], [18, 19], [19, 20] // Pinky
];

// Frame processing loop
async function processFrame() {
  if (!collecting) return;
  if (!video || video.readyState < 2) return;

  await holistic.send({ image: video });

  drawResults(holisticResults);

  let res = extractKeypoints(holisticResults || {});
  frameDataArray.push(res);

  if (frameDataArray.length >= 30) {
    sendFrames(frameDataArray);
    frameDataArray = [];
  }

  requestAnimationFrame(processFrame);
}

// Send frames to server
function sendFrames(frames) {
  let sp = $('#speech-switch').is(':checked');
  console.log('Sending frames:', frames, 'Speech:', sp);

  $.ajax({
    url: '/api/model/predict/',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({ frames: frames, speech_request: sp, target_language: $('#language-select').val() }),
    success: (response) => {
      console.log('Response:', response);
      if (response.result) {
        displayResult(response);
      } else {
        console.error('No result in response:', response);
      }
    },
    error: (xhr, status, error) => {
      console.error('Error:', error);
    }
  });
}

// Display the prediction result
function displayResult(response) {
  if (result_temp === response.result) return;
  result_temp = response.result;

  const card = `
    <div class="card">
      <h4 class="text-capitalize ps-2">${response.result}</h4>
    </div>`;

  $('#results').prepend(card);

  if (response.audio_b64) {
    playAudio(response.audio_b64);
  }
}

// Play audio response
async function playAudio(base64) {
  audioPlayer.src = 'data:audio/mpeg;base64,' + base64;
  audioPlayer.volume = 1;
  await audioPlayer.play();
}

// Initialize everything
async function mediapipeInit() {
  console.log('mediapipeInit called');

  await setupMediapipe();

  video = document.getElementById('video');
  canvas = document.getElementById('output');
  ctx = canvas.getContext('2d');

  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      video.srcObject = stream;
      video.style.transform = 'scaleX(-1)'; // Mirror the video

      video.play();
    });

  video.style.transform = 'scaleX(-1)'; // Mirror the video

  document.getElementById('start-recording').onclick = () => {
    collecting = true;
    $('#start-recording').prop('disabled', true);
    $('#stop-recording').prop('disabled', false);
    frameDataArray = [];
    requestAnimationFrame(processFrame);
    console.log('Recording started');
  };

  document.getElementById('stop-recording').onclick = () => {
    collecting = false;
    $('#start-recording').prop('disabled', false);
    $('#stop-recording').prop('disabled', true);
    console.log('Recording stopped');
  };
}

// Expose to window
window.mediapipeInit = mediapipeInit;


export { mediapipeInit, setupMediapipe };