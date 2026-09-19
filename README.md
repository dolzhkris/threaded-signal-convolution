# threaded-signal-convolution
Python implementation of sequential and multithreaded signal convolution with a low-pass filter using NumPy and threading.

## About

This project demonstrates the processing of a digital signal using convolution with an impulse response of a low-pass filter. The project was developed as part of university work during the fourth year of university.

## Key Functions

* generate_signal() - generates the input signal and its time axis.
* convolve_seq() - performs sequential convolution of the input signal with the filter impulse response.
* worker_thread() - processes an assigned range of signal samples in a separate thread.
* parent_thread() - creates and starts worker threads, distributes processing ranges, and waits for their completion.
* plot() - displays the original signal, the signal after low-pass filtering and the impulse response of the filter.

## Key Variables

* N - number of samples in the impulse response;
* fc - filter cutoff frequency parameter;
* num_threads - number of worker threads;
* h - impulse response of the filter;
* x - input signal;
* y - shared result of multithreaded processing;
* y_seq - result of sequential convolution;
* y_par - result of multithreaded convolution;
* t - time axis of the generated signal;
* chunk_size - size of the processing range assigned to a thread;
* start_k - starting index of a processing range;
* end_k - ending index of a processing range;
* lock - synchronization object for accessing the shared result;
* thread_id - identifier of a worker thread.

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/dolzhkris/threaded-signal-convolution.git
```

2. Install the required libraries:

```bash
pip install -r requirements.txt
```

3. Run the program:

```bash
python main.py
```
