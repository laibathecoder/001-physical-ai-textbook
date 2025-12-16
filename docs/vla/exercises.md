---
sidebar_position: 3
title: VLA Integration Exercises - Verify Student Understanding
---

# VLA Integration Exercises - Verify Student Understanding

## Exercise 1: Setting Up Whisper for Robot Voice Commands

### Objective
Install and configure OpenAI Whisper for voice command processing on a humanoid robot platform.

### Tasks
1. Install Whisper and required dependencies
2. Set up audio input pipeline for robot
3. Configure Whisper model for real-time processing
4. Test basic transcription capabilities
5. Integrate with ROS 2 audio topics

### Expected Outcome
- Understanding of Whisper installation and configuration
- Ability to set up audio pipeline for robot environments
- Knowledge of real-time transcription challenges
- Integration with ROS 2 communication framework

### Solution Steps
```bash
# Install Whisper and dependencies
pip install openai-whisper
pip install pyaudio
pip install scipy
pip install librosa

# Install system dependencies for audio processing
sudo apt-get install portaudio19-dev  # For PyAudio
sudo apt-get install ffmpeg          # For audio format conversion
```

```python
# Example Whisper setup for robot
import whisper
import torch
import pyaudio
import numpy as np

def setup_whisper_robot():
    """Setup Whisper model optimized for robot voice commands"""

    # Select appropriate model size based on robot computational resources
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_size = "base"  # Good balance of accuracy and speed

    print(f"Loading Whisper {model_size} model on {device}...")
    model = whisper.load_model(model_size, device=device)

    return model

def setup_audio_stream():
    """Setup audio stream for robot microphone"""
    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024
    )

    return audio, stream

# Example usage
model = setup_whisper_robot()
audio, stream = setup_audio_stream()

# Test transcription
sample_audio = np.zeros(16000, dtype=np.float32)  # 1 second of silence
result = model.transcribe(sample_audio)
print("Test transcription:", result["text"])
```

### Assessment Questions
1. What are the trade-offs between different Whisper model sizes for robot applications?
2. How does audio preprocessing improve Whisper performance in robot environments?
3. What computational resources are required for real-time Whisper processing on robots?

## Exercise 2: Voice Command Recognition Pipeline

### Objective
Create a complete voice command recognition pipeline that processes audio and maps to robot actions.

### Tasks
1. Implement audio preprocessing pipeline
2. Create voice activity detection
3. Integrate Whisper transcription
4. Map recognized commands to robot actions
5. Implement error handling and feedback

### Expected Outcome
- Understanding of complete voice command pipeline
- Ability to recognize and classify voice commands
- Knowledge of command mapping and execution
- Error handling for misrecognitions

### Solution Steps
```python
import asyncio
import threading
import queue
from dataclasses import dataclass
from typing import Callable, Dict, Any


@dataclass
class VoiceCommand:
    """Represents a recognized voice command"""
    text: str
    confidence: float
    timestamp: float
    action_mapping: str = None


class VoiceCommandRecognizer:
    """Complete voice command recognition pipeline"""

    def __init__(self, whisper_model, command_mappings: Dict[str, Callable]):
        self.model = whisper_model
        self.command_mappings = command_mappings
        self.audio_queue = queue.Queue()
        self.command_queue = queue.Queue()

        # Voice activity detection parameters
        self.energy_threshold = 0.01
        self.silence_duration = 1.0  # seconds
        self.min_speech_duration = 0.5  # seconds

        # Processing threads
        self.recognition_thread = threading.Thread(target=self._process_audio, daemon=True)
        self.command_thread = threading.Thread(target=self._execute_commands, daemon=True)

        self.running = False

    def start(self):
        """Start voice command recognition"""
        self.running = True
        self.recognition_thread.start()
        self.command_thread.start()
        print("Voice command recognizer started")

    def stop(self):
        """Stop voice command recognition"""
        self.running = False
        self.recognition_thread.join(timeout=2.0)
        self.command_thread.join(timeout=2.0)
        print("Voice command recognizer stopped")

    def _process_audio(self):
        """Continuously process audio for voice commands"""
        buffer = np.array([])
        recording_start_time = None

        while self.running:
            try:
                # Get audio chunk from queue
                if not self.audio_queue.empty():
                    audio_chunk = self.audio_queue.get_nowait()

                    # Check for speech
                    energy = np.mean(audio_chunk ** 2)
                    has_speech = energy > self.energy_threshold

                    if has_speech:
                        # Add to buffer if speech detected
                        buffer = np.concatenate([buffer, audio_chunk])

                        # Mark start time if not already recording
                        if recording_start_time is None:
                            recording_start_time = time.time()
                    else:
                        # Check if we have accumulated speech to process
                        if (len(buffer) > 0 and
                            time.time() - recording_start_time > self.min_speech_duration):

                            # Process accumulated speech
                            self._transcribe_audio(buffer.copy())
                            buffer = np.array([])
                            recording_start_time = None
                        elif len(buffer) > 0:
                            # Add silence to buffer until timeout
                            buffer = np.concatenate([buffer, audio_chunk])

                            if len(buffer) / 16000.0 > 5.0:  # 5 second timeout
                                self._transcribe_audio(buffer.copy())
                                buffer = np.array([])
                                recording_start_time = None
                else:
                    time.sleep(0.01)  # Small delay to prevent busy waiting
            except Exception as e:
                print(f"Error in audio processing: {e}")
                time.sleep(0.1)

    def _transcribe_audio(self, audio_data):
        """Transcribe audio using Whisper"""
        try:
            # Transcribe audio
            result = self.model.transcribe(
                audio_data,
                fp16=torch.cuda.is_available(),
                language='en'  # Specify language for better accuracy
            )

            text = result['text'].strip()
            confidence = result.get('avg_logprob', -1.0)  # Use log probability as confidence

            if text and confidence > -1.0:  # Only process if confidence is reasonable
                command = VoiceCommand(
                    text=text,
                    confidence=confidence,
                    timestamp=time.time()
                )

                # Find matching command
                action_mapping = self._match_command(text)
                command.action_mapping = action_mapping

                # Add to command queue for execution
                self.command_queue.put(command)

        except Exception as e:
            print(f"Error in transcription: {e}")

    def _match_command(self, text: str) -> str:
        """Match text to available commands"""
        text_lower = text.lower()

        # Simple fuzzy matching using difflib
        import difflib

        possible_commands = list(self.command_mappings.keys())
        matches = difflib.get_close_matches(
            text_lower,
            possible_commands,
            n=1,
            cutoff=0.6
        )

        return matches[0] if matches else None

    def _execute_commands(self):
        """Execute recognized commands"""
        while self.running:
            try:
                if not self.command_queue.empty():
                    command = self.command_queue.get_nowait()

                    if command.action_mapping:
                        print(f"Executing command: {command.text} -> {command.action_mapping}")
                        # Execute the mapped command
                        self.command_mappings[command.action_mapping]()
                    else:
                        print(f"Unknown command: {command.text}")
                        self._handle_unknown_command(command.text)
                else:
                    time.sleep(0.1)
            except Exception as e:
                print(f"Error in command execution: {e}")
                time.sleep(0.1)

    def _handle_unknown_command(self, command_text: str):
        """Handle unrecognized commands"""
        print(f"Unknown command received: {command_text}")
        # Could implement asking for clarification or providing help


# Example usage
def move_forward():
    print("Moving robot forward")

def turn_left():
    print("Turning robot left")

def pick_up_object():
    print("Attempting to pick up object")

# Command mappings
commands = {
    "move forward": move_forward,
    "go forward": move_forward,
    "move left": turn_left,
    "turn left": turn_left,
    "pick up": pick_up_object,
    "grab object": pick_up_object
}

recognizer = VoiceCommandRecognizer(whisper_model, commands)
recognizer.start()

# Add audio to queue (in real implementation, this would come from microphone)
# recognizer.audio_queue.put(audio_data)

# Stop when done
# recognizer.stop()
```

### Assessment Questions
1. How does voice activity detection improve the efficiency of voice command processing?
2. What techniques can be used to improve command recognition accuracy?
3. How do you handle ambiguous or unclear voice commands?

## Exercise 3: Vision-Language Integration

### Objective
Implement a system that combines visual perception with language understanding for object manipulation.

### Tasks
1. Set up object detection pipeline
2. Integrate with language understanding
3. Create spatial reasoning capabilities
4. Implement referring expression comprehension
5. Test object manipulation commands

### Expected Outcome
- Understanding of vision-language fusion
- Ability to connect language references to visual objects
- Knowledge of spatial reasoning for robotics
- Implementation of referring expression understanding

### Solution Steps
```python
import cv2
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from torchvision import transforms
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class DetectedObject:
    """Represents a detected object with spatial information"""
    name: str
    bbox: Tuple[int, int, int, int]  # x, y, width, height
    confidence: float
    center: Tuple[float, float]  # x, y center coordinates
    distance: float = None  # Distance if depth available


class VisionLanguageFusion:
    """Fuses visual perception with language understanding"""

    def __init__(self):
        # Load object detection model (e.g., YOLO or Detectron2)
        self.detector = self._load_detector()

        # Load language model for understanding spatial references
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.lang_model = AutoModel.from_pretrained('bert-base-uncased')

        # Spatial reference understanding
        self.spatial_keywords = {
            'left': ['left', 'left side', 'on the left'],
            'right': ['right', 'right side', 'on the right'],
            'front': ['front', 'in front', 'ahead'],
            'back': ['back', 'behind', 'rear'],
            'near': ['near', 'close', 'next to'],
            'far': ['far', 'distant', 'away from']
        }

    def _load_detector(self):
        """Load object detection model"""
        # In practice, this would load a model like YOLOv5, Detectron2, etc.
        # For this example, we'll create a mock detector
        class MockDetector:
            def detect(self, image):
                # Mock detection - return some objects
                height, width = image.shape[:2]
                objects = [
                    DetectedObject(
                        name='cup',
                        bbox=(int(width * 0.3), int(height * 0.4), 50, 50),
                        confidence=0.85,
                        center=(width * 0.3 + 25, height * 0.4 + 25)
                    ),
                    DetectedObject(
                        name='book',
                        bbox=(int(width * 0.6), int(height * 0.3), 60, 80),
                        confidence=0.78,
                        center=(width * 0.6 + 30, height * 0.3 + 40)
                    )
                ]
                return objects

        return MockDetector()

    def process_scene(self, image, command_text):
        """Process visual scene with language command"""
        # Detect objects in the scene
        detected_objects = self.detector.detect(image)

        # Parse the command to understand spatial references
        target_object = self._parse_command_for_target(command_text, detected_objects)

        return detected_objects, target_object

    def _parse_command_for_target(self, command_text: str, objects: List[DetectedObject]) -> DetectedObject:
        """Parse command to identify target object"""
        command_lower = command_text.lower()

        # Look for object names in command
        object_names = [obj.name for obj in objects]

        # Find potential target objects based on command
        potential_targets = []
        for obj in objects:
            if obj.name in command_lower:
                # Calculate relevance based on spatial relations
                relevance_score = self._calculate_relevance(obj, command_lower)
                potential_targets.append((obj, relevance_score))

        # Sort by relevance and return most likely target
        if potential_targets:
            potential_targets.sort(key=lambda x: x[1], reverse=True)
            return potential_targets[0][0]

        return None

    def _calculate_relevance(self, obj: DetectedObject, command: str) -> float:
        """Calculate relevance of object to command based on spatial relations"""
        relevance = 0.0

        # Check for spatial keywords in command
        for direction, keywords in self.spatial_keywords.items():
            for keyword in keywords:
                if keyword in command:
                    # Calculate spatial relevance based on object position
                    relevance += self._spatial_relevance(obj, direction, command)

        # Add confidence as base relevance
        relevance += obj.confidence

        return relevance

    def _spatial_relevance(self, obj: DetectedObject, direction: str, command: str) -> float:
        """Calculate spatial relevance based on object position"""
        # This is a simplified example - in practice, this would be more sophisticated
        x_center, y_center = obj.center
        image_width, image_height = 640, 480  # Assuming 640x480 image

        if direction == 'left':
            return 1.0 if x_center < image_width / 2 else 0.0
        elif direction == 'right':
            return 1.0 if x_center > image_width / 2 else 0.0
        elif direction == 'front':
            return 1.0 if y_center < image_height / 2 else 0.0
        elif direction == 'back':
            return 1.0 if y_center > image_height / 2 else 0.0
        elif direction == 'near':
            # Assuming closer to center is "near"
            center_dist = np.sqrt((x_center - image_width/2)**2 + (y_center - image_height/2)**2)
            return max(0.0, 1.0 - center_dist / (image_width/2))
        else:
            return 0.0


# Example usage
fusion = VisionLanguageFusion()

# In a real application, this would come from robot's camera
mock_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

command = "pick up the red cup on the left"
detected_objects, target_object = fusion.process_scene(mock_image, command)

print(f"Detected objects: {[obj.name for obj in detected_objects]}")
if target_object:
    print(f"Target object: {target_object.name} at {target_object.center}")
else:
    print("No target object identified")
```

### Assessment Questions
1. How does spatial reasoning improve object manipulation in robotics?
2. What challenges arise when connecting language references to visual objects?
3. How can vision-language fusion be made robust to ambiguity?

## Exercise 4: Action Generation from VLA Understanding

### Objective
Implement action generation system that translates VLA understanding into robot control commands.

### Tasks
1. Create action space definition
2. Map VLA understanding to robot actions
3. Implement action sequence planning
4. Add safety checks and validation
5. Test with sample VLA inputs

### Expected Outcome
- Understanding of action generation from VLA inputs
- Ability to map high-level commands to low-level actions
- Knowledge of action sequencing and planning
- Implementation of safety and validation checks

### Solution Steps
```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
import math


class ActionType(Enum):
    """Types of robot actions"""
    NAVIGATE_TO = "navigate_to"
    GRASP_OBJECT = "grasp_object"
    RELEASE_OBJECT = "release_object"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    MOVE_FORWARD = "move_forward"
    MOVE_BACKWARD = "move_backward"
    LOOK_AT = "look_at"
    SPEAK = "speak"


@dataclass
class RobotAction:
    """Represents a robot action"""
    action_type: ActionType
    parameters: dict
    priority: int = 1
    safety_level: int = 1  # 1-5 scale, 5 being most critical safety


@dataclass
class ActionSequence:
    """Sequence of actions to execute"""
    actions: List[RobotAction]
    confidence: float
    description: str


class VLAActionGenerator:
    """Generates robot actions from VLA understanding"""

    def __init__(self):
        self.action_templates = {
            'navigate_to': self._create_navigate_action,
            'grasp_object': self._create_grasp_action,
            'move': self._create_move_action,
            'turn': self._create_turn_action,
            'speak': self._create_speak_action
        }

    def generate_actions(self, command_text: str, target_object: DetectedObject = None) -> ActionSequence:
        """Generate action sequence from command and target object"""
        # Parse command to determine action type
        parsed_command = self._parse_command(command_text)

        actions = []

        if parsed_command['action_type'] == 'navigate_to':
            if target_object:
                # Navigate to target object
                navigate_action = self._create_navigate_action(
                    target_object.center[0],
                    target_object.center[1],
                    target_object.name
                )
                actions.append(navigate_action)

        elif parsed_command['action_type'] == 'grasp_object':
            if target_object:
                # Navigate to object, then grasp
                navigate_action = self._create_navigate_action(
                    target_object.center[0],
                    target_object.center[1],
                    target_object.name
                )
                grasp_action = self._create_grasp_action(target_object.name)

                actions.extend([navigate_action, grasp_action])

        elif parsed_command['action_type'] == 'move':
            move_action = self._create_move_action(parsed_command['direction'])
            actions.append(move_action)

        elif parsed_command['action_type'] == 'turn':
            turn_action = self._create_turn_action(parsed_command['direction'])
            actions.append(turn_action)

        # Add safety validation
        validated_actions = self._validate_actions(actions)

        return ActionSequence(
            actions=validated_actions,
            confidence=parsed_command.get('confidence', 0.8),
            description=f"Generated from: {command_text}"
        )

    def _parse_command(self, command_text: str) -> dict:
        """Parse command text to determine action type and parameters"""
        command_lower = command_text.lower()

        # Simple parsing - in practice, this would use more sophisticated NLP
        if any(word in command_lower for word in ['go to', 'navigate to', 'move to', 'walk to']):
            return {
                'action_type': 'navigate_to',
                'confidence': 0.9
            }
        elif any(word in command_lower for word in ['pick up', 'grasp', 'take', 'grab']):
            return {
                'action_type': 'grasp_object',
                'confidence': 0.85
            }
        elif any(word in command_lower for word in ['move', 'go', 'forward', 'backward']):
            direction = self._extract_direction(command_lower)
            return {
                'action_type': 'move',
                'direction': direction,
                'confidence': 0.8
            }
        elif any(word in command_lower for word in ['turn', 'rotate', 'left', 'right']):
            direction = self._extract_direction(command_lower)
            return {
                'action_type': 'turn',
                'direction': direction,
                'confidence': 0.8
            }
        else:
            return {
                'action_type': 'unknown',
                'confidence': 0.3
            }

    def _extract_direction(self, command: str) -> str:
        """Extract direction from command"""
        if any(word in command for word in ['forward', 'ahead', 'straight']):
            return 'forward'
        elif any(word in command for word in ['backward', 'back', 'reverse']):
            return 'backward'
        elif any(word in command for word in ['left', 'counter-clockwise']):
            return 'left'
        elif any(word in command for word in ['right', 'clockwise']):
            return 'right'
        else:
            return 'forward'  # default

    def _create_navigate_action(self, x: float, y: float, target_name: str) -> RobotAction:
        """Create navigation action"""
        return RobotAction(
            action_type=ActionType.NAVIGATE_TO,
            parameters={
                'x': x,
                'y': y,
                'target_name': target_name,
                'approach_distance': 0.5  # meters
            },
            priority=2,
            safety_level=3
        )

    def _create_grasp_action(self, object_name: str) -> RobotAction:
        """Create grasp action"""
        return RobotAction(
            action_type=ActionType.GRASP_OBJECT,
            parameters={
                'object_name': object_name,
                'grasp_type': 'top_grasp',  # or 'side_grasp', etc.
                'force_limit': 10.0  # Newtons
            },
            priority=3,
            safety_level=4
        )

    def _create_move_action(self, direction: str) -> RobotAction:
        """Create movement action"""
        distance = 1.0  # meters

        if direction == 'forward':
            vx, vy = 0.5, 0.0
        elif direction == 'backward':
            vx, vy = -0.5, 0.0
        else:
            vx, vy = 0.0, 0.0

        return RobotAction(
            action_type=ActionType.MOVE_FORWARD if direction == 'forward' else ActionType.MOVE_BACKWARD,
            parameters={
                'linear_velocity_x': vx,
                'linear_velocity_y': vy,
                'duration': distance / 0.5  # time to move at 0.5 m/s
            },
            priority=1,
            safety_level=2
        )

    def _create_turn_action(self, direction: str) -> RobotAction:
        """Create turn action"""
        angular_velocity = 0.5  # rad/s
        angle = math.pi / 2  # 90 degrees

        if direction == 'left':
            wz = angular_velocity
        elif direction == 'right':
            wz = -angular_velocity
        else:
            wz = 0.0

        return RobotAction(
            action_type=ActionType.TURN_LEFT if direction == 'left' else ActionType.TURN_RIGHT,
            parameters={
                'angular_velocity_z': wz,
                'angle': angle if abs(wz) > 0 else 0.0,
                'duration': angle / angular_velocity if abs(wz) > 0 else 0.0
            },
            priority=1,
            safety_level=2
        )

    def _validate_actions(self, actions: List[RobotAction]) -> List[RobotAction]:
        """Validate actions for safety and feasibility"""
        validated_actions = []

        for action in actions:
            # Check safety constraints
            if self._is_safe_action(action):
                validated_actions.append(action)
            else:
                print(f"Action {action.action_type} failed safety check, skipping")

        return validated_actions

    def _is_safe_action(self, action: RobotAction) -> bool:
        """Check if action is safe to execute"""
        # Basic safety checks
        if action.action_type == ActionType.GRASP_OBJECT:
            # Check force limits
            if action.parameters.get('force_limit', 0) > 50:  # Newtons
                return False

        # Check movement parameters
        if action.action_type in [ActionType.MOVE_FORWARD, ActionType.MOVE_BACKWARD]:
            velocity = action.parameters.get('linear_velocity_x', 0)
            if abs(velocity) > 1.0:  # m/s - too fast
                return False

        if action.action_type in [ActionType.TURN_LEFT, ActionType.TURN_RIGHT]:
            velocity = action.parameters.get('angular_velocity_z', 0)
            if abs(velocity) > 1.0:  # rad/s - too fast
                return False

        return True


# Example usage
generator = VLAActionGenerator()

# Example 1: Navigate to object
target_obj = DetectedObject(
    name='red cup',
    bbox=(100, 100, 50, 50),
    confidence=0.9,
    center=(125, 125)
)

actions_seq = generator.generate_actions("navigate to the red cup", target_obj)
print(f"Generated {len(actions_seq.actions)} actions for navigation:")
for action in actions_seq.actions:
    print(f"  - {action.action_type.value}: {action.parameters}")


# Example 2: Grasp object
actions_seq = generator.generate_actions("pick up the red cup", target_obj)
print(f"\nGenerated {len(actions_seq.actions)} actions for grasping:")
for action in actions_seq.actions:
    print(f"  - {action.action_type.value}: {action.parameters}")
```

### Assessment Questions
1. How do you ensure safety when translating high-level commands to low-level actions?
2. What validation checks are important for action generation?
3. How can action sequences be optimized for efficiency?

## Exercise 5: Complete VLA Integration Pipeline

### Objective
Implement a complete VLA pipeline that integrates vision, language, and action components.

### Tasks
1. Integrate all VLA components
2. Implement real-time processing loop
3. Add feedback and error handling
4. Create user interaction interface
5. Test complete pipeline with sample commands

### Expected Outcome
- Understanding of complete VLA system integration
- Ability to process real-time VLA inputs
- Knowledge of feedback and error handling
- Complete working VLA system

### Solution Steps
```python
import asyncio
import threading
from queue import Queue
import time
from typing import Optional


class VLAPipeline:
    """Complete Vision-Language-Action pipeline"""

    def __init__(self):
        # Initialize components
        self.vision_fusion = VisionLanguageFusion()
        self.action_generator = VLAActionGenerator()
        self.voice_recognizer = None  # Would be connected to Whisper system

        # Queues for data flow
        self.vision_queue = Queue(maxsize=10)
        self.command_queue = Queue(maxsize=10)
        self.action_queue = Queue(maxsize=10)

        # Processing threads
        self.vision_thread = None
        self.command_thread = None
        self.action_thread = None

        self.running = False
        self.current_target_object = None

    def start_pipeline(self):
        """Start the complete VLA pipeline"""
        self.running = True

        # Start processing threads
        self.vision_thread = threading.Thread(target=self._process_vision, daemon=True)
        self.command_thread = threading.Thread(target=self._process_commands, daemon=True)
        self.action_thread = threading.Thread(target=self._execute_actions, daemon=True)

        self.vision_thread.start()
        self.command_thread.start()
        self.action_thread.start()

        print("VLA Pipeline started")

    def stop_pipeline(self):
        """Stop the VLA pipeline"""
        self.running = False

        if self.vision_thread:
            self.vision_thread.join(timeout=2.0)
        if self.command_thread:
            self.command_thread.join(timeout=2.0)
        if self.action_thread:
            self.action_thread.join(timeout=2.0)

        print("VLA Pipeline stopped")

    def _process_vision(self):
        """Process visual input and update scene understanding"""
        while self.running:
            try:
                if not self.vision_queue.empty():
                    # Get latest image (discard older ones)
                    while self.vision_queue.qsize() > 1:
                        self.vision_queue.get_nowait()

                    image = self.vision_queue.get_nowait()

                    # Process scene with current command context
                    if not self.command_queue.empty():
                        # Use latest command for context
                        while self.command_queue.qsize() > 1:
                            self.command_queue.get_nowait()

                        command = self.command_queue.get_nowait()

                        # Process scene with command context
                        detected_objects, target_object = self.vision_fusion.process_scene(
                            image, command
                        )

                        if target_object:
                            self.current_target_object = target_object
                            print(f"Target object identified: {target_object.name}")

                    time.sleep(0.01)  # Small delay
                else:
                    time.sleep(0.05)  # Longer delay if no vision data
            except Exception as e:
                print(f"Error in vision processing: {e}")
                time.sleep(0.1)

    def _process_commands(self):
        """Process voice commands and generate actions"""
        while self.running:
            try:
                if not self.command_queue.empty():
                    command = self.command_queue.get_nowait()

                    # Generate actions based on current target object
                    action_sequence = self.action_generator.generate_actions(
                        command, self.current_target_object
                    )

                    # Add actions to execution queue
                    for action in action_sequence.actions:
                        self.action_queue.put(action)

                    print(f"Generated {len(action_sequence.actions)} actions for: {command}")

                    time.sleep(0.01)  # Small delay
                else:
                    time.sleep(0.05)  # Longer delay if no commands
            except Exception as e:
                print(f"Error in command processing: {e}")
                time.sleep(0.1)

    def _execute_actions(self):
        """Execute robot actions"""
        while self.running:
            try:
                if not self.action_queue.empty():
                    action = self.action_queue.get_nowait()

                    # Execute action (in real system, this would interface with robot)
                    self._execute_robot_action(action)

                    time.sleep(0.01)  # Small delay
                else:
                    time.sleep(0.05)  # Longer delay if no actions
            except Exception as e:
                print(f"Error in action execution: {e}")
                time.sleep(0.1)

    def _execute_robot_action(self, action: RobotAction):
        """Execute robot action (mock implementation)"""
        print(f"Executing {action.action_type.value} with parameters: {action.parameters}")

        # In real implementation, this would send commands to robot
        # via ROS 2 or other communication protocol
        if action.action_type == ActionType.NAVIGATE_TO:
            x, y = action.parameters['x'], action.parameters['y']
            print(f"  Navigating to ({x}, {y}) for {action.parameters['target_name']}")
        elif action.action_type == ActionType.GRASP_OBJECT:
            obj_name = action.parameters['object_name']
            print(f"  Grasping {obj_name}")
        elif action.action_type in [ActionType.MOVE_FORWARD, ActionType.MOVE_BACKWARD]:
            vel = action.parameters['linear_velocity_x']
            print(f"  Moving with velocity {vel} m/s")
        elif action.action_type in [ActionType.TURN_LEFT, ActionType.TURN_RIGHT]:
            vel = action.parameters['angular_velocity_z']
            print(f"  Turning with angular velocity {vel} rad/s")

    def add_vision_data(self, image):
        """Add vision data to processing queue"""
        if not self.vision_queue.full():
            self.vision_queue.put(image)

    def add_command(self, command_text: str):
        """Add voice command to processing queue"""
        if not self.command_queue.full():
            self.command_queue.put(command_text)


# Example usage
vla_pipeline = VLAPipeline()
vla_pipeline.start_pipeline()

# Simulate adding data to pipeline
import numpy as np

# Simulate camera data
mock_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
vla_pipeline.add_vision_data(mock_image)

# Simulate voice command
vla_pipeline.add_command("pick up the red cup on the left")

# Let it run briefly
time.sleep(2)

# Stop pipeline
vla_pipeline.stop_pipeline()
```

### Assessment Questions
1. How do you handle timing and synchronization in real-time VLA systems?
2. What feedback mechanisms are important for VLA systems?
3. How can you improve the robustness of complete VLA pipelines?

## Exercise 6: Isaac Integration with VLA

### Objective
Integrate VLA system with Isaac Sim and Isaac ROS for humanoid robot control.

### Tasks
1. Connect VLA to Isaac Sim environment
2. Implement Isaac ROS interfaces
3. Test perception-action loop
4. Validate in simulation environment
5. Document integration patterns

### Expected Outcome
- Understanding of Isaac integration with VLA systems
- Ability to connect VLA to simulation
- Knowledge of Isaac ROS interfaces
- Validated integration in simulation

### Solution Steps
```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped, Twist
from std_msgs.msg import String
from vision_msgs.msg import Detection2DArray
import cv2
from cv_bridge import CvBridge
import numpy as np


class IsaacVLANode(Node):
    """
    VLA system integrated with Isaac Sim and ROS
    """

    def __init__(self):
        super().__init__('isaac_vla_node')

        # Initialize components
        self.vision_fusion = VisionLanguageFusion()
        self.action_generator = VLAActionGenerator()
        self.cv_bridge = CvBridge()

        # Current scene state
        self.latest_image = None
        self.latest_detections = None
        self.current_command = None

        # Subscribers
        self.image_sub = self.create_subscription(
            Image,
            '/camera/rgb/image_rect_color',
            self.image_callback,
            10
        )

        self.detection_sub = self.create_subscription(
            Detection2DArray,
            '/isaac_ros/detections',
            self.detection_callback,
            10
        )

        self.command_sub = self.create_subscription(
            String,
            '/voice_command',
            self.command_callback,
            10
        )

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.goal_pub = self.create_publisher(PoseStamped, '/goal_pose', 10)
        self.response_pub = self.create_publisher(String, '/vla_response', 10)

        # Timer for processing loop
        self.process_timer = self.create_timer(0.1, self.process_vla_cycle)

        self.get_logger().info('Isaac VLA Node initialized')

    def image_callback(self, msg):
        """Handle incoming camera images"""
        try:
            self.latest_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'Error converting image: {e}')

    def detection_callback(self, msg):
        """Handle incoming object detections"""
        self.latest_detections = msg

    def command_callback(self, msg):
        """Handle incoming voice commands"""
        self.current_command = msg.data
        self.get_logger().info(f'Received command: {msg.data}')

    def process_vla_cycle(self):
        """Main VLA processing cycle"""
        if self.latest_image is not None and self.current_command is not None:
            try:
                # Process scene with current command
                detected_objects, target_object = self.vision_fusion.process_scene(
                    self.latest_image,
                    self.current_command
                )

                # Generate actions
                action_sequence = self.action_generator.generate_actions(
                    self.current_command,
                    target_object
                )

                # Execute actions
                for action in action_sequence.actions:
                    self.execute_isaac_action(action)

                # Clear current command after processing
                self.current_command = None

                # Publish response
                response_msg = String()
                response_msg.data = f"Processed: {action_sequence.description}"
                self.response_pub.publish(response_msg)

            except Exception as e:
                self.get_logger().error(f'Error in VLA cycle: {e}')

    def execute_isaac_action(self, action: RobotAction):
        """Execute action in Isaac environment"""
        if action.action_type == ActionType.NAVIGATE_TO:
            # Create goal pose for navigation
            goal_pose = PoseStamped()
            goal_pose.header.stamp = self.get_clock().now().to_msg()
            goal_pose.header.frame_id = 'map'

            # Convert screen coordinates to world coordinates
            # This would require camera calibration and depth information
            goal_pose.pose.position.x = action.parameters['x'] / 100.0  # Scale appropriately
            goal_pose.pose.position.y = action.parameters['y'] / 100.0
            goal_pose.pose.position.z = 0.0

            # Set orientation (face toward target)
            self.goal_pub.publish(goal_pose)

        elif action.action_type == ActionType.MOVE_FORWARD:
            cmd = Twist()
            cmd.linear.x = action.parameters.get('linear_velocity_x', 0.5)
            self.cmd_vel_pub.publish(cmd)

        elif action.action_type == ActionType.TURN_LEFT:
            cmd = Twist()
            cmd.angular.z = action.parameters.get('angular_velocity_z', 0.5)
            self.cmd_vel_pub.publish(cmd)

        elif action.action_type == ActionType.TURN_RIGHT:
            cmd = Twist()
            cmd.angular.z = action.parameters.get('angular_velocity_z', -0.5)
            self.cmd_vel_pub.publish(cmd)

        self.get_logger().info(f'Executed action: {action.action_type.value}')


def main(args=None):
    """Main function to run Isaac VLA node"""
    rclpy.init(args=args)
    node = IsaacVLANode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down Isaac VLA Node...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Assessment Questions
1. How does Isaac Sim enhance VLA system development and testing?
2. What are the advantages of using Isaac ROS for VLA integration?
3. How do you validate VLA performance in simulation before real-world deployment?

## Advanced Assessment Questions

### Theoretical Understanding
1. Explain the architecture of a complete VLA system for humanoid robotics.
2. Analyze the challenges of real-time processing in VLA systems.
3. Compare different approaches to vision-language fusion in robotics.

### Practical Application
4. Design a VLA system for a specific humanoid robot task (e.g., serving drinks).
5. Implement error recovery mechanisms for VLA misinterpretations.
6. Create a validation framework for VLA system performance.

### Problem-Solving
7. Troubleshoot a scenario where VLA system misinterprets spatial references.
8. Optimize VLA system performance for real-time operation on robot hardware.
9. Adapt VLA system for multi-language support in international environments.