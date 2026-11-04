Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SetOutputToWaveFile("firm_environment/storage/test_voice.wav")
$synth.Speak("Привет, это проверка синтеза речи для квантового ИИ.")
$synth.Dispose()
Write-Host "Voice synthesis successful!"
