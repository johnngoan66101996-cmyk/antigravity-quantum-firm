Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Rate = 0
$synth.Volume = 100
$synth.SetOutputToWaveFile("firm_environment/storage/voiceover2_grok.wav")
$text = [System.IO.File]::ReadAllText("firm_environment/storage/script2.txt", [System.Text.Encoding]::UTF8)
$synth.Speak($text)
$synth.Dispose()
Write-Host "VOICEOVER_2_SUCCESS"
