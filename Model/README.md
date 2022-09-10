# Euterpe Pre-Trained Model

***

### Here is a SMALL/DEMO Euterpe Pre-Trained Model for evaluation and testing
### LARGE/FULL model is NOT going to be published and it is only avaialable for licensing/commercial use

***

## DEMO Model Stats:

### Multi-Instrumental MIDI model with six velocity degrees
### Trained upon 12GB of multi-instrumental MIDI music for 1 epochs (64k steps/~64 hours) @ 32 batches on quad A6000 GPUs
### FLoss 0.8806 CE
### VFloss 0.8806 CE
### Acc 0.76 CE

***

## Model Sequence Info:

### [(MIDI Channel(0-11) * 11)+Velocity(1-6), dTime(0-127)+128, Duration(1-127)+256, MIDI Pitch(1-127)+384]

***

![Euterpe-Training-Loss-Graph](https://user-images.githubusercontent.com/56325539/189494622-2d8a6342-aa3d-48e6-9cf6-6af24dcc3c9a.png)


***

![Euterpe-Positional-Embeddings-Plot](https://user-images.githubusercontent.com/56325539/189494625-efe9ae59-84f2-4f9d-a35e-fb0e649e1141.png)

***

### Project Los Angeles
### Tegridy Code 2022
