import React, { useState, useRef, useEffect } from 'react';
import '../styles/VoiceInterface.css';

function VoiceInterface({ onTranscription }) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [response, setResponse] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const recognitionRef = useRef(null);
  const synthRef = useRef(null);

  const BACKEND_URL = 'http://localhost:5000';

  // Initialize Web Speech API
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert('Speech Recognition not supported in your browser. Use Chrome, Edge, or Safari.');
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    // When speech is recognized
    recognition.onresult = (event) => {
      let interimTranscript = '';
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;

        if (event.results[i].isFinal) {
          finalTranscript += transcript + ' ';
        } else {
          interimTranscript += transcript;
        }
      }

      if (finalTranscript) {
        setTranscript(finalTranscript.trim());
        handleVoiceInput(finalTranscript.trim());
      }
    };

    // Handle errors
    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current = recognition;
    synthRef.current = window.speechSynthesis;

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
    };
  }, []);

  // Start listening
  const startListening = () => {
    if (recognitionRef.current) {
      setIsListening(true);
      setTranscript('');
      recognitionRef.current.start();
    }
  };

  // Stop listening
  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  };

  // Handle voice input
  const handleVoiceInput = async (text) => {
    if (!text.trim()) return;

    setIsProcessing(true);

    try {
      console.log('Processing voice input:', text);

      // Send to backend
      const response = await fetch(`${BACKEND_URL}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          titles: extractJobTitles(text),
          location: extractLocation(text),
          salary_min: 50000,
          goals: text,
        }),
      });

      const data = await response.json();

      if (data.status === 'success') {
        const responseText = generateResponse(data);
        setResponse(responseText);

        // Speak the response
        if (synthRef.current) {
          speakResponse(responseText);
        }

        if (onTranscription) {
          onTranscription({
            input: text,
            output: responseText,
            results: data,
          });
        }
      }
    } catch (error) {
      console.error('Error processing voice input:', error);
      const errorMsg = 'Sorry, I encountered an error. Please try again.';
      setResponse(errorMsg);
      speakResponse(errorMsg);
    }

    setIsProcessing(false);
  };

  // Extract job titles from text
  const extractJobTitles = (text) => {
    const titles = [];
    const keywords = [
      'customer success',
      'implementation consultant',
      'project manager',
      'solutions consultant',
      'tech support',
      'onboarding',
    ];

    keywords.forEach((keyword) => {
      if (text.toLowerCase().includes(keyword)) {
        titles.push(keyword);
      }
    });

    return titles.length > 0 ? titles : ['Customer Success'];
  };

  // Extract location from text
  const extractLocation = (text) => {
    const locations = ['canada', 'remote', 'toronto', 'vancouver', 'calgary', 'montréal'];

    for (let location of locations) {
      if (text.toLowerCase().includes(location)) {
        return location.charAt(0).toUpperCase() + location.slice(1);
      }
    }

    return 'Canada';
  };

  // Generate response text
  const generateResponse = (data) => {
    const jobsFound = data.total_jobs || 0;
    const appsCount = data.total_applications || 0;

    if (jobsFound === 0) {
      return 'I did not find any matching jobs. Try different keywords or locations.';
    }

    return `Perfect! I found ${jobsFound} matching jobs and applied to ${appsCount} of them. The top opportunity is ${data.jobs?.[0]?.title} at ${data.jobs?.[0]?.company}. Would you like more details?`;
  };

  // Speak response using Text-to-Speech
  const speakResponse = (text) => {
    if (!synthRef.current) return;

    // Cancel any ongoing speech
    synthRef.current.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    synthRef.current.speak(utterance);
  };

  return (
    <div className="voice-interface">
      <div className="voice-container">
        {/* Microphone Button */}
        <div className="voice-button-container">
          <button
            className={`voice-button ${isListening ? 'listening' : ''} ${isProcessing ? 'processing' : ''}`}
            onClick={isListening ? stopListening : startListening}
            disabled={isProcessing}
            title={isListening ? 'Click to stop listening' : 'Click to start listening'}
          >
            {isListening ? (
              <>
                <span className="voice-icon">🎤</span>
                <span className="voice-status">Listening...</span>
              </>
            ) : isProcessing ? (
              <>
                <span className="voice-icon">⏳</span>
                <span className="voice-status">Processing...</span>
              </>
            ) : (
              <>
                <span className="voice-icon">🎤</span>
                <span className="voice-status">Click to Speak</span>
              </>
            )}
          </button>
        </div>

        {/* Transcript Display */}
        {transcript && (
          <div className="transcript">
            <p className="label">You said:</p>
            <p className="text">"{transcript}"</p>
          </div>
        )}

        {/* Response Display */}
        {response && (
          <div className="response">
            <p className="label">🤖 Agent Says:</p>
            <p className="text">"{response}"</p>
            <button className="replay-button" onClick={() => speakResponse(response)}>
              🔊 Replay
            </button>
          </div>
        )}

        {/* Voice Commands Help */}
        <div className="voice-help">
          <p className="help-title">💡 Try saying:</p>
          <ul className="help-list">
            <li>"Find customer success jobs in Canada"</li>
            <li>"Search for implementation consultants"</li>
            <li>"Show me my applications"</li>
            <li>"Apply to all matching jobs"</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default VoiceInterface;
