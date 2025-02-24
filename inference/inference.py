from net import ImprovedBirdNet
import os
import json
import logging
from datetime import datetime
import torch
import librosa
import numpy as np
from pathlib import Path
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('inference/inference_logs.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BirdSoundInference:
    def __init__(self, model_path, data_folder='data', node_id=1):
        self.node_id = node_id
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.data_folder = Path(data_folder)
        self.inference_count_file = "inference/inference_count.txt"
        self.inference_log_file = "inference/inference_history.json"
        self.model_path = model_path
        
        # Load model and associated data
        self.load_model()
        self.initialize_inference_count()
        self.processed_files = self.load_processed_files()

    def load_model(self):
        """Load the trained model and associated data"""
        try:
            self.class_names = ['greybackedcamaroptera', 'hartlaubsturaco', 'tropicalboubou']
            logger.info(f"Loaded {len(self.class_names)} classes: {self.class_names}")
            
            checkpoint = torch.load(self.model_path, map_location=self.device)

            # Initialize model
            # Assuming the input dimension from the first layer of the model
            input_dim = next(iter(checkpoint['model_state_dict'].items()))[1].shape[1]
            num_classes = len(self.class_names)
            
            self.model = ImprovedBirdNet(input_dim, num_classes).to(self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])

            # Initialize feature normalization parameters
            # For now, using identity normalization - you may want to save these during training
            self.feature_mean = torch.zeros(input_dim)
            self.feature_std = torch.ones(input_dim)
            
            self.model.eval()
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def initialize_inference_count(self):
        if os.path.exists(self.inference_count_file):
            with open(self.inference_count_file, 'r') as f:
                self.inference_count = int(f.read().strip())
        else:
            self.inference_count = 0
            self._save_inference_count()
    
    def _save_inference_count(self):
        with open(self.inference_count_file, 'w') as f:
            f.write(str(self.inference_count))

    def load_processed_files(self):
        if os.path.exists(self.inference_log_file):
            with open(self.inference_log_file, 'r') as f:
                log_data = json.load(f)
                return {entry['audio_path'] for entry in log_data}
        return set()

    def extract_features(self, audio_path, sr=22050, duration=5):
        """Extract features from audio file"""
        try:
            # Load and preprocess audio
            y, _ = librosa.load(audio_path, sr=sr, duration=duration)
            
            # Ensure consistent length
            target_length = int(sr * duration)
            if len(y) < target_length:
                y = np.pad(y, (0, target_length - len(y)))
            else:
                y = y[:target_length]
            
            # Extract features (same as training)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            spectral_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
            
            # Combine features
            features = np.concatenate([
                np.mean(mfccs, axis=1),
                np.std(mfccs, axis=1),
                np.mean(spectral_cent, axis=1),
                np.mean(chroma, axis=1),
                np.mean(spectral_contrast, axis=1)
            ])
            
            return features

        except Exception as e:
            logger.error(f"Error extracting features from {audio_path}: {str(e)}")
            raise

    def normalize_features(self, features):
        """Normalize features using saved mean and std"""
        features_tensor = torch.tensor(features, dtype=torch.float32)
        return (features_tensor - self.feature_mean) / (self.feature_std + 1e-8)

    def make_inference(self, audio_path):
        """Make inference on a single audio file"""
        try:
            # Extract and normalize features
            features = self.extract_features(audio_path)
            normalized_features = self.normalize_features(features)
            
            # Prepare for inference
            features_batch = normalized_features.unsqueeze(0).to(self.device)
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(features_batch)
                probabilities = torch.softmax(outputs, dim=1)
                predicted_idx = torch.argmax(outputs, dim=1).item()
                confidence = probabilities[0][predicted_idx].item()
            
            # Increment inference count
            self.inference_count += 1
            self._save_inference_count()
            
            # Prepare results
            result = {
                'inference_id': self.inference_count,
                'node_id': self.node_id,
                'species_name': self.class_names[predicted_idx],
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'audio_path': str(audio_path)
            }
            
            # Log inference
            self._log_inference(result)

            # Return client-facing results
            return {
                'inference_id': result['inference_id'],
                'node_id': result['node_id'],
                'species_name': result['species_name'],
                'time_of_collection': result['timestamp']
            }
        except Exception as e:
            logger.error(f"Error during inference: {str(e)}")
            raise
    
    def _log_inference(self, result):
        """Log inference results to JSON file"""
        try:
            log_data = []
            if os.path.exists(self.inference_log_file):
                with open(self.inference_log_file, 'r') as f:
                    log_data = json.load(f)
            log_data.append(result)
            with open(self.inference_log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
            logger.info(f"Inference logged: ID {result['inference_id']}, Species: {result['species_name']}")
        except Exception as e:
            logger.error(f"Error logging inference: {str(e)}")
            raise

    def process_new_files(self):
        audio_files = list(self.data_folder.glob("*.wav"))
        new_files = [f for f in audio_files if str(f) not in self.processed_files]
        
        if not new_files:
            logger.info("No new audio files found.")
            return
        
        logger.info(f"Found {len(new_files)} new audio files.")
        for file in new_files:
            try:
                result = self.make_inference(file)
                self.processed_files.add(str(file))
                logger.info(f"Processed {file}: {result}")
            except Exception as e:
                logger.error(f"Failed to process {file}: {str(e)}")

if __name__ == "__main__":
    model_path = "models/best_model.pth"
    inference_system = BirdSoundInference(model_path)
    inference_system.process_new_files()
