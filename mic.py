import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import time,wave,datetime,os,csv

#For FFTs

def fft_calc(data_vec):
    data_vec = data_vec*np.hanning(len(data_vec)) # hanning window
    N_fft = len(data_vec) # length of fft
    freq_vec = (float(samp_rate)*np.arange(0,int(N_fft/2)))/N_fft # fft frequency vector
    fft_data_raw = np.abs(np.fft.fft(data_vec)) # calculate FFT
    fft_data = fft_data_raw[0:int(N_fft/2)]/float(N_fft) # FFT amplitude normalisation
    fft_data[1:] = 2.0*fft_data[1:]
    return freq_vec,fft_data

def pyserial_start():
    audio = pyaudio.PyAudio()
    # Audio stuff
    # format = bit depth of audio recording (16-bit is standard)
    # rate = Sample Rate (44.1kHz, 48kHz, 96kHz)
    # channels = channels to read (1-2, typically)
    # input_device_index = index of sound device
    # input = True (let pyaudio know you want input)
    # frames_per_buffer = chunk to grab and keep in buffer before reading
    stream = audio.open(format = pyaudio_format,rate = samp_rate,channels = chans, input_device_index = dev_index,input = True, frames_per_buffer=CHUNK)
    stream.stop_stream() # stop stream to prevent overload
    return stream,audio

def pyserial_end():
    stream.close()
    audio.terminate()

#To plot FFTs and other plots

def plotter(plt_1=0,plt_2=0):
    plt.style.use('ggplot')
    plt.rcParams.update({'font.size':16})
    if plt_1:
        fig,axs = plt.subplots(2,1,figsize=(12,8))
        ax = axs[0]
        ax.plot(t_vec,data,label='Time Series')
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Amplitude')
        ax.legend(loc='upper left')

        ax2 = axs[1]
        ax2.plot(freq_vec,fft_data,label='Frequency')
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.set_xlabel('Frequency [Hz]')
        ax2.set_ylabel('Amplitude')
        ax2.legend(loc='upper left')

        max_indx = np.argmax(fft_data)
        ax2.annotate(r'$f_{max}$'+' = {0:2.1f}Hz'.format(freq_vec[max_indx]),
                     xy=(freq_vec[max_indx],fft_data[max_indx]),
                     xytext=(2.0*freq_vec[max_indx],
                             (fft_data[max_indx]+np.mean(fft_data))/2.0),
                     arrowprops=dict(facecolor='black',shrink=0.1))

    if plt_2:
        fig2, ax3 = plt.subplots(figsize=(12, 8))
        t_spec = np.reshape(np.repeat(t_spectrogram, np.shape(freq_array)[1]), np.shape(freq_array))
        y_plot = fft_array
        spect = ax3.pcolormesh(t_spec, freq_array, y_plot, shading='nearest')
        ax3.set_ylim([20.0, 20000.0])
        ax3.set_yscale('log')
        cbar = fig2.colorbar(spect)
        cbar.ax.set_ylabel('Amplitude', fontsize=16)

    fig.subplots_adjust(hspace=0.3)
    fig.savefig('Rel_Plots.png', dpi=300,
                bbox_inches='tight')
    plt.show()

def data_grabber(rec_len):
    stream.start_stream()
    stream.read(CHUNK,exception_on_overflow=False)
    t_0 = datetime.datetime.now()
    data,data_frames = [],[]
    for frame in range(0,int((samp_rate*rec_len)/CHUNK)):
        stream_data = stream.read(CHUNK,exception_on_overflow=False)
        data_frames.append(stream_data)
        data.append(np.frombuffer(stream_data,dtype=buffer_format))
    stream.stop_stream()
    return data,data_frames,t_0

def data_analyzer(chunks_ii):
    freq_array,fft_array = [],[]
    t_spectrogram = []
    data_array = []
    t_ii = 0.0
    for frame in chunks_ii:
        freq_ii,fft_ii = fft_calc(frame) # calculate fft for chunk
        freq_array.append(freq_ii)
        fft_array.append(fft_ii)
        t_vec_ii = np.arange(0,len(frame))/float(samp_rate)
        t_ii+=t_vec_ii[-1]
        t_spectrogram.append(t_ii) # time step for time v freq. plot
        data_array.extend(frame)
    t_vec = np.arange(0,len(data_array))/samp_rate
    freq_vec,fft_vec = fft_calc(data_array)
    return t_vec,data_array,freq_vec,fft_vec,freq_array,fft_array,t_spectrogram

def data_saver(t_0):
    data_folder = './data/'
    if os.path.isdir(data_folder)==False:
        os.mkdir(data_folder)
    filename = datetime.datetime.strftime(t_0, '%Y_%m_%d_%H_%M_%S_pyaudio') # filename based on recording time
    wf = wave.open(data_folder+filename+'.wav','wb')
    wf.setnchannels(chans)
    wf.setsampwidth(audio.get_sample_size(pyaudio_format))
    wf.setframerate(samp_rate)
    wf.writeframes(b''.join(data_frames))
    wf.close()
    return filename

if __name__=="__main__":
    CHUNK          = 44100  # FFT windows
    samp_rate      = 44100 # sample rate (Choose, 44100, 48000, 96000 ideally equal to chunks but computationally expensive)
    pyaudio_format = pyaudio.paInt16 # bitrate of mic (Im not sure of this so setting to default 16)
    buffer_format  = np.int16 # bitrate equal to mic's
    chans          = 1 # only read 1 channel (As we are using mono in each pi and not stereo)
    dev_index      = 0 # defaults to one

    stream,audio = pyserial_start()
    record_length = 1200 #Record for 20 mins
    noise_chunks,_,_ = data_grabber(CHUNK/samp_rate)
    data_chunks,data_frames,t_0 = data_grabber(record_length)
    data_saver(t_0)
    pyserial_end()
    _,_,_,fft_noise,_,_,_ = data_analyzer(noise_chunks)
    t_vec,data,freq_vec,fft_data,freq_array,fft_array,t_spectrogram = data_analyzer(data_chunks)
    fft_array = np.subtract(fft_array,fft_noise) #Denoising
    freq_vec = freq_array[0]
    fft_data = np.mean(fft_array[1:,:],0)
    fft_data = fft_data+np.abs(np.min(fft_data))+1.0
    plotter(plt_1=1,plt_2=0) #(plt_1 is time/freq), (plt_2 is spectrogram) choose 1 or 0 to satisfy boolean in the plotter function above

