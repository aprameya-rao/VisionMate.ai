    let mediaRecorder;
    let audioChunks = [];
  
    const recordBtn = document.getElementById("recordBtn");
    const stopBtn = document.getElementById("stopBtn");
    const status = document.getElementById("status");
    const transcript = document.getElementById("transcript");
  
    recordBtn.onclick = async () => {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];
  
      mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
      };
  
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append("file", audioBlob, "audio.webm");
  
        status.textContent = "Status: Transcribing...";
  
        try {
          const response = await fetch("http://localhost:8000/transcribe", {
            method: "POST",
            body: formData
          });
  
          const data = await response.json(); // Make sure this line exists!
          console.log("Response from API:", data);
  
          if (data.transcript) {
            transcript.textContent = "Transcript: " + data.transcript;
            status.textContent = "Status: Done.";
            console.log("done");
          } else {
            transcript.textContent = "Transcript: [No text received]";
            status.textContent = "Status: Error - empty response.";
          }
        } catch (err) {
          console.error("Transcription error:", err);
          status.textContent = "Status: Error - could not reach API.";
          transcript.textContent = "Transcript: [Error]";
          console.log("not done");
        }
      };
  
      mediaRecorder.start();
      status.textContent = "Status: Recording...";
      recordBtn.disabled = true;
      stopBtn.disabled = false;
    };
  
    stopBtn.onclick = () => {
      mediaRecorder.stop();
      recordBtn.disabled = false;
      stopBtn.disabled = true;
    };