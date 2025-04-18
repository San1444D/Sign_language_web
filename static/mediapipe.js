import * as vision from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js";

// Setup webcam
const video = document.getElementById('video');
navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
    video.play();
});


const startButton = document.getElementById('start-recording');
const stopButton = document.getElementById('stop-recording');


// Setup Mediapipe
let handLandmarker, poseLandmarker, frameDataArray = [], collecting = false;

async function setupMediapipe() {
    const fileset = await vision.FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.7/wasm"
    );
    handLandmarker = await vision.HandLandmarker.createFromOptions(fileset, {
        baseOptions: { modelAssetPath: "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task" },
        runningMode: "VIDEO",
        numHands: 2
    });
    poseLandmarker = await vision.PoseLandmarker.createFromOptions(fileset, {
        baseOptions: { modelAssetPath: "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task" },
        runningMode: "VIDEO",
        numPoses: 1
    });
}
setupMediapipe();

async function processFrame() {
    if (!collecting) return;
    if (video.readyState < 2) return;
    const now = performance.now();
    const handResult = handLandmarker.detectForVideo(video, now);
    const poseResult = poseLandmarker.detectForVideo(video, now);
    frameDataArray.push({
        hands: handResult?.landmarks || [],
        pose: poseResult?.landmarks || []
    });
    if (frameDataArray.length >= 30) {
        // Send to server
        $.ajax({
            url: '/api/model/predict',
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
        // console.log('Sending data to server:', frameDataArray);
        // Reset the array after sending
        frameDataArray = [];
    }
    requestAnimationFrame(processFrame);
}

// Button handlers
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