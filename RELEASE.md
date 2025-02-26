# Release History

*****************

## Release ONDEWO T2S API 6.1.0

### New Features

* [OND232-788](https://ondewo.atlassian.net/browse/OND232-788) Add T2SNormalization and word_to_phoneme_mapping to
  RequestConfig in SynthesizeRequest or BatchSynthesize
* [OND232-799](https://ondewo.atlassian.net/browse/OND232-799) Add StreamingSynthesize endpoint so text can be streamed
  to T2S and audio is streamed back

*****************

## Release ONDEWO T2S API 6.0.0

### New Features

* [OND232-749](https://ondewo.atlassian.net/browse/OND232-749) Added cloud service providers amazon, google, microsoft
  and elevenlabs as ondewo-t2s models.

*****************

## Release ONDEWO T2S API 5.4.0

### Improvements

* [OND232-631](https://ondewo.atlassian.net/browse/OND232-631) Add phoneme correction mapping feature in
  `T2SNormalization` to be able to customize phonemes in a specific voice model

*****************

## Release ONDEWO T2S API 5.3.0

### Improvements

* [OND232-495](https://ondewo.atlassian.net/browse/OND232-495) Add single inference as a new type of inference
* [OND232-495](https://ondewo.atlassian.net/browse/OND232-495) Add vits and vits_triton model

*****************

## Release ONDEWO T2S API 5.2.0

### Improvements

* Cleaned up API description
* Upgraded pre-commit hook libraries

*****************

## Release ONDEWO T2S API 5.1.0

### Improvements

* [OND232-438](https://ondewo.atlassian.net/browse/OND232-438) Moved CustomerPhonemizer endpoints to TextToSpeech
  service
* Added documentation of the endpoints and messages

*****************

## Release ONDEWO T2S API 5.0.0

### Improvements

* Synchronize all API Client Versions

*****************

## Release ONDEWO T2S API 4.3.0

### Improvements

* [[OND211-2039]](https://ondewo.atlassian.net/browse/OND211-2039) - Added pre-commit hooks and adjusted files to them

*****************

## Release ONDEWO T2S API 4.2.0

### New Features

* [[OND211-2039]](https://ondewo.atlassian.net/browse/OND211-2039) - Automated Release Process

*****************

## Release ONDEWO T2S API 4.1.0

### New Features

* Added normalizer to synthesize message.

*****************

## Release ONDEWO T2S API 4.0.5

### New Features

* Added callsign mapping.

*****************

## Release ONDEWO T2S API 4.0.4

### New Features

* Fix mapping type, added callsign long and short to configuration file api.

*****************

## Release ONDEWO T2S API 4.0.3

### New Features

* Add NormalizeText endpoint, that allows for text normalization without speech synthesis.

*****************

## Release ONDEWO T2S API 4.0.2

### New Features

* Add field T2SCustomLengthScales to T2SNormalizePipeline.

*****************

## Release ONDEWO T2S API 4.0.1

### New Features

* [[OND232-348]](https://ondewo.atlassian.net/browse/OND232-348) - Add field normalized_text to SynthesizeResponse.

*****************

## Release ONDEWO T2S API 4.0.0

### Breaking Changes

* [[OND232-343]](https://ondewo.atlassian.net/browse/OND232-343) - Rename oneof attributes and merged custom-phonemizer
  proto into text-to-speech proto

*****************

## Release ONDEWO T2S API 3.0.0

### Breaking Changes

* [[OND231-334]](https://ondewo.atlassian.net/browse/OND231-334) - Rename Description, GetServiceInfoResponse, Inference
  and Normalization messages to include S2T

*****************

## Release ONDEWO T2S API 2.0.0

### Breaking Changes

* `RequestConfig` implemented in SynthesizeRequest.

*****************

## Release ONDEWO T2S API 0.2.2

### Improvements

* Updated README.

*****************

## Release ONDEWO T2S API 0.2.1

### Bug fixes

* Updated licenses.

*****************

## Release ONDEWO T2S API 0.2.0

### New Features

* Move to GitHub!

### Improvements

* No longer closed source.

### Migration Guide

* [Replace submodule](https://stackoverflow.com/a/1260982/7756727) in the client.

*****************

## Release ONDEWO T2S API 0.1.0

### New Features

* Refactored individual project APIs into separate repos.

### Improvements

* Easier to develop independently.

### Known issues not covered in this release

* Harder to install apis under one heading-- this will be addressed at a later date.

### Migration Guide

* [Replace submodule](https://stackoverflow.com/a/1260982/7756727) in the client.

*****************
