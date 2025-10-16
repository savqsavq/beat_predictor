# beat_predictor
rough bpm estimator prototype.  
uses clip duration + rough rms amplitude to guess tempo, then simulates tempo variation and swing.  
outputs bpm graph + json summary.

## usage
```bash
python beat_predictor.py sample.wav
```