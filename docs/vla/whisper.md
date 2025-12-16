---
sidebar_position: 2
title: Whisper Integration for Voice Commands
---

# Whisper Integration for Voice Commands

## Introduction to Voice Command Processing

Voice command processing enables natural human-robot interaction by allowing users to communicate with humanoid robots using spoken language. This capability is essential for creating intuitive and accessible robotic interfaces that don't require specialized knowledge or physical interaction with robot controls.

## Speech Recognition in Robotics

### Challenges in Robot Environments

Speech recognition in robotics faces unique challenges:
- **Acoustic Environment**: Robot environments often have background noise from motors, fans, and other equipment
- **Microphone Positioning**: Robot-mounted microphones may have different acoustic characteristics than desktop/laptop systems
- **Real-time Processing**: Need for low-latency response to maintain natural interaction
- **Robustness**: Must handle various accents, speaking styles, and environmental conditions

### OpenAI Whisper for Robotics

OpenAI's Whisper model offers several advantages for robotic applications:
- **Multilingual Support**: Handles multiple languages and accents
- **Robustness**: Performs well in noisy environments
- **Open Source**: Allows for customization and optimization
- **Offline Capability**: Can run without internet connection for privacy and reliability

## Whisper Architecture for Robots

### Model Variants

Whisper comes in different sizes optimized for different applications:

| Model | Size | Required Memory | Relative Speed | English-only | Multilingual |
|-------|------|----------------|----------------|--------------|--------------|
| tiny  | 75 MB | ~1 GB | ~32x | ✅ | ✅ |
| base  | 145 MB | ~1 GB | ~16x | ✅ | ✅ |
| small | 444 MB | ~2 GB | ~6x | ✅ | ✅ |
| medium | 769 MB | ~5 GB | ~2x | ✅ | ✅ |
| large | 1.55 GB | ~10 GB | 1x | ❌ | ✅ |

For humanoid robots, the choice depends on available computational resources and real-time requirements.

### Integration Architecture

The typical Whisper integration architecture for robotics includes:

```
Microphone Array → Audio Preprocessing → Whisper ASR → NLU → Command Execution
       ↓                    ↓                  ↓        ↓         ↓
   Noise Reduction    Audio Enhancement   Transcription  Intent  Robot Action
   Beamforming      Format Conversion    Confidence     Extraction  Execution
```

## Real-time Voice Command Processing

### Audio Pipeline

Setting up the audio processing pipeline:

```python
import pyaudio
import numpy as np
import threading
import queue
from scipy import signal
import whisper
import torch

class VoiceCommandProcessor:
    """
    Real-time voice command processor using Whisper for humanoid robots
    """

    def __init__(self, model_size='base', device='cuda' if torch.cuda.is_available() else 'cpu'):
        # Initialize Whisper model
        self.model = whisper.load_model(model_size, device=device)

        # Audio parameters
        self.sample_rate = 16000
        self.chunk_size = 1024  # Samples per chunk
        self.audio_queue = queue.Queue()

        # Voice activity detection parameters
        self.energy_threshold = 0.01
        self.silence_duration = 1.0  # Seconds of silence to trigger processing

        # Initialize audio stream
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        # Processing thread
        self.processing_thread = threading.Thread(target=self.process_audio, daemon=True)
        self.running = True
        self.processing_thread.start()

        print(f"Voice command processor initialized with Whisper {model_size}")

    def is_speech_detected(self, audio_chunk):
        """Detect if speech is present in the audio chunk"""
        energy = np.mean(audio_chunk ** 2)
        return energy > self.energy_threshold

    def process_audio(self):
        """Continuously process audio for voice commands"""
        buffer = np.array([])
        silence_counter = 0

        while self.running:
            # Read audio chunk
            data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            audio_chunk = np.frombuffer(data, dtype=np.float32)

            # Add to buffer if speech detected or buffer not empty
            if self.is_speech_detected(audio_chunk) or len(buffer) > 0:
                buffer = np.concatenate([buffer, audio_chunk])

                # Reset silence counter when speech detected
                if self.is_speech_detected(audio_chunk):
                    silence_counter = 0
                else:
                    silence_counter += self.chunk_size / self.sample_rate

            # Process if sufficient silence detected
            if silence_counter > self.silence_duration and len(buffer) > self.sample_rate * 0.5:
                # Process the accumulated speech
                self.transcribe_and_execute(buffer.copy())
                buffer = np.array([])  # Clear buffer
                silence_counter = 0

    def transcribe_and_execute(self, audio_data):
        """Transcribe audio and execute corresponding command"""
        try:
            # Convert audio to the format expected by Whisper
            audio_tensor = torch.from_numpy(audio_data).float()

            # Transcribe using Whisper
            result = self.model.transcribe(audio_tensor.numpy(), fp16=torch.cuda.is_available())
            transcription = result['text'].strip()

            if transcription:
                print(f"Transcribed: {transcription}")

                # Process the command
                self.execute_command(transcription)

        except Exception as e:
            print(f"Error processing audio: {e}")

    def execute_command(self, command_text):
        """Parse and execute voice command"""
        # Normalize the command text
        command = command_text.lower().strip()

        # Simple command parsing (in practice, use more sophisticated NLP)
        if 'move' in command or 'go' in command:
            if 'forward' in command:
                self.send_robot_command('move_forward')
            elif 'backward' in command or 'back' in command:
                self.send_robot_command('move_backward')
            elif 'left' in command:
                self.send_robot_command('turn_left')
            elif 'right' in command:
                self.send_robot_command('turn_right')
            else:
                print(f"Could not determine direction from command: {command}")

        elif 'grasp' in command or 'pick' in command or 'take' in command:
            self.send_robot_command('grasp_object')

        elif 'drop' in command or 'release' in command:
            self.send_robot_command('release_object')

        elif 'stop' in command or 'halt' in command:
            self.send_robot_command('stop_motion')

        elif 'dance' in command:
            self.send_robot_command('perform_dance')

        elif 'hello' in command or 'hi' in command:
            self.send_robot_command('greet_user')

        else:
            print(f"Unknown command: {command}")
            self.respond_to_unknown_command(command_text)

    def send_robot_command(self, command_type):
        """Send command to robot control system"""
        # In a real implementation, this would interface with the robot's
        # control system through ROS 2 or another communication protocol
        print(f"Executing robot command: {command_type}")

        # Example ROS 2 publisher (would be implemented in real system)
        # self.command_publisher.publish(RobotCommand(type=command_type))

    def respond_to_unknown_command(self, original_command):
        """Handle unrecognized commands"""
        print(f"Sorry, I didn't understand: '{original_command}'. Please try again.")

    def shutdown(self):
        """Clean shutdown of audio processing"""
        self.running = False
        self.processing_thread.join(timeout=2.0)
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        print("Voice command processor shutdown complete")


def main():
    """Example usage of the voice command processor"""
    processor = VoiceCommandProcessor(model_size='base')

    try:
        print("Voice command processor running. Say commands like 'move forward' or 'pick up object'")
        print("Press Ctrl+C to stop...")

        # Keep the main thread alive
        while True:
            import time
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down voice command processor...")
        processor.shutdown()


if __name__ == '__main__':
    main()
```

### ROS 2 Integration

Integrating Whisper with ROS 2 for robot command processing:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import AudioData
from geometry_msgs.msg import Twist
import whisper
import torch
import numpy as np


class WhisperVoiceNode(Node):
    """
    ROS 2 node for Whisper-based voice command processing
    """

    def __init__(self):
        super().__init__('whisper_voice_node')

        # Initialize Whisper model
        self.model = whisper.load_model('base')

        # Publishers and subscribers
        self.command_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.response_pub = self.create_publisher(String, '/voice_response', 10)
        self.audio_sub = self.create_subscription(
            AudioData, '/microphone/audio', self.audio_callback, 10
        )

        # Command mapping
        self.command_mapping = {
            'move forward': self.move_forward,
            'move backward': self.move_backward,
            'turn left': self.turn_left,
            'turn right': self.turn_right,
            'stop': self.stop_robot,
            'halt': self.stop_robot,
        }

        self.get_logger().info('Whisper Voice Command Node initialized')

    def audio_callback(self, msg):
        """Process incoming audio data"""
        try:
            # Convert audio data to numpy array
            audio_array = np.frombuffer(msg.data, dtype=np.int16).astype(np.float32)
            audio_array /= 32768.0  # Normalize to [-1, 1]

            # Transcribe using Whisper
            result = self.model.transcribe(audio_array, fp16=torch.cuda.is_available())
            transcription = result['text'].strip()

            if transcription:
                self.get_logger().info(f'Transcribed: {transcription}')
                self.process_command(transcription)

        except Exception as e:
            self.get_logger().error(f'Error processing audio: {e}')

    def process_command(self, command_text):
        """Process the transcribed command"""
        # Normalize command
        normalized_cmd = command_text.lower().strip()

        # Find closest matching command
        matched_cmd = self.find_closest_command(normalized_cmd)

        if matched_cmd:
            self.get_logger().info(f'Executing command: {matched_cmd}')
            self.command_mapping[matched_cmd]()

            # Publish response
            response_msg = String()
            response_msg.data = f'Executing: {matched_cmd}'
            self.response_pub.publish(response_msg)
        else:
            self.get_logger().warn(f'Unknown command: {command_text}')
            self.publish_error_response(f'Sorry, I did not understand: {command_text}')

    def find_closest_command(self, command_text):
        """Find the closest matching command using string similarity"""
        import difflib

        # Check for exact matches first
        if command_text in self.command_mapping:
            return command_text

        # Use difflib to find close matches
        matches = difflib.get_close_matches(
            command_text,
            self.command_mapping.keys(),
            n=1,
            cutoff=0.6  # 60% similarity threshold
        )

        return matches[0] if matches else None

    def move_forward(self):
        """Move robot forward"""
        cmd = Twist()
        cmd.linear.x = 0.5  # m/s
        self.command_pub.publish(cmd)

    def move_backward(self):
        """Move robot backward"""
        cmd = Twist()
        cmd.linear.x = -0.5  # m/s
        self.command_pub.publish(cmd)

    def turn_left(self):
        """Turn robot left"""
        cmd = Twist()
        cmd.angular.z = 0.5  # rad/s
        self.command_pub.publish(cmd)

    def turn_right(self):
        """Turn robot right"""
        cmd = Twist()
        cmd.angular.z = -0.5  # rad/s
        self.command_pub.publish(cmd)

    def stop_robot(self):
        """Stop robot motion"""
        cmd = Twist()
        # Zero velocities by default
        self.command_pub.publish(cmd)

    def publish_error_response(self, error_text):
        """Publish error response"""
        response_msg = String()
        response_msg.data = error_text
        self.response_pub.publish(response_msg)


def main(args=None):
    rclpy.init(args=args)
    node = WhisperVoiceNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down Whisper Voice Node...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Noise Reduction and Audio Enhancement

### Acoustic Challenges in Robotics

Robot environments present unique acoustic challenges:
- **Motor Noise**: DC motors, servos, and fans create continuous background noise
- **Mechanical Vibrations**: Movement causes vibrations that affect microphone signals
- **Echo and Reverberation**: Indoor environments create acoustic reflections
- **Variable Distance**: Speaker distance varies during interaction

### Audio Preprocessing Pipeline

```python
import numpy as np
from scipy import signal
import librosa


class AudioPreprocessor:
    """
    Audio preprocessing for robot environments
    """

    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.noise_profile = None
        self.noise_sample_count = 0

    def enhance_audio(self, audio_data):
        """Enhance audio quality for better ASR performance"""
        # Apply noise reduction
        denoised = self.reduce_noise(audio_data)

        # Apply normalization
        normalized = self.normalize_audio(denoised)

        # Apply bandpass filtering to focus on human speech frequencies
        filtered = self.bandpass_filter(normalized)

        return filtered

    def reduce_noise(self, audio_data):
        """Apply spectral subtraction for noise reduction"""
        if self.noise_profile is None:
            # If no noise profile, return original
            return audio_data

        # Apply Wiener filtering using noise profile
        stft = librosa.stft(audio_data)
        magnitude = np.abs(stft)
        phase = np.angle(stft)

        # Estimate clean signal magnitude using noise profile
        clean_magnitude = np.maximum(magnitude - self.noise_profile, 0)

        # Reconstruct signal
        clean_stft = clean_magnitude * np.exp(1j * phase)
        denoised = librosa.istft(clean_stft)

        return denoised.astype(audio_data.dtype)

    def normalize_audio(self, audio_data):
        """Normalize audio amplitude"""
        # Calculate RMS
        rms = np.sqrt(np.mean(audio_data ** 2))

        # Normalize to target RMS
        target_rms = 0.1  # Adjustable based on environment
        if rms > 0:
            gain = target_rms / rms
            # Apply soft limiting to prevent clipping
            normalized = np.tanh(audio_data * gain)
        else:
            normalized = audio_data

        return normalized

    def bandpass_filter(self, audio_data, low_freq=80, high_freq=8000):
        """Apply bandpass filter for human speech frequencies"""
        nyquist = self.sample_rate / 2
        low = low_freq / nyquist
        high = high_freq / nyquist

        # Design Butterworth bandpass filter
        b, a = signal.butter(4, [low, high], btype='band', fs=self.sample_rate)

        # Apply filter with zero-phase to avoid distortion
        filtered = signal.filtfilt(b, a, audio_data)

        return filtered

    def update_noise_profile(self, noise_sample):
        """Update noise profile for noise reduction"""
        # Compute STFT of noise sample
        stft = librosa.stft(noise_sample)
        magnitude = np.abs(stft)

        # Average across time dimension to get noise spectrum
        noise_spectrum = np.mean(magnitude, axis=1)

        # Update noise profile using exponential averaging
        if self.noise_profile is None:
            self.noise_profile = noise_spectrum
        else:
            alpha = 0.1  # Learning rate
            self.noise_profile = (1 - alpha) * self.noise_profile + alpha * noise_spectrum


# Example usage
preprocessor = AudioPreprocessor(sample_rate=16000)

# In a real application, you would continuously update the noise profile
# during quiet periods when the robot is not in use