# tts_runner.py
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# --- IBM TTS setup ---
API_KEY = "Qkhw_mmE9bPpKDPQui52K8Loz4M76KNz9JZNh9ry013p"
URL = "https://api.eu-de.text-to-speech.watson.cloud.ibm.com"

authenticator = IAMAuthenticator(API_KEY)
tts_service = TextToSpeechV1(authenticator=authenticator)
tts_service.set_service_url(URL)

# English voice options
ENGLISH_VOICES = {
    # US English - Standard
    "allison": "en-US_AllisonV3Voice",
    "lisa": "en-US_LisaV3Voice", 
    "michael": "en-US_MichaelV3Voice",
    "kevin": "en-US_KevinV3Voice",
    "henry": "en-US_HenryV3Voice",
    "emily": "en-US_EmilyV3Voice",
    
    # US English - Expressive (supports emotions)
    "allison_expressive": "en-US_AllisonExpressive",
    "emma_expressive": "en-US_EmmaExpressive",
    "lisa_expressive": "en-US_LisaExpressive",
    "michael_expressive": "en-US_MichaelExpressive",
    
    # British English
    "kate_british": "en-GB_KateV3Voice",
    "charlotte_british": "en-GB_CharlotteV3Voice",
    "james_british": "en-GB_JamesV3Voice",
    
    # Australian English
    "heidi_australian": "en-AU_HeidiExpressive",
    "jack_australian": "en-AU_JackExpressive",
}

# Emotion mapping to SSML expressions
EMOTION_MAPPING = {
    'ANGRY': 'angry',
    'DISGUST': 'disgusted',
    'FEAR': 'afraid',
    'HAPPY': 'cheerful',
    'JOY': 'cheerful',
    'SAD': 'sad',
    'SURPRISE': 'surprised',
    'NEUTRAL': 'neutral',
    'EXCITED': 'excited',
    'CALM': 'calm'
}

def generate_tts(
    emotion_objects,
    output_file="output_audio.mp3",
    voice_name="allison_expressive",  # Use friendly voice name
):
    """
    Convert text with emotions to speech and save as a single audio file.
    
    Args:
        emotion_objects: List of dicts containing 'speech_text' and 'emotion' keys.
        output_file: Path to save the audio file.
        voice_name: Voice name from ENGLISH_VOICES keys (default: allison_expressive).
    
    Returns:
        Path to the saved audio file.
    """
    
    # Get actual voice ID from friendly name
    voice = ENGLISH_VOICES.get(voice_name, "en-US_AllisonExpressive")
    is_expressive = "Expressive" in voice
    
    print(f"Using voice: {voice_name} ({voice})")
    
    if is_expressive:
        # Build SSML with emotions for expressive voices
        ssml_parts = ['<speak>']
        
        for obj in emotion_objects:
            text = obj["speech_text"]
            emotion = obj.get("emotion", "NEUTRAL").upper()
            
            # Map emotion to SSML expression
            ssml_emotion = EMOTION_MAPPING.get(emotion, "neutral")
            
            # Wrap text with emotion expression
            ssml_part = f'<express-as type="{ssml_emotion}">{text}</express-as>'
            
            # Add pause between sentences
            ssml_part += '<break time="0.5s"/>'
            
            ssml_parts.append(ssml_part)
        
        ssml_parts.append('</speak>')
        synthesis_text = ''.join(ssml_parts)
        
        print(f"Generated SSML: {synthesis_text[:200]}...")  # Debug print
        
    else:
        # Use simple text concatenation for standard voices
        synthesis_text = ". ".join([obj["speech_text"] for obj in emotion_objects])
        print(f"Using standard voice - no emotion support")
    
    try:
        # Generate audio
        response = tts_service.synthesize(
            synthesis_text,
            voice=voice,
            accept="audio/mp3"
        ).get_result()
        
        with open(output_file, "wb") as audio_file:
            audio_file.write(response.content)
            
    except Exception as e:
        print(f"Error with {voice_name} voice, falling back to basic synthesis: {e}")
        
        # Fallback: use basic voice without emotions
        combined_text = ". ".join([obj["speech_text"] for obj in emotion_objects])
        response = tts_service.synthesize(
            combined_text,
            voice="en-US_AllisonV3Voice",
            accept="audio/mp3"
        ).get_result()
        
        with open(output_file, "wb") as audio_file:
            audio_file.write(response.content)

    print(f"Audio saved as {output_file}")
    return output_file

def list_available_voices():
    """Display all available English voice options."""
    print("Available English Voices:")
    print("\n🇺🇸 US English (Standard):")
    for key, voice in ENGLISH_VOICES.items():
        if "en-US" in voice and "Expressive" not in voice:
            gender = "Female" if any(name in voice for name in ["Allison", "Lisa", "Emily"]) else "Male"
            print(f"  • {key}: {gender} voice")
    
    print("\n🎭 US English (Expressive - Supports Emotions):")
    for key, voice in ENGLISH_VOICES.items():
        if "en-US" in voice and "Expressive" in voice:
            gender = "Female" if any(name in voice for name in ["Allison", "Emma", "Lisa"]) else "Male"
            print(f"  • {key}: {gender} voice with emotion support")
    
    print("\n🇬🇧 British English:")
    for key, voice in ENGLISH_VOICES.items():
        if "en-GB" in voice:
            gender = "Female" if any(name in voice for name in ["Kate", "Charlotte"]) else "Male"
            print(f"  • {key}: {gender} British accent")
    
    print("\n🇦🇺 Australian English:")
    for key, voice in ENGLISH_VOICES.items():
        if "en-AU" in voice:
            gender = "Female" if "Heidi" in voice else "Male"
            print(f"  • {key}: {gender} Australian accent with emotions")

# Usage examples:
"""
# Use default expressive voice
generate_tts(emotion_objects, "story1.mp3")

# Use specific voice
generate_tts(emotion_objects, "story2.mp3", voice_name="michael_expressive")

# Use British accent
generate_tts(emotion_objects, "story3.mp3", voice_name="james_british")

# List all available voices
list_available_voices()
"""