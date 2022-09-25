# -*- coding: utf-8 -*-
"""Euterpe_Maker.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/asigalov61/Euterpe/blob/main/Training-Code/Euterpe_Maker.ipynb

# Euterpe Maker (ver. 1.0)

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
!pip install tqdm
!pip install matplotlib

#@title Import all needed modules

print('Loading needed modules. Please wait...')
import os
from tqdm import tqdm
import random
import secrets

if not os.path.exists('/content/Dataset'):
    os.makedirs('/content/Dataset')

if not os.path.exists('/content/INTS'):
    os.makedirs('/content/INTS')

print('Loading TMIDIX and GPT2RGAX modules...')
os.chdir('/content/Euterpe')
import TMIDIX
from GPT2RGAX import *

import matplotlib.pyplot as plt

os.chdir('/content/')

"""# (FROM SCRATCH) Download and process MIDI dataset

### Acquire MMD Dataset here and untar it to the ./Dataset dir

https://github.com/jeffreyjohnens/MetaMIDIDataset
"""

# Commented out IPython magic to ensure Python compatibility.
#@title Download original LAKH MIDI Dataset here

# %cd /content/Dataset/

!wget 'http://hog.ee.columbia.edu/craffel/lmd/lmd_full.tar.gz'
!tar -xvf 'lmd_full.tar.gz'
!rm 'lmd_full.tar.gz'

# %cd /content/

"""# (PROCESS)

### Processing is going to be done in chunks due to huge size of the datasets
"""

#@title Scan the ./Dataset dir/MIDI files and save the file list just in case
###########

print('Loading MIDI files...')
print('This may take a while on a large dataset in particular.')

dataset_addr = "/content/Dataset"
# os.chdir(dataset_addr)
filez = list()
for (dirpath, dirnames, filenames) in os.walk(dataset_addr):
    filez += [os.path.join(dirpath, file) for file in filenames]
print('=' * 70)

if filez == []:
    print('Could not find any MIDI files. Please check Dataset dir...')
    print('=' * 70)

print('Randomizing file list...')
random.shuffle(filez)

TMIDIX.Tegridy_Any_Pickle_File_Writer(filez, '/content/Euterpe-MIDIs-File-List')

#@title LOAD/RELOAD MIDI file list
filez = TMIDIX.Tegridy_Any_Pickle_File_Reader('/content/Euterpe-MIDIs-File-List')

#@title Process MIDIs with TMIDIX MIDI processor

sorted_or_random_file_loading_order = False # Sorted order is NOT usually recommended
dataset_ratio = 1 # Change this if you need more data


print('TMIDIX MIDI Processor')
print('Starting up...')
###########

files_count = 0

gfiles = []

melody_chords_f = []

stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

print('Processing MIDI files. Please wait...')
for f in tqdm(filez[:int(len(filez) * dataset_ratio)]):
    try:
        fn = os.path.basename(f)
        fn1 = fn.split('.')[0]

        #print('Loading MIDI file...')
        score = TMIDIX.midi2ms_score(open(f, 'rb').read())

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
                        stats[event[3]] += 1

        # Sorting...
        events_matrix1.sort(key=lambda x: (x[1], x[3]))

        # recalculating timings
        for e in events_matrix1:
            e[1] = int(e[1] / 16)
            e[2] = int(e[2] / 32)
        
        # final processing...

        pe = events_matrix1[0]
        for e in events_matrix1:

            time = max(0, min(127, e[1]-pe[1]))
            dur = max(1, min(127, e[2]))
            cha = max(0, min(11, e[3]))
            ptc = max(1, min(127, e[4]))
            vel = max(19, min(127, e[5]))

            div_vel = int(vel / 19)

            chan_vel = (cha * 11) + div_vel

            melody_chords_f.extend([chan_vel, time+128, dur+256, ptc+384])

            pe = e

        # Break between compositions
        melody_chords_f.extend([0, 127+128, 127+256, 0+384])
        melody_chords_f.extend([0, 127+128, 127+256, 0+384])

        files_count += 1

        if files_count % 4000 == 0:
          count = str(files_count)
          TMIDIX.Tegridy_Any_Pickle_File_Writer(melody_chords_f, '/content/INTS/Euterpe_INTs_'+count)
          melody_chords_f = []
        
    except KeyboardInterrupt:
        print('Saving current progress and quitting...')
        break  

    except:
        print('Bad MIDI:', f)
        continue

count = str(files_count)
TMIDIX.Tegridy_Any_Pickle_File_Writer(melody_chords_f, '/content/INTS/Euterpe_INTs_'+count)

print('=' * 70)
        
print('Done!')   
print('=' * 70)

print('Resulting Stats:')
print('=' * 70)
print('Total MIDI Files:', files_count)
print('=' * 70)

print('Piano:', stats[0])
print('Guitar:', stats[1])
print('Bass:', stats[2])
print('Violin:', stats[3])
print('Cello:', stats[4])
print('Harp:', stats[5])
print('Trumpet:', stats[6])
print('Clarinet:', stats[7])
print('Flute:', stats[8])
print('Drums:', stats[9])
print('Choir:', stats[10])
print('Organ:', stats[11])

print('=' * 70)

"""# (FROM THE TRAIN DATA PACK) Download pre-processed and ready-to-use Euterpe training data

## Once you downloaded and unziped the train data pack, you can jump straight to INTs loading code below
"""

# Commented out IPython magic to ensure Python compatibility.
#@title Euterpe Training Data Pack (2GB compressed)
# %cd /content/INTS/
!wget --no-check-certificate -O 'Euterpe-Training-Data.zip' "https://onedrive.live.com/download?cid=8A0D502FC99C608F&resid=8A0D502FC99C608F%2118665&authkey=AF0mW39Iqv0gR5o"
!unzip 'Euterpe-Training-Data.zip'
!rm 'Euterpe-Training-Data.zip'
# %cd /content/

"""# (LOAD INTs)"""

#@title Load INTs...

#@markdown PLEASE NOTE: You will need at least 32GB RAM to load all files

print('Processing the dataset...')

dataset_addr = "/content/INTS"
# os.chdir(dataset_addr)
filez = list()
for (dirpath, dirnames, filenames) in os.walk(dataset_addr):
    filez += [os.path.join(dirpath, file) for file in filenames]
print('=' * 70)

filez.sort()

print('Processing MIDI files. Please wait...')

train_data = torch.Tensor()

for f in tqdm(filez):
  fn = f.split('.')[0]
  train_data = torch.cat((train_data, torch.Tensor(TMIDIX.Tegridy_Any_Pickle_File_Reader(fn))))
  print('Loaded file:', f)

print('Done!')        
print('=' * 70)
        
print('Total INTs:', len(train_data))
print('=' * 70)

"""# Test the resulting INTs dataset..."""

#@title Test INTs
print('Sample INTs', train_data[:15])

out = train_data[:160000].tolist()

if len(out) != 0:
    
    song = out
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

"""# (PREP DATALOADER)"""

#@title Prep the dataloader

SEQ_LEN = max_seq

BATCH_SIZE = 1 # Change this to your specs

# DO NOT FORGET TO ADJUST MODEL PARAMS IN GPT2RGAX module to your specs

print('=' * 50)
print('Loading training data...')

class MusicSamplerDataset(Dataset):
    def __init__(self, data, seq_len):
        super().__init__()
        self.data = data
        self.seq_len = seq_len

    def __getitem__(self, index):

        rand = secrets.randbelow((self.data.size(0)-(self.seq_len)) // (self.seq_len)) * (self.seq_len)

        x = self.data[rand: rand + self.seq_len].long()
        trg = self.data[(rand+1): (rand+1) + self.seq_len].long()
        
        return x, trg

    def __len__(self):
        return self.data.size(0) // self.seq_len

train_dataset = MusicSamplerDataset(train_data, SEQ_LEN)
val_dataset   = MusicSamplerDataset(train_data, SEQ_LEN)
train_loader  = DataLoader(train_dataset, batch_size = BATCH_SIZE)
val_loader    = DataLoader(val_dataset, batch_size = BATCH_SIZE)

print('=' * 50)
print('Sample train dataset:', train_dataset[0])
print('Sample val dataset:', val_dataset[0])
print('=' * 50)
print('Train loader length:', len(train_loader))
print('Val loader length:', len(val_loader))
print('=' * 50)
print('Done! Enjoy! :)')
print('=' * 50)

"""# (TRAIN)

# Train the model
"""

#@title Train

DIC_SIZE = 512

# DO NOT FORGET TO ADJUST MODEL PARAMS IN GPT2RGAX module to your specs

config = GPTConfig(DIC_SIZE, 
                   max_seq,
                   dim_feedforward=2048,
                   n_layer=24, 
                   n_head=8, 
                   n_embd=1024,
                   enable_rpr=True,
                   er_len=max_seq)

# DO NOT FORGET TO ADJUST MODEL PARAMS IN GPT2RGAX module to your specs

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = GPT(config)

model = nn.DataParallel(model)

model.to(device)

#=====

init_step = 0
lr = 0.1 # Seems to work best
lr_stepper = LrStepTracker(d_model, SCHEDULER_WARMUP_STEPS, init_step)
eval_loss_func = nn.CrossEntropyLoss(ignore_index=DIC_SIZE)
train_loss_func = eval_loss_func

# opt = Adam(model.parameters(), lr=lr, betas=(ADAM_BETA_1, ADAM_BETA_2), eps=ADAM_EPSILON)

opt = Adam(model.parameters(), lr=lr) # Default optimizer settings work better on large datasets

lr_scheduler = LambdaLR(opt, lr_stepper.step)


#===

best_eval_acc        = 0.0
best_eval_acc_epoch  = -1
best_eval_loss       = float("inf")
best_eval_loss_epoch = -1
best_acc_file = '/content/gpt2_rpr_acc.pth'
best_loss_file = '/content/gpt2_rpr_loss.pth'
loss_train, loss_val, acc_val = [], [], []

for epoch in range(0, epochs):
    new_best = False
    
    loss = train(epoch+1, 
                 model, train_loader, 
                 train_loss_func, 
                 opt, 
                 lr_scheduler, 
                 num_iters=-1, 
                 save_checkpoint_steps=4000)
    
    loss_train.append(loss)
    
    eval_loss, eval_acc = eval_model(model, val_loader, eval_loss_func, num_iters=-1)
    loss_val.append(eval_loss)
    acc_val.append(eval_acc)
    
    if(eval_acc > best_eval_acc):
        best_eval_acc = eval_acc
        best_eval_acc_epoch  = epoch+1
        torch.save(model.state_dict(), best_acc_file)
        new_best = True

    if(eval_loss < best_eval_loss):
        best_eval_loss       = eval_loss
        best_eval_loss_epoch = epoch+1
        torch.save(model.state_dict(), best_loss_file)
        new_best = True
    
    if(new_best):
        print("Best eval acc epoch:", best_eval_acc_epoch)
        print("Best eval acc:", best_eval_acc)
        print("")
        print("Best eval loss epoch:", best_eval_loss_epoch)
        print("Best eval loss:", best_eval_loss)

#@title Eval funct to eval separately if needed

DIC_SIZE = 512

#=====

init_step = 0
lr = LR_DEFAULT_START
lr_stepper = LrStepTracker(d_model, SCHEDULER_WARMUP_STEPS, init_step)
eval_loss_func = nn.CrossEntropyLoss(ignore_index=DIC_SIZE)
train_loss_func = eval_loss_func

opt = Adam(model.parameters(), lr=lr, betas=(ADAM_BETA_1, ADAM_BETA_2), eps=ADAM_EPSILON)
lr_scheduler = LambdaLR(opt, lr_stepper.step)


eval_loss, eval_acc = eval_model(model, val_loader, eval_loss_func, num_iters=-1)

"""# (SAVE)"""

#@title Save the model

print('Saving the model...')
full_path_to_model_checkpoint = "/content/Euterpe-Trained-Model.pth" #@param {type:"string"}
torch.save(model.state_dict(), full_path_to_model_checkpoint)
print('Done!')

"""# Congrats! You did it! :)"""