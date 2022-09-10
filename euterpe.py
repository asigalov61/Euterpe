# -*- coding: utf-8 -*-
"""Euterpe.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/asigalov61/Euterpe/blob/main/Euterpe.ipynb

# Euterpe (ver. 1.0)

***

Powered by tegridy-tools: https://github.com/asigalov61/tegridy-tools

***

Credit for GPT2-RGA code used in this colab goes out @ Sashmark97 https://github.com/Sashmark97/midigen and @ Damon Gwinn https://github.com/gwinndr/MusicTransformer-Pytorch

***

WARNING: This complete implementation is a functioning model of the Artificial Intelligence. Please excercise great humility, care, and respect. https://www.nscai.gov/

***

#### Project Los Angeles

#### Tegridy Code 2022

***

# (Setup Environment)
"""

#@title nvidia-smi gpu check
!nvidia-smi

#@title Install all dependencies (run only once per session)

!git clone https://github.com/asigalov61/Euterpe

!pip install torch
!pip install torch-summary

!pip install tqdm
!pip install matplotlib
!pip install sklearn

!apt install fluidsynth #Pip does not work for some reason. Only apt works
!pip install midi2audio

#@title Import all needed modules

print('Loading needed modules. Please wait...')
import os
import random
import copy

from collections import OrderedDict

from tqdm.notebook import tqdm

import matplotlib.pyplot as plt

from torchsummary import summary
from sklearn import metrics

print('Loading TMIDIX module...')
os.chdir('/content/Euterpe')

import TMIDIX
from GPT2RGAX import *

from midi2audio import FluidSynth
from IPython.display import Audio, display

os.chdir('/content/')

"""# (UNZIP MODEL)"""

# Commented out IPython magic to ensure Python compatibility.
#@title Unzip pre-trained Euterpe Model
# %cd /content/Euterpe/Model

print('=' * 70)
print('Unzipping pre-trained model...Please wait...')
print('=' * 70)

!cat /content/Euterpe/Model/Euterpe-Trained-Model.zip* > Euterpe-Trained-Model.zip
print('=' * 70)

!unzip -j Euterpe-Trained-Model.zip
print('=' * 70)

print('Done! Enjoy! :)')
print('=' * 70)
# %cd /content/

"""# (LOAD)"""

#@title Load/Reload the model

full_path_to_model_checkpoint = "/content/Euterpe/Model/Euterpe-Trained-Model_66924_steps_0.8806_loss.pth" #@param {type:"string"}

print('Loading the model...')
config = GPTConfig(512, 
                   1280,
                   dim_feedforward=1280,
                   n_layer=16, 
                   n_head=16, 
                   n_embd=1280,
                   enable_rpr=True,
                   er_len=1280)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = GPT(config)

state_dict = torch.load(full_path_to_model_checkpoint, map_location=device)

new_state_dict = OrderedDict()
for k, v in state_dict.items():
    name = k[7:] #remove 'module'
    new_state_dict[name] = v

model.load_state_dict(new_state_dict)

model.to(device)

model.eval()

print('Done!')

summary(model)

cos_sim = metrics.pairwise.cosine_similarity(
    model.tok_emb.weight.detach().cpu().numpy()
)
plt.figure(figsize=(8, 8))
plt.imshow(cos_sim, cmap="inferno", interpolation="none")
im_ratio = cos_sim.shape[0] / cos_sim.shape[1]
plt.colorbar(fraction=0.046 * im_ratio, pad=0.04)
plt.xlabel("Position")
plt.ylabel("Position")
plt.tight_layout()
plt.plot()
plt.savefig("/content/Euterpe-Positional-Embeddings-Plot.png", bbox_inches="tight")

"""# (GENERATE)

# Improvisation from scratch
"""

#@title Improv Generator

#@markdown Select desired instruments (any combination is fine)

Piano = True #@param {type:"boolean"}
Guitar = True #@param {type:"boolean"}
Bass = True #@param {type:"boolean"}
Violin = False #@param {type:"boolean"}
Cello = False #@param {type:"boolean"}
Harp = False #@param {type:"boolean"}
Trumpet = False #@param {type:"boolean"}
Clarinet = False #@param {type:"boolean"}
Flute = False #@param {type:"boolean"}
Drums = True #@param {type:"boolean"}
Choir = False #@param {type:"boolean"}
Organ = False #@param {type:"boolean"}

#@markdown Improv Timings and Velocity

desired_prime_time = 18 #@param {type:"slider", min:1, max:126, step:1}
desired_prime_duration = 15 #@param {type:"slider", min:1, max:126, step:1}
desired_velocity = 4 #@param {type:"slider", min:1, max:6, step:1}

#@markdown Model settings

number_of_notes_to_generate = 512 #@param {type:"slider", min:16, max:2048, step:16}
number_of_memory_tokens = 512 #@param {type:"slider", min:16, max:1280, step:16}
temperature = 0.8 #@param {type:"slider", min:0.1, max:1, step:0.1}
show_stats = False #@param {type:"boolean"}

instruments = []

if Piano:
  instruments += [(0 * 11)+desired_velocity,
                  0+128,
                  desired_prime_duration+256,
                  60+384] + [(0 * 11)+desired_velocity,
                  0+128,
                  desired_prime_duration+256,
                  48+384]

if Guitar:
  instruments += [(1 * 11)+desired_velocity,
                  0+128,
                  desired_prime_duration+256,
                  60+384]

if Bass:
  instruments += [(2 * 11)+desired_velocity,
                  0+128,
                  desired_prime_duration+256,
                  46+384]

if Violin:
  instruments += [(3 * 11)+desired_velocity,
                  0+128,
                  desired_prime_duration+256,
                  72+384]

if Cello:
  instruments += [(4 * 11)+desired_velocity,
                  0+128,
                  desired_prime_duration+256,
                  46+384]

if Harp:
  instruments += [(5 * 11)+desired_velocity,
                  0+128,
                  desired_prime_duration+256,
                  72+384]

if Trumpet:
  instruments += [(6 * 11)+desired_velocity,
                  0+128,
                  desired_prime_duration+256,
                  72+384]

if Clarinet:
  instruments += [(7 * 11)+desired_velocity,
                  0+128,
                  desired_prime_duration+256,
                  72+384]

if Flute:
  instruments += [(8 * 11)+desired_velocity,
                  0+128,
                  desired_prime_duration+256,
                  72+384]

if Drums:
  instruments += [(9 * 11)+desired_velocity,
                  0+128,
                  desired_prime_duration+256,
                  35+384]

if Choir:
  instruments += [(10 * 11)+desired_velocity,
                  0+128,
                  desired_prime_duration+256,
                  58+384]

if Organ:
  instruments += [(11 * 11)+desired_velocity,
                  0+128,
                  desired_prime_duration+256,
                  58+384]
instruments[1] = desired_prime_time+128
instruments[5::4] = [0+128] * len(instruments[5::4])

prime = instruments

#===================================================================

print('=' * 70)
print('Euterpe Music Model Improvisation Generator')
print('=' * 70)

print('Generation settings:')
print('=' * 70)
print('Number of notes to generate:', number_of_notes_to_generate)
print('Number of memory tokens:', number_of_memory_tokens)
print('Model temperature:', temperature)

print('=' * 70)
print('Generating...')

out1 = []
out1.extend(prime)

for i in tqdm(range(number_of_notes_to_generate)):

  if len(out1)+4 < number_of_memory_tokens:
    num_memtoks = len(out1)+4
  else:
    num_memtoks = number_of_memory_tokens

  rand_seq = model.generate(torch.Tensor(out1[-(number_of_memory_tokens-4):]), 
                                          target_seq_length=num_memtoks,
                                          temperature=temperature,
                                          stop_token=512,
                                          verbose=show_stats)
    
  out = rand_seq[0].cpu().tolist()

  out1.extend(out[-4:])

if len(out1) != 0:
    
    song = out1
    song_f = []
    time = 0
    dur = 0
    vel = 0
    pitch = 0
    channel = 0
    son = []
    song1 = []

    for s in song:
      if s > 127:
        son.append(s)

      else:
        if len(son) == 4:
          song1.append(son)
        son = []
        son.append(s)
    
    for s in song1:
      if s[0] > 0 and s[1] >= 128:
        if s[2] > 256 and s[3] > 384:

          channel = s[0] // 11

          vel = (s[0] % 11) * 19

          time += (s[1]-128) * 16
      
          dur = (s[2] - 256) * 32
          
          pitch = (s[3] - 384)
                                    
          song_f.append(['note', time, dur, channel, pitch, vel ])

    detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                        output_signature = 'Euterpe',  
                                                        output_file_name = '/content/Euterpe-Music-Composition', 
                                                        track_name='Project Los Angeles',
                                                        list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 53, 19, 0, 0, 0, 0],
                                                        number_of_ticks_per_quarter=500)

    print('Done!')

print('Displaying resulting composition...')
fname = '/content/Euterpe-Music-Composition'

x = []
y =[]
c = []

colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

for s in song_f:
  x.append(s[1] / 1000)
  y.append(s[4])
  c.append(colors[s[3]])

FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
display(Audio(str(fname + '.wav'), rate=16000))

plt.figure(figsize=(14,5))
ax=plt.axes(title=fname)
ax.set_facecolor('black')

plt.scatter(x,y, c=c)
plt.xlabel("Time")
plt.ylabel("Pitch")
plt.show()

"""# Continuation / Inpainting / Melody Orchestration"""

#@title Load Seed/Custom MIDI
full_path_to_custom_MIDI_file = "/content/Euterpe/Euterpe-MI-Seed-1.mid" #@param {type:"string"}

print('Loading custom MIDI file...')
score = TMIDIX.midi2ms_score(open(full_path_to_custom_MIDI_file, 'rb').read())

events_matrix = []

itrack = 1

patches = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

patch_map = [[0, 1, 2, 3, 4, 5, 6, 7], # Piano 
              [24, 25, 26, 27, 28, 29, 30], # Guitar
              [32, 33, 34, 35, 36, 37, 38, 39], # Bass
              [40, 41], # Violin
              [42, 43], # Cello
              [46], # Harp
              [56, 57, 58, 59, 60], # Trumpet
              [71, 72], # Clarinet
              [73, 74, 75], # Flute
              [-1], # Fake Drums
              [52, 53], # Choir
              [16, 17, 18, 19, 20] # Organ
            ]

while itrack < len(score):
    for event in score[itrack]:         
        if event[0] == 'note' or event[0] == 'patch_change':
            events_matrix.append(event)
    itrack += 1

events_matrix.sort(key=lambda x: x[1])

events_matrix1 = []
for event in events_matrix:
        if event[0] == 'patch_change':
            patches[event[2]] = event[3]

        if event[0] == 'note':
            event.extend([patches[event[3]]])
            once = False
            
            for p in patch_map:
                if event[6] in p and event[3] != 9: # Except the drums
                    event[3] = patch_map.index(p)
                    once = True
                    
            if not once and event[3] != 9: # Except the drums
                event[3] = 0 # All other instruments/patches channel
                event[5] = max(80, event[5])
                
            if event[3] < 12: # We won't write chans 11-16 for now...
                events_matrix1.append(event)

# Sorting...
events_matrix1.sort(key=lambda x: (x[1], x[3]))

# recalculating timings
for e in events_matrix1:
    e[1] = int(e[1] / 16)
    e[2] = int(e[2] / 32)

# final processing...

inputs = []

melody = []

melody_chords = []

pe = events_matrix1[0]
for e in events_matrix1:

    time = max(0, min(127, e[1]-pe[1]))
    dur = max(1, min(127, e[2]))
    cha = max(0, min(11, e[3]))
    ptc = max(1, min(127, e[4]))
    vel = max(19, min(127, e[5]))

    div_vel = int(vel / 19)

    chan_vel = (cha * 11) + div_vel

    # Continuation / Inpainting
    inputs.extend([chan_vel, time+128, dur+256, ptc+384])

    # Melody Orchestration
    if time != 0:
      if ptc < 60:
        ptc = (ptc % 12) + 60  

      # Converted to Piano
      melody.extend([div_vel, time+128, dur+256, ptc+384])

    # For future development
    melody_chords.append([time, dur, cha, ptc, vel])

    pe = e

# =================================

out1 = inputs

if len(out1) != 0:
    
    song = out1
    song_f = []
    time = 0
    dur = 0
    vel = 0
    pitch = 0
    channel = 0
    son = []
    song1 = []

    for s in song:
      if s > 127:
        son.append(s)

      else:
        if len(son) == 4:
          song1.append(son)
        son = []
        son.append(s)
    
    for s in song1:
      if s[0] > 0 and s[1] >= 128:
        if s[2] > 256 and s[3] > 384:

          channel = s[0] // 11

          vel = (s[0] % 11) * 19

          time += (s[1]-128) * 16
      
          dur = (s[2] - 256) * 32
          
          pitch = (s[3] - 384)
                                    
          song_f.append(['note', time, dur, channel, pitch, vel ])

    detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                        output_signature = 'Euterpe',  
                                                        output_file_name = '/content/Euterpe-Music-Composition', 
                                                        track_name='Project Los Angeles',
                                                        list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 53, 19, 0, 0, 0, 0],
                                                        number_of_ticks_per_quarter=500)

    print('Done!')

print('Displaying resulting composition...')
fname = '/content/Euterpe-Music-Composition'

x = []
y =[]
c = []

colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

for s in song_f:
  x.append(s[1] / 1000)
  y.append(s[4])
  c.append(colors[s[3]])

FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
display(Audio(str(fname + '.wav'), rate=16000))

plt.figure(figsize=(14,5))
ax=plt.axes(title=fname)
ax.set_facecolor('black')

plt.scatter(x,y, c=c)
plt.xlabel("Time")
plt.ylabel("Pitch")
plt.show()

"""# Continuation"""

#@title Single Continuation Block Generator

#@markdown NOTE: Play with the settings to get different results
number_of_prime_tokens = 512 #@param {type:"slider", min:16, max:512, step:16}
number_of_tokens_to_generate = 1024 #@param {type:"slider", min:64, max:1264, step:32}
number_of_batches = 2 #@param {type:"slider", min:1, max:8, step:1}
temperature = 0.8 #@param {type:"slider", min:0.1, max:1, step:0.1}
show_stats = True #@param {type:"boolean"}

#===================================================================
print('=' * 70)
print('Euterpe Music Model Continuation Generator')
print('=' * 70)

print('Generation settings:')
print('=' * 70)
print('Number of prime tokens:', number_of_prime_tokens)
print('Number of tokens to generate:', number_of_tokens_to_generate)
print('Number of batches:', number_of_batches)
print('Model temperature:', temperature)

print('=' * 70)
print('Generating...')

num_toks = min(1280, number_of_prime_tokens+number_of_tokens_to_generate)

inp = inputs[:number_of_prime_tokens]

rand_seq = model.generate_batches(torch.Tensor(inp), 
                                          target_seq_length=num_toks,
                                          temperature=temperature,
                                          num_batches=number_of_batches,
                                          verbose=show_stats)
  
out1 = rand_seq.cpu().tolist()

bcount = 1

for o in out1:

  if len(o) != 0:
      
      song = o
      song_f = []
      time = 0
      dur = 0
      vel = 0
      pitch = 0
      channel = 0
      son = []
      song1 = []

      for s in song:
        if s > 127:
          son.append(s)

        else:
          if len(son) == 4:
            song1.append(son)
          son = []
          son.append(s)
      
      for s in song1:
        if s[0] > 0 and s[1] >= 128:
          if s[2] > 256 and s[3] > 384:

            channel = s[0] // 11

            vel = (s[0] % 11) * 19

            time += (s[1]-128) * 16
        
            dur = (s[2] - 256) * 32
            
            pitch = (s[3] - 384)
                                      
            song_f.append(['note', time, dur, channel, pitch, vel ])

      detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                          output_signature = 'Euterpe',  
                                                          output_file_name = '/content/Euterpe-Music-Composition_'+str(bcount), 
                                                          track_name='Project Los Angeles',
                                                          list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 53, 19, 0, 0, 0, 0],
                                                          number_of_ticks_per_quarter=500)

      print('Done!')

  print('Displaying resulting composition...')
  fname = '/content/Euterpe-Music-Composition_' + str(bcount)

  x = []
  y =[]
  c = []

  colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

  for s in song_f:
    x.append(s[1] / 1000)
    y.append(s[4])
    c.append(colors[s[3]])

  FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
  display(Audio(str(fname + '.wav'), rate=16000))

  plt.figure(figsize=(14,5))
  ax=plt.axes(title=fname)
  ax.set_facecolor('black')

  plt.scatter(x,y, c=c)
  plt.xlabel("Time")
  plt.ylabel("Pitch")
  plt.show()

  bcount += 1

#@title Auto-Continue Custom MIDI

#@markdown NOTE: This may or may not work well due to long-term structure decay
number_of_continuation_notes = 400 #@param {type:"slider", min:10, max:2000, step:10}
number_of_memory_tokens = 1276 #@param {type:"slider", min:64, max:1276, step:4}
temperature = 0.8 #@param {type:"slider", min:0.1, max:1, step:0.1}
show_stats = False #@param {type:"boolean"}

#===================================================================
print('=' * 70)
print('Euterpe Music Model Auto-Continuation Generator')
print('=' * 70)

print('Generation settings:')
print('=' * 70)
print('Number of continuation notes:', number_of_continuation_notes)
print('Number of memory tokens:', number_of_memory_tokens)
print('Model temperature:', temperature)

print('=' * 70)
print('Generating...')

out2 = copy.deepcopy(inputs)

memt = min(number_of_memory_tokens, len(out2)-4)
seqt = min(number_of_memory_tokens+4, memt+4)

for i in tqdm(range(number_of_continuation_notes)):

  rand_seq = model.generate(torch.Tensor(out2[-memt:]), 
                                            target_seq_length=seqt,
                                            temperature=temperature,
                                            stop_token=512,
                                            verbose=show_stats)
    
  out = rand_seq[0].cpu().tolist()

  out2.extend(out[-4:])

if len(out2) != 0:
    
    song = out2
    song_f = []
    time = 0
    dur = 0
    vel = 0
    pitch = 0
    channel = 0
    son = []
    song1 = []

    for s in song:
      if s > 127:
        son.append(s)

      else:
        if len(son) == 4:
          song1.append(son)
        son = []
        son.append(s)
    
    for s in song1:
      if s[0] > 0 and s[1] >= 128:
        if s[2] > 256 and s[3] > 384:

          channel = s[0] // 11

          vel = (s[0] % 11) * 19

          time += (s[1]-128) * 16
      
          dur = (s[2] - 256) * 32
          
          pitch = (s[3] - 384)
                                    
          song_f.append(['note', time, dur, channel, pitch, vel ])

    detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                        output_signature = 'Euterpe',  
                                                        output_file_name = '/content/Euterpe-Music-Composition', 
                                                        track_name='Project Los Angeles',
                                                        list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 53, 19, 0, 0, 0, 0],
                                                        number_of_ticks_per_quarter=500)

    print('Done!')

print('Displaying resulting composition...')
fname = '/content/Euterpe-Music-Composition'

x = []
y =[]
c = []

colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

for s in song_f:
  x.append(s[1] / 1000)
  y.append(s[4])
  c.append(colors[s[3]])

FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
display(Audio(str(fname + '.wav'), rate=16000))

plt.figure(figsize=(14,5))
ax=plt.axes(title=fname)
ax.set_facecolor('black')

plt.scatter(x,y, c=c)
plt.xlabel("Time")
plt.ylabel("Pitch")
plt.show()

"""# Inpainting"""

#@title Inpainting / Controlled Generation
control_type = "Channel-Velocity-Time-Duration" #@param ["Channel-Velocity", "Channel-Velocity-Time", "Channel-Velocity-Time-Duration"]
number_of_prime_notes = 16 #@param {type:"slider", min:1, max:64, step:1}
number_of_memory_tokens = 512 #@param {type:"slider", min:64, max:1280, step:16}
temperature = 0.8 #@param {type:"slider", min:0.1, max:1, step:0.1}
show_stats = False #@param {type:"boolean"}

#===================================================================

print('=' * 70)
print('Euterpe Music Model Inpainting Generator')
print('=' * 70)

print('Generation settings:')
print('=' * 70)
print('Control type:', control_type)
print('Number of memory tokens:', number_of_memory_tokens)
print('Model temperature:', temperature)

print('=' * 70)
print('Generating...')

out2 = copy.deepcopy(inputs)

memt = min(number_of_memory_tokens, len(out2)-4)
seqt = min(number_of_memory_tokens+4, memt+4)

if control_type == 'Channel-Velocity':
  ctrl = 1

if control_type == 'Channel-Velocity-Time':
  ctrl = 2

if control_type == 'Channel-Velocity-Time-Duration':
  ctrl = 3

out3 = []

out3.extend(inputs[:number_of_prime_notes * 4])

for i in tqdm(range(((number_of_prime_notes+1) * 4), len(inputs), 4)):

  out3.extend(out2[i:i+ctrl])

  rand_seq = model.generate(torch.Tensor(out3[-memt:]), 
                                            target_seq_length=len(out3[-memt:])+(4-ctrl),
                                            temperature=temperature,
                                            stop_token=512,
                                            verbose=show_stats)
    
  out = rand_seq[0].cpu().tolist()

  out3.extend(out[-(4-ctrl):])

if len(out3) != 0:
    
    song = out3
    song_f = []
    time = 0
    dur = 0
    vel = 0
    pitch = 0
    channel = 0
    son = []
    song1 = []

    for s in song:
      if s > 127:
        son.append(s)

      else:
        if len(son) == 4:
          song1.append(son)
        son = []
        son.append(s)
    
    for s in song1:
      if s[0] > 0 and s[1] >= 128:
        if s[2] > 256 and s[3] > 384:

          channel = s[0] // 11

          vel = (s[0] % 11) * 19

          time += (s[1]-128) * 16
      
          dur = (s[2] - 256) * 32
          
          pitch = (s[3] - 384)
                                    
          song_f.append(['note', time, dur, channel, pitch, vel ])

    detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                        output_signature = 'Euterpe',  
                                                        output_file_name = '/content/Euterpe-Music-Composition', 
                                                        track_name='Project Los Angeles',
                                                        list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 53, 19, 0, 0, 0, 0],
                                                        number_of_ticks_per_quarter=500)

    print('Done!')

print('Displaying resulting composition...')
fname = '/content/Euterpe-Music-Composition'

x = []
y =[]
c = []

colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

for s in song_f:
  x.append(s[1] / 1000)
  y.append(s[4])
  c.append(colors[s[3]])

FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
display(Audio(str(fname + '.wav'), rate=16000))

plt.figure(figsize=(14,5))
ax=plt.axes(title=fname)
ax.set_facecolor('black')

plt.scatter(x,y, c=c)
plt.xlabel("Time")
plt.ylabel("Pitch")
plt.show()

"""# Melody Orchestration"""

#@title Melody Orchestration
number_of_prime_notes = 12 #@param {type:"slider", min:1, max:64, step:1}
number_of_memory_tokens = 512 #@param {type:"slider", min:64, max:1280, step:16}
number_of_desired_instruments = 3 #@param {type:"slider", min:1, max:10, step:1}
temperature = 0.8 #@param {type:"slider", min:0.1, max:1, step:0.1}
show_stats = False #@param {type:"boolean"}

#===================================================================

print('=' * 70)
print('Euterpe Music Model Melody Orchestration Generator')
print('=' * 70)

print('Generation settings:')
print('=' * 70)
print('Number of prime notes:', number_of_prime_notes)
print('Number of memory tokens:', number_of_memory_tokens)
print('Number of desired instruments:', number_of_desired_instruments)
print('Model temperature:', temperature)

print('=' * 70)
print('Generating...')


out2 = copy.deepcopy(melody)

memt = min(number_of_memory_tokens, len(out2)-4)
seqt = min(number_of_memory_tokens+4, memt+4)

out3 = []

out3.extend(melody[:(number_of_prime_notes * 4)+2])


number_of_desired_instruments = 3

for i in tqdm(range(((number_of_prime_notes+1) * 4)-2, len(melody)-2, 4)):

  out3.extend(out2[i:i+4])

  for j in range(number_of_desired_instruments):

    rand_seq = model.generate(torch.Tensor(out3[-memt:]), 
                                              target_seq_length=len(out3[-memt:])+4,
                                              temperature=temperature,
                                              stop_token=512,
                                              verbose=show_stats)
      
    out = rand_seq[0].cpu().tolist()

    out3.extend(out[-4:])


    out3[-2] = ((j+1)*11)+(out3[-6] % 11)

    out3[-1] = 128

if len(out3) != 0:
    
    song = out3
    song_f = []
    time = 0
    dur = 0
    vel = 0
    pitch = 0
    channel = 0
    son = []
    song1 = []

    for s in song:
      if s > 127:
        son.append(s)

      else:
        if len(son) == 4:
          song1.append(son)
        son = []
        son.append(s)
    
    for s in song1:
      if s[0] > 0 and s[1] >= 128:
        if s[2] > 256 and s[3] > 384:

          channel = s[0] // 11

          vel = (s[0] % 11) * 19

          time += (s[1]-128) * 16
      
          dur = (s[2] - 256) * 32
          
          pitch = (s[3] - 384)
                                    
          song_f.append(['note', time, dur, channel, pitch, vel ])

    detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                        output_signature = 'Euterpe',  
                                                        output_file_name = '/content/Euterpe-Music-Composition', 
                                                        track_name='Project Los Angeles',
                                                        list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 53, 19, 0, 0, 0, 0],
                                                        number_of_ticks_per_quarter=500)

    print('Done!')

print('Displaying resulting composition...')
fname = '/content/Euterpe-Music-Composition'

x = []
y =[]
c = []

colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

for s in song_f:
  x.append(s[1] / 1000)
  y.append(s[4])
  c.append(colors[s[3]])

FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
display(Audio(str(fname + '.wav'), rate=16000))

plt.figure(figsize=(14,5))
ax=plt.axes(title=fname)
ax.set_facecolor('black')

plt.scatter(x,y, c=c)
plt.xlabel("Time")
plt.ylabel("Pitch")
plt.show()

"""# Congrats! You did it! :)"""