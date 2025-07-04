const controls = window;
const mpHolistic = window;
const drawingUtils = window;
const holistic = new Holistic({
    locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`;
    }
});
const videoElement = document.getElementsByClassName('input_video')[0];
const canvasElement = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElement.getContext('2d');

holistic.setOptions({
  modelComplexity: 1,
  smoothLandmarks: true,
  enableSegmentation: false,
  refineFaceLandmarks: true,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.5
});

// function removeLandmarks(results) {
//     if (results.poseLandmarks) {
//         removeElements(results.poseLandmarks, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16, 17, 18, 19, 20, 21, 22]);
//     }
// }
// function connect(ctx, connectors) {
//     const canvas = ctx.canvas;
//     for (const connector of connectors) {
//         const from = connector[0];
//         const to = connector[1];
//         if (from && to) {
//             if (from.visibility && to.visibility &&
//                 (from.visibility < 0.1 || to.visibility < 0.1)) {
//                 continue;
//             }
//             ctx.beginPath();
//             ctx.moveTo(from.x * canvas.width, from.y * canvas.height);
//             ctx.lineTo(to.x * canvas.width, to.y * canvas.height);
//             ctx.stroke();
//         }
//     }
// }
// let activeEffect = 'mask';
// function onResults(results) {
//     // Hide the spinner.
//     document.body.classList.add('loaded');
//     // Remove landmarks we don't want to draw.
//     removeLandmarks(results);
//     // Update the frame rate.
//     fpsControl.tick();
//     // Draw the overlays.
//     canvasCtx.save();
//     canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
//     if (results.segmentationMask) {
//         canvasCtx.drawImage(results.segmentationMask, 0, 0, canvasElement.width, canvasElement.height);
//         // Only overwrite existing pixels.
//         if (activeEffect === 'mask' || activeEffect === 'both') {
//             canvasCtx.globalCompositeOperation = 'source-in';
//             // This can be a color or a texture or whatever...
//             canvasCtx.fillStyle = '#00FF007F';
//             canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);
//         }
//         else {
//             canvasCtx.globalCompositeOperation = 'source-out';
//             canvasCtx.fillStyle = '#0000FF7F';
//             canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);
//         }
//         // Only overwrite missing pixels.
//         canvasCtx.globalCompositeOperation = 'destination-atop';
//         canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
//         canvasCtx.globalCompositeOperation = 'source-over';
//     }
//     else {
//         canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
//     }
//     // Connect elbows to hands. Do this first so that the other graphics will draw
//     // on top of these marks.
//     canvasCtx.lineWidth = 5;
//     if (results.poseLandmarks) {
//         if (results.rightHandLandmarks) {
//             canvasCtx.strokeStyle = 'white';
//             connect(canvasCtx, [[
//                 results.poseLandmarks[mpHolistic.POSE_LANDMARKS.RIGHT_ELBOW],
//                 results.rightHandLandmarks[0]
//             ]]);
//         }
//         if (results.leftHandLandmarks) {
//             canvasCtx.strokeStyle = 'white';
//             connect(canvasCtx, [[
//                 results.poseLandmarks[mpHolistic.POSE_LANDMARKS.LEFT_ELBOW],
//                 results.leftHandLandmarks[0]
//             ]]);
//         }
//     }
//     // Pose...
//     drawingUtils.drawConnectors(canvasCtx, results.poseLandmarks, mpHolistic.POSE_CONNECTIONS, { color: 'white' });
//     drawingUtils.drawLandmarks(canvasCtx, Object.values(mpHolistic.POSE_LANDMARKS_LEFT)
//         .map(index => results.poseLandmarks[index]), { visibilityMin: 0.65, color: 'white', fillColor: 'rgb(255,138,0)' });
//     drawingUtils.drawLandmarks(canvasCtx, Object.values(mpHolistic.POSE_LANDMARKS_RIGHT)
//         .map(index => results.poseLandmarks[index]), { visibilityMin: 0.65, color: 'white', fillColor: 'rgb(0,217,231)' });
//     // Hands...
//     drawingUtils.drawConnectors(canvasCtx, results.rightHandLandmarks, mpHolistic.HAND_CONNECTIONS, { color: 'white' });
//     drawingUtils.drawLandmarks(canvasCtx, results.rightHandLandmarks, {
//         color: 'white',
//         fillColor: 'rgb(0,217,231)',
//         lineWidth: 2,
//         radius: (data) => {
//             return drawingUtils.lerp(data.from.z, -0.15, .1, 10, 1);
//         }
//     });
//     drawingUtils.drawConnectors(canvasCtx, results.leftHandLandmarks, mpHolistic.HAND_CONNECTIONS, { color: 'white' });
//     drawingUtils.drawLandmarks(canvasCtx, results.leftHandLandmarks, {
//         color: 'white',
//         fillColor: 'rgb(255,138,0)',
//         lineWidth: 2,
//         radius: (data) => {
//             return drawingUtils.lerp(data.from.z, -0.15, .1, 10, 1);
//         }
//     });
//     // Face...
//     drawingUtils.drawConnectors(canvasCtx, results.faceLandmarks, mpHolistic.FACEMESH_TESSELATION, { color: '#C0C0C070', lineWidth: 1 });
//     drawingUtils.drawConnectors(canvasCtx, results.faceLandmarks, mpHolistic.FACEMESH_RIGHT_EYE, { color: 'rgb(0,217,231)' });
//     drawingUtils.drawConnectors(canvasCtx, results.faceLandmarks, mpHolistic.FACEMESH_RIGHT_EYEBROW, { color: 'rgb(0,217,231)' });
//     drawingUtils.drawConnectors(canvasCtx, results.faceLandmarks, mpHolistic.FACEMESH_LEFT_EYE, { color: 'rgb(255,138,0)' });
//     drawingUtils.drawConnectors(canvasCtx, results.faceLandmarks, mpHolistic.FACEMESH_LEFT_EYEBROW, { color: 'rgb(255,138,0)' });
//     drawingUtils.drawConnectors(canvasCtx, results.faceLandmarks, mpHolistic.FACEMESH_FACE_OVAL, { color: '#E0E0E0', lineWidth: 5 });
//     drawingUtils.drawConnectors(canvasCtx, results.faceLandmarks, mpHolistic.FACEMESH_LIPS, { color: '#E0E0E0', lineWidth: 5 });
//     canvasCtx.restore();
// }

holistic.onResults(onResults);


function onResults(results) {
    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    canvasCtx.drawImage(
        results.image, 0, 0, canvasElement.width, canvasElement.height);
  
    // Pose...
    drawingUtils.drawConnectors(canvasCtx, results.poseLandmarks, mpHolistic.POSE_CONNECTIONS, { color: 'white' });
    drawingUtils.drawLandmarks(canvasCtx, Object.values(mpHolistic.POSE_LANDMARKS_LEFT)
        .map(index => results.poseLandmarks[index]), { visibilityMin: 0.65, color: 'white', fillColor: 'rgb(255,138,0)' });
    drawingUtils.drawLandmarks(canvasCtx, Object.values(mpHolistic.POSE_LANDMARKS_RIGHT)
        .map(index => results.poseLandmarks[index]), { visibilityMin: 0.65, color: 'white', fillColor: 'rgb(0,217,231)' });
    // Hands...
    drawingUtils.drawConnectors(canvasCtx, results.rightHandLandmarks, mpHolistic.HAND_CONNECTIONS, { color: 'white' });
    drawingUtils.drawLandmarks(canvasCtx, results.rightHandLandmarks, {
        color: 'white',
        fillColor: 'rgb(0,217,231)',
        lineWidth: 2,
        radius: (data) => {
            return drawingUtils.lerp(data.from.z, -0.15, .1, 10, 1);
        }
    });
    drawingUtils.drawConnectors(canvasCtx, results.leftHandLandmarks, mpHolistic.HAND_CONNECTIONS, { color: 'white' });
    drawingUtils.drawLandmarks(canvasCtx, results.leftHandLandmarks, {
        color: 'white',
        fillColor: 'rgb(255,138,0)',
        lineWidth: 2,
        radius: (data) => {
            return drawingUtils.lerp(data.from.z, -0.15, .1, 10, 1);
        }
    });
    // Face...
    drawingUtils.drawConnectors(canvasCtx, results.faceLandmarks, mpHolistic.FACEMESH_TESSELATION, { color: '#C0C0C070', lineWidth: 1 });
    drawingUtils.drawConnectors(canvasCtx, results.faceLandmarks, mpHolistic.FACEMESH_RIGHT_EYE, { color: 'rgb(0,217,231)' });
    drawingUtils.drawConnectors(canvasCtx, results.faceLandmarks, mpHolistic.FACEMESH_RIGHT_EYEBROW, { color: 'rgb(0,217,231)' });
    drawingUtils.drawConnectors(canvasCtx, results.faceLandmarks, mpHolistic.FACEMESH_LEFT_EYE, { color: 'rgb(255,138,0)' });
    drawingUtils.drawConnectors(canvasCtx, results.faceLandmarks, mpHolistic.FACEMESH_LEFT_EYEBROW, { color: 'rgb(255,138,0)' });
    drawingUtils.drawConnectors(canvasCtx, results.faceLandmarks, mpHolistic.FACEMESH_FACE_OVAL, { color: '#E0E0E0', lineWidth: 5 });
    drawingUtils.drawConnectors(canvasCtx, results.faceLandmarks, mpHolistic.FACEMESH_LIPS, { color: '#E0E0E0', lineWidth: 5 });
    canvasCtx.restore();
  }
  
  const camera = new Camera(videoElement, {
    onFrame: async () => {
      await holistic.send({image: videoElement});
    },
    width: 640,
    height: 480
  });
  camera.start();
  