# Transcribe

## What is Transcribe

`Transcribe` is a non-interactive application that offers audio transcription based on `OpenAI` `Whisper` (and derivatives thereoff).

The main use case is sporadic transcription of audio or video files. There is intentionally no bulk mode (or API or library)
to help with large scale projects.

The supported flow is:

- Upload audio or video file using the `Files` interface of the web portal

- Configure transcription via the `Interactive Apps` -> `Transcribe` application (currently under `Testing` section at the bottom);
  you can select `Whisper inputfile`.

- Launch it and wait. Connecting to the running transcription is entirely optional; there is nothing interactive to do.
  You will also receive an email when the transcritpion started.

- Upon completion, you will receive an email with link to the result directory. This info will also be shown in the application session under
  `My interactive sessions` (but the session data is only available for a week).

  The result directory has a subdirectory per language with the text files and some metadata in JSON format of the transcritpion itself and input file.


This is intentionally kept simple. There is also no risk of loosing previous results
(although some previous result directories might get renamed when input file names are reused).

## Performance and default settings

The defaults should give the best balance between quality, performance and time to result.
You can expect approx 10 minutes of transcription time per language and per hour of input using the default flavour.
This combined with an almost immediate start time is the best combination for the intended use case.
There should be enough resources available to get this result most of the time.

## Advanced options

There are some advanced options one can choose from. They should not be needed for normal usage.

They are intended for corner cases, or to compare results between different `Whisper` models and/or different implementation flavours
(`whisper` and `whisper-ctranslate2`) with respect to speed and quality.

### Whisper language

Using the `Automatic detection` (the default), whisper determines the spoken language based on the first 30 seconds of audio.
If, for some reason, the autodection fails (e.g. the input file starts with silence or some music), you can force one of the languages.

When selecting more than one, the transcription will be done separately for each language
(this will also increase your total running time, so you might also want to increase the `Time`).

The selected language will also determine the output language. However, this is ***not*** meant as a translation feature;
although the quality is not that bad if your languages have enough similarity.

### Cluster

Changing the cluster from the interactive cluster will give you access to much better GPU,
but at a penalty of having to wait in the queue of the other cluster typically for a much longer time
than it will take to complete the transcription on the default cluster.

## Resources

Default settings of 4 cores with at least 10GB of RAM and 1 hour (wall)time should be enough for most transcriptions.

### Flavour

We currently support 2 flavours: `whisper` (the OpenAI reference implementation), and `whisper-ctranslate2`
(a faster version with some extras). Benchmarks indicate that `whisper-ctranslate2` is about 4 times faster than `whisper`,
but might have some lower quality.

### Model

Default model is `large-v3`, others can be choosen but should be careful to compare resulting speed and/or quality differences.

### Task

From the selected (or auto-detected) source speech language, you can choose to transcribe to the same language or to `English`.
You can use this last option to translate to English (as opposed to force the detection of the source language as if it was spoken in English).

