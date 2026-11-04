Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Rate = 0
$synth.Volume = 100
$synth.SetOutputToWaveFile("firm_environment/storage/voiceover1_claude.wav")
$text = [System.IO.File]::ReadAllText("firm_environment/storage/script1.txt", [System.Text.Encoding]::UTF8)
$synth.Speak($text)
$synth.Dispose()
Write-Host "VOICEOVER_1_SUCCESS"
