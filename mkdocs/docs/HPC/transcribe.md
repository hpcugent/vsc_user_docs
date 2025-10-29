# Transcribe

## What is Transcribe

`Transcribe` is a non-interactive application that offers audio transcription based on `OpenAI` `Whisper` (and derivatives thereoff).

The main use case is sporadic transcription of audio or video files. There is intentionally no bulk mode (or API or library)
to help with large scale projects.

The supported flow is:

- Upload audio or video file using the `Files` interface of the web portal

- Configure transcription via the `Interactive Apps` -> `Transcribe` application (currently under `Testing` section at the bottom);
  you can select `Whisper inputfile` and `Whisper language`.

- Launch it and wait. Connecting to the running transcription is entirely optional; there is nothing interactive to do.
  You will also receive an email when the transcritpion started.

- Upon completion, you will receive an email with link to the result directory. This info will also be shown in the application session under
  `My interactive sessions` (but the session data is only available for a week).

  The result directory has a subdirectory per language (transcription and optional translation)
  with the text files and some metadata in JSON format of the transcritpion itself and input file.


This is intentionally kept simple. There is also no risk of loosing previous results
(although some previous result directories might get renamed when input file names are reused).


If you have issues, please report them via the `Problems with this session? Submit support ticket` link.


## Performance and default settings

The defaults should give the best balance between quality, performance and time to result.
You can expect approximate 10 minutes of transcription time per hour of input and
approximate 1 minute per translation language using the default flavour.
This performance combined with an almost immediate start time is the best combination for the intended use case.
There should be enough resources available to get this result most of the time.

## Advanced options

There are some advanced options one can choose from. They should not be needed for normal usage.

They are intended for corner cases, or to compare results between different `Whisper` models and/or different implementation flavours
(`whisper` and `whisper-ctranslate2`) with respect to speed and quality.

### Whisper language

The selected language will also determine the output language. However, this is ***not*** meant as a translation feature;
although the quality is not that bad if your languages have enough similarity.

### Translation target languages

Select one or more languages to translate to. Hold the `Ctrl` button pressed while clicking to select (or unselect) languages.

!!! warning
    Right-to-left languages might generate incorrect subtitles. If you have any examples, you can use the
    `Problems with this session? Submit support ticket` to report this so we can investigate properly.

The translation is run after the transcription, and is separate from the Whisper based process.
If you select a language to translate to that is also the `Whisper language`, there will be no translation generated for it.

The default languages are `Dutch` and `English`.  If e.g. you have a Dutch spoken video (and select Dutch as the `Whisper language`),
the end result will be a Dutch transcription and an English translation of the Dutch transcription. (And thus no `Dutch-to-Dutch` translation.)

There is thus no need to unselect the languages each time based on changing input languages.

### Model

Default model is `large-v3`, others can be choosen but should be careful to compare resulting speed and/or quality differences.

### Flavour

We currently support 3 flavours:
- `whisper` the OpenAI reference implementation
- `whisper-ctranslate2` a faster version with some extras
- `WhisperX` a faster version with most features like voice activity detection and speaker diarization

Benchmarks indicate that `whisper-ctranslate2` is about 4 times faster than `whisper`,
but might have some lower quality. `WhisperX` should be on par with `whisper-ctranslate2`.

### Speaker diarization

Speaker diarization (associate words with speaker) is only available for the `WhisperX` flavour.
You must both select the flavour and enable this feature to get the diarization working.

### Task

From the selected (or auto-detected) source speech language, you can choose to transcribe to the same language or to `English`.
You can use this last option to translate to English (as opposed to force the detection of the source language as if it was spoken in English).

### Cluster

Changing the cluster from the interactive cluster will give you access to much better GPU,
but at a penalty of having to wait in the queue of the other cluster typically for a much longer time
than it will take to complete the transcription on the default cluster.

## Resources

Default settings of 4 cores with at least 10GB of RAM and 1 hour (wall)time should be enough for most transcriptions.
But don't forget that translations and diarization add to the total runtime.
