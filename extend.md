# Sign Language Web Project Documentation

## Table of Contents

1. Introduction
2. Objective
3. Features
4. Technology Stack
5. System Architecture
6. Modules
7. Setup Instructions
8. Usage
9. Testing and Validation
10. Challenges Faced
11. Future Enhancements
12. Conclusion

---

## 1. Introduction

The **Sign Language Web** project is a web-based application designed to bridge the communication gap between individuals who use sign language and those who do not. This project leverages modern technologies like Mediapipe and machine learning to recognize gestures and convert them into text or speech. It aims to make communication more inclusive and accessible for everyone.

This project is developed as part of a final-year academic requirement by a team of four contributors:
- Vijay K (711620104024)
- Raghul P (711620104015)
- Vignesh G (711620104322)
- Karthikeyan J (711620104010)

---

## 2. Objective

The primary objective of this project is to create an accessible platform that:

- Recognizes sign language gestures in real-time.
- Converts gestures into text or speech for effective communication.
- Provides a user-friendly interface for both gesture-to-text and text-to-gesture functionalities.
- Promotes inclusivity by enabling communication between sign language users and non-users.

---

## 3. Features

1. **Gesture Recognition**: Real-time recognition of hand and body gestures using Mediapipe.
2. **Text-to-Gesture Conversion**: Converts text or speech into corresponding gestures.
3. **Audio Output**: Provides audio feedback for recognized gestures.
4. **Multilingual Support**: Allows users to select different languages for translation.
5. **Interactive UI**: A responsive and intuitive user interface for seamless interaction.
6. **Authentication**: Secure user authentication using Firebase.
7. **Error Handling**: Custom error pages for 403, 404, and 500 errors.

---

## 4. Technology Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Python (Flask Framework)
- **Libraries**:
  - Mediapipe (Holistic, Drawing Utils, Camera Utils)
  - jQuery for AJAX requests
- **Database**: Firebase (for authentication and data storage)
- **Other Tools**: 
  - JSON for configuration
  - Excel for data management

---

## 5. System Architecture

The system is divided into the following components:

1. **Frontend**: Handles user interaction and displays results.
2. **Backend**: Processes requests, manages gesture recognition, and handles API calls.
3. **Mediapipe Integration**: Performs gesture recognition using Mediapipe's Holistic model.
4. **Database**: Stores user data and configurations.
5. **Error Handling**: Manages application errors and provides user-friendly feedback.

---

## 6. Modules

### 1. Gesture Recognition
- **File**: `src/static/js/mediapipe.js`
- **Description**: Implements Mediapipe's Holistic model to detect hand and body gestures.

### 2. User Interface
- **Files**:
  - `src/templates/to_text.html`
  - `src/templates/to_gesture.html`
- **Description**: Provides pages for gesture-to-text and text-to-gesture functionalities.

### 3. API Integration
- **Description**: Fetches language options and processes translations via AJAX.

### 4. Audio Output
- **File**: `src/static/js/mediapipe.js`
- **Description**: Converts recognized gestures into audio using Base64-encoded audio data.

### 5. Authentication
- **File**: `src/static/js/login-auth.js`
- **Description**: Manages user login and authentication using Firebase.

### 6. Error Handling
- **Files**:
  - `src/templates/errors/403.html`
  - `src/templates/errors/404.html`
  - `src/templates/errors/500.html`
- **Description**: Provides custom error pages for different HTTP errors.

---

## 7. Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd Sign_language_web
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up Firebase authentication by adding `firebase-auth.json` to the project root.
5. Run the application:
   ```bash
   python app.py
   ```
6. Access the application at `http://localhost:5000`.

---

## 8. Usage

1. **Gesture to Text/Speech**:
   - Navigate to the "Gesture to Text/Speech" page.
   - Start the camera and perform gestures.
   - View the recognized text or listen to the audio output.

2. **Text/Speech to Gesture**:
   - Navigate to the "Text/Speech to Gesture" page.
   - Enter text or speech input.
   - View the corresponding gesture animation.

3. **Clear Results**:
   - Use the "Clear Results" button to reset the output.

---

## 9. Testing and Validation

### Testing
- Unit tests were conducted for each module to ensure functionality.
- Integration tests verified the seamless interaction between modules.

### Validation
- The application was tested with various gestures to ensure accuracy.
- User feedback was collected to improve usability.

---

## 10. Challenges Faced

1. **Gesture Recognition Accuracy**: Ensuring accurate recognition of gestures in different lighting conditions and backgrounds.
2. **Real-Time Processing**: Optimizing the application to process gestures in real-time without significant delays.
3. **Multilingual Support**: Implementing accurate translations for multiple languages.
4. **User Authentication**: Integrating Firebase authentication securely and efficiently.

---

## 11. Future Enhancements

1. **Mobile App Integration**: Develop a mobile version of the application.
2. **Advanced Gesture Recognition**: Incorporate more complex gestures and facial expressions.
3. **Offline Mode**: Enable offline gesture recognition using pre-trained models.
4. **Expanded Language Support**: Add support for more languages and dialects.
5. **AI-Powered Suggestions**: Use AI to suggest corrections for unrecognized gestures.

---

## 12. Conclusion

The **Sign Language Web** project is a step toward making communication more inclusive and accessible. By leveraging cutting-edge technologies, this application provides a platform for seamless interaction between sign language users and non-users. With future enhancements, it has the potential to become a comprehensive solution for sign language translation.