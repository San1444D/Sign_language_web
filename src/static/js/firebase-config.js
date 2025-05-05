// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.6.0/firebase-analytics.js";
import {
  getAuth,
  GoogleAuthProvider
} from "https://www.gstatic.com/firebasejs/11.6.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/11.6.0/firebase-firestore.js";


// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCE_sr5UYylNA2X2syXLsfO8jjjQ8nd9rY",
  authDomain: "sign-language-project-b4eb8.firebaseapp.com",
  projectId: "sign-language-project-b4eb8",
  storageBucket: "sign-language-project-b4eb8.firebasestorage.app",
  messagingSenderId: "464226384961",
  appId: "1:464226384961:web:d86a771a6bdf2fe45edac0",
  measurementId: "G-BJYZLVP8SX"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

const db = getFirestore(app);

export { auth, provider, db, firebaseConfig };